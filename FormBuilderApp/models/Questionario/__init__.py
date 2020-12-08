from django.contrib.auth.models import User
from django.db import models


class Questionario(models.Model):
    titulo = models.CharField("Titulo", max_length=100)
    descricao = models.TextField("Descricao", blank=True, null=True)

    #Opções das respostas
    aceitaResposta = models.BooleanField("Aceita respostas", default=True, blank=True)
    dataInicio = models.DateTimeField("Data Inicio", null=True, blank=True)
    dataTermino = models.DateTimeField("Data Termino", null=True, blank=True)
    mensagemAgradecimento = models.TextField("Mensagem de Agradecimento", blank=True,default="")

    #Responsavel
    criador = models.ForeignKey(User, verbose_name="Criador", on_delete=models.SET_NULL, null=True)

    dataCriacao = models.DateTimeField("Data Criacao", editable=False, auto_now_add=True)
    dataUltimaAlteracao = models.DateTimeField("Data da Ultima Alteração", editable=False, auto_now=True)

    #Ativo
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Questionario"
        verbose_name_plural = "Questionarios"

    def __str__(self):
        return self.titulo

    def respostasPerQuestao(self):
        qsSecoes = self.secao_set.all()
        qsQuestoes = Questao.objects.filter(secao__in=qsSecoes)
        qsResposta = Resposta.objects.filter(questionario = self)

    def save(self,*args,**kwargs):
        if (self.titulo is None or self.titulo=='') and self.criador:
            count=Questionario.objects.filter(criador=self.criador).count()+1
            self.titulo = f"Questionário {count}"
        print(self.titulo)
        return super(Questionario, self).save(*args,**kwargs)





from .Secao import Secao
from .Questao import *

from .Resposta import *
