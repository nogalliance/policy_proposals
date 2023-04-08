from django.utils.text import slugify
from django.views.generic import TemplateView

from proposals.models import PolicyProposal


class Home(TemplateView):
    template_name = 'home.html'

    @property
    def extra_context(self):
        state_names = PolicyProposal.objects.values_list('state', flat=True).distinct().order_by('state')

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

        proposals = PolicyProposal.objects.filter(state__in=selected_states).order_by('-last_change')

        return {
            'states': states,
            'proposals': proposals,
        }
