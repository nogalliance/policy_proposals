import argparse
import re
from pprint import pprint
from urllib.parse import urljoin

import bs4
import dateparser
import requests
from bs4 import BeautifulSoup
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
    verbosity = 1

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('rir', nargs='?', choices=RegionalInternetRegistry.objects.values_list('slug', flat=True))

    def output(self, level: int = 1, msg="", style_func=None, ending=None):
        if self.verbosity >= level:
            self.stdout.write(msg=msg, style_func=style_func, ending=ending)

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity', 1)

        if options['rir']:
            rirs = RegionalInternetRegistry.objects.filter(slug=options['rir'])
        else:
            rirs = RegionalInternetRegistry.objects.all()

        global_now = timezone.now()

        for rir in rirs:
            self.output(2, f"Processing {rir.name}", style_func=self.style.HTTP_INFO)

            try:
                response = requests.get(rir.proposals_url, headers={'Accept-Encoding': ''})
                if not response.ok:
                    self.output(0, f"{rir.name} Proposals URL returned {response.status_code}", self.style.ERROR)
                    self.output(3, rir.proposals_url)
                    continue
            except requests.exceptions.RequestException as e:
                self.output(0, f"{rir.name} Proposals URL raised {e}", self.style.ERROR)
                self.output(3, rir.proposals_url)
                continue

            date_settings = {
                'TIMEZONE': str(rir.timezone),
                'RETURN_AS_TIMEZONE_AWARE': True,
                'DATE_ORDER': rir.date_order,
                'PREFER_LOCALE_DATE_ORDER': False,
            }

            bs = BeautifulSoup(response.content, features="html5lib")
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
                    self.output(1, f"Found {rir.name} proposal without identifier, check the CSS selectors!")
                    continue

                # Get the last modified date
                date = find(proposal_element, rir.date_selector)
                last_change = dateparser.parse(date, settings=date_settings) if date else None

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
                    'last_change': last_change or global_now
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

                if updated and not last_change:
                    last_change = global_now

                if last_change and proposal.last_change != last_change:
                    proposal.last_change = last_change
                    updated = True

                if updated:
                    proposal.save()

                if created or updated:
                    self.output(2, f"{identifier} -!- {date} -!- {name} -!- {state} -!- {url}")
