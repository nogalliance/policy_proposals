from django.contrib import admin

from proposals.models import RegionalInternetRegistry, PolicyProposal


@admin.register(RegionalInternetRegistry)
class RegionalInternetRegistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'proposals_url')
    ordering = ('name',)


@admin.register(PolicyProposal)
class PolicyProposalAdmin(admin.ModelAdmin):
    list_display = ('rir', 'identifier', 'name', 'state', 'last_change')
    list_filter = ('rir', 'state')
    ordering = ('last_change', 'rir', 'identifier')
