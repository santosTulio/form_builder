from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from FormBuilderApp.models import Formulario


class Dashboard(LoginRequiredMixin,ListView):
    model = Formulario
    template_name = 'dashboard/index.html'
    context_object_name = 'formularios'

    def get_queryset(self):
        return super(Dashboard, self).get_queryset().filter(criador__username=self.request.user).order_by('-dataUltimaAlteracao')