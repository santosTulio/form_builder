from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from FormBuilderApp.models import Questionario


class PerguntaView(LoginRequiredMixin,DetailView):
    model = Questionario
    template_name = 'formbuilder/Perguntas.html'
    context_object_name = 'questionario'

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') is None:
            q=Questionario(criador=User.objects.get(username=self.request.user))
            q.save()
            return HttpResponseRedirect(reverse('formbuilder:formulario-perguntas',kwargs={'pk':q.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PerguntaView, self).get_context_data(**kwargs)
        return context