from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models


class Formulario(models.Model):
    titulo = models.CharField("Titulo", max_length=100)
    descricao = models.TextField("Descricao", blank=True, null=True)

    #Opções das respostas
    aceitaResposta = models.BooleanField("Aceita respostas", default=True, blank=True)
    unicaResposta = models.BooleanField("Unica resposta por pessoa", default=True, blank=True)
    # Questoes ainda a ser implementada
    #dataInicio = models.DateTimeField("Data Inicio", null=True, blank=True, )
    #dataTermino = models.DateTimeField("Data Termino", null=True, blank=True, )

    mensagemAgradecimento = models.TextField("Mensagem de Agradecimento", blank=True,default="")
    slug = AutoSlugField(populate_from='dataCriacao', unique=True)

    #Responsavel
    criador = models.ForeignKey(User, verbose_name="Criador", on_delete=models.SET_NULL, null=True)

    dataCriacao = models.DateTimeField("Data Criacao", editable=False, auto_now_add=True)
    dataUltimaAlteracao = models.DateTimeField("Data da Ultima Alteração", editable=False, auto_now=True)


    class Meta:
        verbose_name = "Formulário"
        verbose_name_plural = "Formulários"

    def __str__(self):
        return self.titulo

    def save(self,*args,**kwargs):
        if (self.titulo is None or self.titulo=='') and self.criador:
            count=Formulario.objects.filter(criador=self.criador).count()+1
            self.titulo = f"Questionário {count}"

        return super(Formulario, self).save(*args,**kwargs)

    def ultimaAlteracao(self):
        return max([*[_.ultimaAlteracao() for _ in self.secao_set.all()], self.dataUltimaAlteracao if self.dataUltimaAlteracao else self.dataCriacao])

    def getQuestoes(self):
        return Questao.objects.filter(secao__formulario=self)
    questoes = property(getQuestoes)

from .Secao import Secao
from .Questao import *

from .Resposta import *
