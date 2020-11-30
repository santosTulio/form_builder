from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from FormBuilderApp.models import Questionario, User


class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        fields = ['titulo', 'descricao','aceitaResposta','dataInicio','dataTermino','mensagemAgradecimento','criador','ativo']

class PerguntasView(CreateView):
    model = Questionario
    form_class = QuestionarioForm


class RespostaView(LoginRequiredMixin,DetailView):
    model = Questionario
    template_name = 'formbuilder/Respostas.html'
    context_object_name = 'questionario'

    def get_context_data(self, **kwargs):
        context = super(RespostaView, self).get_context_data(**kwargs)
        questionario=self.get_object()
        if hasattr(questionario, 'submissao_set'):
            pass

        return context
