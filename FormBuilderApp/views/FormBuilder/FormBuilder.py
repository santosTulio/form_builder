from django import forms
from django.views.generic import CreateView, DetailView

from FormBuilderApp.models import Questionario

class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        fields = ['titulo', 'descricao','aceitaResposta','dataInicio','dataTermino','mensagemAgradecimento','criador','ativo']


class FormBuilder(DetailView):
    model = Questionario
    template_name = 'formbuilder/Formulario.html'
    context_object_name = 'questionario'