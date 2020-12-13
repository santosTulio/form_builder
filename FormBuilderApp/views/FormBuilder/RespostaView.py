from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from FormBuilderApp.models import Formulario, User


class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['titulo', 'descricao','aceitaResposta','dataInicio','dataTermino','mensagemAgradecimento']

class PerguntasView(CreateView):
    model = Formulario
    form_class = QuestionarioForm


