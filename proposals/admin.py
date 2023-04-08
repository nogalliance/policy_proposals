from django.contrib import admin
from django.db.models import Max
from django.utils.translation import gettext_lazy as _

from proposals.models import RegionalInternetRegistry, PolicyProposal


@admin.register(RegionalInternetRegistry)
class RegionalInternetRegistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'timezone', 'date_order', 'admin_proposals', 'admin_last_change')
    ordering = ('name',)

    @admin.display(description=_('Proposals'))
    def admin_proposals(self, rir: RegionalInternetRegistry):
        return rir.policyproposal_set.count()

    @admin.display(description=_('Last change'))
    def admin_last_change(self, rir: RegionalInternetRegistry):
        return rir.policyproposal_set.aggregate(Max('last_change'))['last_change__max']


@admin.register(PolicyProposal)
class PolicyProposalAdmin(admin.ModelAdmin):
    list_display = ('rir', 'identifier', 'name', 'state', 'last_change')
    list_filter = ('rir', 'state')
    ordering = ('last_change', 'rir', 'identifier')
