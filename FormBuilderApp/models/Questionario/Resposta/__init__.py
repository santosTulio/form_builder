from django.contrib.auth.models import User
from django.db import models

class Submissao(models.Model):
    proprietarioResposta = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True,blank=True)
    dataUltimaAlteracao = models.DateTimeField(blank=True)

    def add(self, resposta):
        resposta.submissao = self
        if hasattr(self,'resposta_set'):
            if self.resposta_set.first().questionario == resposta.questionario:
                resposta.save()
            else:
                raise PermissionError("Resposta de questionario diferente")
        else:
            resposta.save()
        return True

from .Resposta import *
from .RespostaEscolha import *
from .RespostaNumero import *
from .RespostaTexto import *