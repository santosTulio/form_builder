from django.db import models


class Resposta(models.Model):
    submissao =models.ForeignKey("Submissao", on_delete=models.CASCADE)
    questao = models.ForeignKey('Questao', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"


    def save(self, *args, **kwargs):
        if self.questao.questionario.valida():
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
