from django.db import models

from FormBuilderApp.models import *


class Resposta(models.Model):
    submissao =models.ForeignKey("Submissao", on_delete=models.CASCADE)
    questao = models.ForeignKey('Questao', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"


    def save(self, *args, **kwargs):
        if self.questao.questionario.valida() and self.questao.valida:
            return super(Resposta, self).save(*args,**kwargs)
        raise PermissionError("Questionario não validado")

    def getTipo(self):
        return self.questao.tipoCampo
    tipo = property(getTipo)

    def getQuestionario(self):
        return self.questao.questionario
    questionario = property(getQuestionario)

    def getSecao(self):
        return self.questao.secao
    secao = property(getSecao)

    def get_resposta(self):
        if self.tipo in tipoTexto:
            return self.respostatexto
        if self.tipo in tipoEscolha:
            return self.respostaescolha
        if self.tipo in tipoNumero:
            return self.respostanumero
    resposta = property(get_resposta)