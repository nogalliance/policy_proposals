import argparse
import re
from urllib.parse import urljoin

import bs4
import requests
from bs4 import BeautifulSoup
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.utils import timezone

from proposals.models import RegionalInternetRegistry, PolicyProposal


def clean(string: str) -> str:
    return re.sub(r'\s{2,}', ' ', string.strip().strip(':'))


def find(proposal_element: bs4.Tag, selector_str: str, attr: str = None) -> str:
    selectors = selector_str.split()
    element = proposal_element

    if not selectors:
        return ''

    while selectors:
        selector = selectors[0]
        if selector == ':scope':
            # Select the element itself, built-in implementation doesn't seem to work
            pass
        elif selector == ':parent':
            element = element.parent
        elif selector == ':previous-tag':
            while element:
                element = element.previous_sibling
                if isinstance(element, bs4.Tag):
                    break
        else:
            break

        selectors.pop(0)

    # Process the selector
    if element and selectors:
        selector_str = ' '.join(selectors)
        elements = element.css.select(selector_str)
        element = elements[0] if elements else None

    if not element:
        return ''

    if attr:
        # Return an attribute
        return clean(element[attr])
    else:
        # Return the content
        return clean(element.text)


class Command(BaseCommand):
    help = "Retrieve RIR proposals."
    output_transaction = True

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('rir', nargs='?', choices=RegionalInternetRegistry.objects.values_list('slug', flat=True))

    def handle(self, *args, **options):
        if options['rir']:
            rirs = RegionalInternetRegistry.objects.filter(slug=options['rir'])
        else:
            rirs = RegionalInternetRegistry.objects.all()

        now = timezone.now()

        for rir in rirs:
            response = requests.get(rir.proposals_url)
            if not response.ok:
                raise CommandError(f"{rir.name} Proposals URL returned {response.status_code}")

            bs = BeautifulSoup(response.text, features="html5lib")
            for proposal_element in bs.css.select(rir.proposal_selector):
                identifier = find(proposal_element, rir.identifier_selector)

                if rir.name_selector == rir.identifier_selector:
                    # Identifiers and names are stored in one element, split them
                    parts = re.split('[: ]', identifier, 1)
                    identifier = clean(parts[0])
                    name = clean(' '.join(parts[1:]))
                else:
                    name = find(proposal_element, rir.name_selector)

                # Abort if we don't have an identifier
                if not identifier:
                    self.stderr.write("Found a proposal without identifier, check the CSS selectors!")
                    continue

                # Get the state and normalise it a bit
                state = find(proposal_element, rir.state_selector)
                if state.lower().startswith('reached consensus'):
                    state = 'Consensus'
                elif state.lower() in ('open for discussion', 'under discussion'):
                    state = 'Under discussion'
                elif state.lower() in ('abandoned', 'did not reach consensus'):
                    state = 'No consensus'

                url = find(proposal_element, rir.url_selector, 'href')
                if not url and rir.url_template:
                    url = rir.url_template.format(**{
                        'identifier': identifier,
                        'name': name,
                        'state': state,
                    })
                url = urljoin(rir.proposals_url, url)

                proposal, created = PolicyProposal.objects.get_or_create(defaults={
                    'name': name,
                    'state': state,
                    'url': url,
                    'last_change': now
                }, rir=rir, identifier=identifier)

                updated = False
                if name and proposal.name != name:
                    proposal.name = name
                    updated = True

                if state and proposal.state != state:
                    proposal.state = state
                    updated = True

                if url and proposal.url != url:
                    proposal.url = url
                    updated = True

                if updated:
                    proposal.last_change = now
                    proposal.save()

                if created or updated:
                    print(f"{identifier} -!- {name} -!- {state} -!- {url}")
