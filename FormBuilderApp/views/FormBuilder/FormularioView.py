from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, DeleteView

from FormBuilderApp.models import Formulario, Submissao, Questao, Resposta, OPCOES, LISTA_SUSPENSA, RESPOSTA_CURTA, \
    RESPOSTA_LONGA
from FormBuilderApp.views.FormBuilder.SubmissaoView import SubmissaoCreateView


class FormularioDeleteRedirectView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('formbuilder:dashboard')
    model = Formulario
    template_name = 'formbuilder/DeletarFormulario.html'
    context_object_name = 'formulario'

class ConstrutorDeFormularioView(LoginRequiredMixin, DetailView):
    model = Formulario
    template_name = 'formbuilder/BuilderForm.html'
    context_object_name = 'formulario'

    def get_queryset(self):
        return super(ConstrutorDeFormularioView, self).get_queryset().filter(criador__username=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') is None:
            q=Formulario(criador=self.request.user)
            q.save()
            return HttpResponseRedirect(reverse('formbuilder:editar-formulario',kwargs={'pk':q.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConstrutorDeFormularioView, self).get_context_data(**kwargs)
        context.update({
            'editando':True
        })
        return context

class FormularioSubmissaoViewer(SubmissaoCreateView):

    template_status_submit = 'formbuilder/StatusViewerFormulario.html'

    def get(self,request, *args, **kwargs):
        formulario = get_object_or_404(Formulario, slug=kwargs['slug'])
        if formulario.aceitaResposta and formulario.questoes.count() > 0:
            if hasattr(formulario,'submissao_set') and formulario.unicaResposta:
                if formulario.submissao_set.filter(proprietarioResposta=self.request.user).count()>0:
                    return render(request, self.template_status_submit,
                                  {'formulario': formulario, 'user': self.request.user, 'status': 'ALREADY_ANSWERED', 'visualizando':True})
            return render(request, 'formbuilder/ViewerFormulario.html', {'formulario': formulario, 'status':'ACCEEPT', 'visualizando':True})




        return render(request, self.template_status_submit,
                   {'formulario': formulario, 'user': self.request.user, 'status': 'NOT_ACCEPTING', 'visualizando':True})