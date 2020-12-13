from django.db import models

from FormBuilderApp.models import *

from FormBuilderApp.models.Formulario.Questao import LISTA_SUSPENSA, OPCOES, DECIMAL, INTEIRO

class Resposta(models.Model):
    submissao =models.ForeignKey("Submissao", on_delete=models.CASCADE)
    questao = models.ForeignKey('Questao', on_delete=models.CASCADE)
    numero = models.FloatField("Numero", default=None, null=True)
    opcoes = models.ManyToManyField('Alternativa')
    texto = models.TextField("Resposta", default=None, null=True)

    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"

    def checkNumber(self):
        if self.questao.subTipoCampo in [INTEIRO, DECIMAL]:
            try:
                (int(self.numero) if self.questao.subTipoCampo == INTEIRO else float(self.numero))
            except ValueError:
                return False
            return self.questao.numeroMinimo < self.numero < self.questao.numeroMaximo
        return False


    def save(self, *args, **kwargs):
        if self.submissao.formulario == self.questao.formulario:
            return super(Resposta, self).save(*args,**kwargs)
        raise Exception('Formulário da submissão diferente da questão')

    def getTipo(self):
        return self.questao.subTipoCampo
    tipo = property(getTipo)

    def getSecao(self):
        return self.questao.secao
    secao = property(getSecao)

    def getResposta(self):
        if self.tipo in [OPCOES,LISTA_SUSPENSA]:
            return [_ for _ in self.opcoes.all()]
        if self.tipo in [INTEIRO,DECIMAL]:
            if self.tipo == INTEIRO:
                return int(self.numero)
            return self.numero
        return self.texto
    resposta = property(getResposta)
