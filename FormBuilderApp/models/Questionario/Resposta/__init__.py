from django.contrib.auth.models import User
from django.db import models

class Resposta(models.Model):
    questao = models.ForeignKey('Questao', on_delete=models.SET_NULL, null=True)
    proprietarioResposta = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    dataCadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)
    dataAlteracao = models.DateTimeField("Data Ultima Alteração", auto_now=True)

    ativo = models.BooleanField("Ativo", default=True, blank=True)

    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"

    def getTipo(self):
        return self.questao.tipoCampo
    tipo = property(getTipo)

    def getQuestionario(self):
        return self.questao.questionario
    questionario = property(getQuestionario)

    def getSecao(self):
        return self.questao.secao
    secao = property(getSecao)


