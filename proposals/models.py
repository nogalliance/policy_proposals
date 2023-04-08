from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField


class RegionalInternetRegistry(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    slug = AutoSlugField(verbose_name=_('Slug'), populate_from='name', unique=True, db_index=True)
    proposals_url = models.URLField(verbose_name=_('Proposals URL'))
    proposal_selector = models.CharField(verbose_name=_('Proposal selector'), max_length=100, blank=True,
                                         help_text=_('CSS selector that selects one proposal per match'))
    identifier_selector = models.CharField(verbose_name=_('Identifier selector'), max_length=100, blank=True,
                                           help_text=_('CSS selector that selects the identifier of one proposal'))
    name_selector = models.CharField(verbose_name=_('Name selector'), max_length=100, blank=True,
                                     help_text=_('CSS selector that selects the name of one proposal'))
    state_selector = models.CharField(verbose_name=_('State selector'), max_length=100, blank=True,
                                      help_text=_('CSS selector that selects the state of one proposal'))
    url_selector = models.CharField(verbose_name=_('URL selector'), max_length=100, blank=True,
                                    help_text=_('CSS selector that selects the URL of one proposal'))
    url_template = models.CharField(verbose_name=_('URL template'), max_length=100, blank=True,
                                    help_text=_('Template for converting a proposal into a URL'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Regional Internet Registry')
        verbose_name_plural = _('Regional Internet Registries')


class PolicyProposal(models.Model):
    rir = models.ForeignKey(verbose_name=_('RIR'), to=RegionalInternetRegistry, on_delete=models.RESTRICT)
    identifier = models.CharField(verbose_name=_('Identifier'), max_length=25)
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    state = models.CharField(verbose_name=_('State'), max_length=25)
    url = models.URLField(verbose_name=_('URL'))
    last_change = models.DateTimeField(verbose_name=_('Last change'), editable=False)

    def __str__(self):
        return f'{self.rir.name} {self.identifier}: {self.name}'

    class Meta:
        unique_together = (
            ('rir', 'identifier')
        )
        verbose_name = _('Policy Proposal')
        verbose_name_plural = _('Policy Proposals')
