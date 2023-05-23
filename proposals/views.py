from datetime import timedelta

from django.utils.text import slugify
from django.utils.timezone import now
from django.views.generic import TemplateView

from proposals.models import PolicyProposal, RegionalInternetRegistry


class Home(TemplateView):
    template_name = 'home.html'

    @property
    def extra_context(self):
        last_year = now() - timedelta(days=365)
        base_proposals = PolicyProposal.objects.exclude(state__in=['Implemented', 'No consensus'], last_change__lt=last_year)
        state_names = base_proposals.values_list('state', flat=True).distinct().order_by('state')

        default = 'on' if len(self.request.GET) == 0 else 'off'

        selected_states = []
        states = []
        for state_name in state_names:
            key = slugify(state_name)
            state = {
                'name': state_name,
                'key': key,
                'enabled': self.request.GET.get(key, default) != 'off'
            }
            states.append(state)

            if state['enabled']:
                selected_states.append(state_name)

        selected_rirs = []
        rirs = []
        for registry in RegionalInternetRegistry.objects.order_by('name'):
            rir = {
                'name': registry.name,
                'key': registry.slug,
                'enabled': self.request.GET.get(registry.slug, default) != 'off'
            }
            rirs.append(rir)

            if rir['enabled']:
                selected_rirs.append(registry.id)

        proposals = base_proposals \
            .filter(state__in=selected_states) \
            .filter(rir_id__in=selected_rirs) \
            .order_by('-last_change', 'identifier')

        return {
            'states': states,
            'proposals': proposals,
            'rirs': rirs,
        }
