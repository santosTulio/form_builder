from django.db import models

from FormBuilderApp.models.Questionario.Resposta import Resposta


class RespostaEscolha(models.Model):
    resposta = models.OneToOneField(Resposta,on_delete=models.CASCADE)

    opcoes = models.ManyToManyField('Alternativa')

    class Meta:
        verbose_name = "Resposta com escolha"
        verbose_name_plural = "Respostas com escolha"


