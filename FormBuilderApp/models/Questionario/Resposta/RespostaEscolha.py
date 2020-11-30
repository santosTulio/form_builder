from django.db import models

from FormBuilderApp.models.Questionario.Resposta import Resposta


class RespostaEscolha(Resposta):

    opcoes = models.ManyToManyField('Alternativa')

    class Meta:
        verbose_name = "Resposta com escolha"
        verbose_name_plural = "Respostas com escolha"


