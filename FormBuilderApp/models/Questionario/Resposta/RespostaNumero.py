from django.db import models

from FormBuilderApp.models.Questionario.Resposta import Resposta


class RespostaNumero(Resposta):
    numero = models.FloatField("Numero")

    class Meta:
        verbose_name = "Resposta com Numero"
        verbose_name_plural = "Respostas com Numero"