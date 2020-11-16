from django.db import models

from FormBuilderApp.models.Questionario.Resposta import Resposta


class RespostaTexto(Resposta):
    texto = models.TextField("Resposta")

    class Meta:
        verbose_name = "Resposta de Texto"
        verbose_name_plural = "Respostas de Texto"