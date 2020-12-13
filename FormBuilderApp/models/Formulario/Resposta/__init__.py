from django.contrib.auth.models import User
from django.db import models

class Submissao(models.Model):
    proprietarioResposta = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True,blank=True)
    dataUltimaAlteracao = models.DateTimeField(blank=True, auto_now=True)
    formulario = models.ForeignKey('Formulario',on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Submissão'
        verbose_name_plural = 'Submissões'

    def __str__(self):
        return f'{self.proprietarioResposta.get_full_name() if self.proprietarioResposta else "Usuário desconhecido"} - {self.formulario}'

    def checkSubmissao(self):
        if self.formulario.aceitaResposta:
            if self.formulario.unicaResposta and hasattr(self.formulario,'submissao_set') and self.formulario.submissao_set.filter(proprietarioResposta=self.proprietarioResposta).count() > 0:
                return "ALREADY_ANSWERED"
            return "ACCEPT"
        return "NOT_ACCEPTING"



from .Resposta import *