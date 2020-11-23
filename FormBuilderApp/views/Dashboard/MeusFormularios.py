from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from FormBuilderApp.models import Questionario


class MeusFormularioView(LoginRequiredMixin,ListView):
    model = Questionario
    template_name = 'dashboard/MeusFormularios.html'
    context_object_name = 'questionarios'

    def get_queryset(self):
        return super().get_queryset().filter(ativo=True, criador__username=self.request.user).order_by('-dataUltimaAlteracao')