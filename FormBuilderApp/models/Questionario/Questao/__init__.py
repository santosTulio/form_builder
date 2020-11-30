from django.db import models

from FormBuilderApp.models.Questionario.TipoArquivo import TipoArquivo


tipoTexto=[
    "Resposta Curta",
    "Resposta Longa",
]
tipoEscolha=[
    "Lista Suspensa",
    "Opções",
]
tipoNumero=[
    "Decimal",
    "Inteiro",
]

tipos =[*tipoTexto,*tipoEscolha,*tipoNumero]

class Questao(models.Model):
    secao = models.ForeignKey("Secao",on_delete=models.SET_NULL,null=True)
    pergunta = models.CharField("Pergunta",max_length=1000)

    placeholder = models.CharField("Placeholder", max_length=100,default="", blank=True)
    helptext = models.CharField("Texto de Ajuda", max_length=1000, default="", blank=True)

    posicao = models.FloatField("Posicao",default=0, blank=True)

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
        ordering = ["id", "posicao"]

    def getQuestionario(self):
        return self.secao.questionario
    questionario = property(getQuestionario)

    def save(self):
        secao = self.secao
        pergunta = self.pergunta
        placeholder = self.placeholder
        helptext = self.placeholder
        posicao = self.posicao

#------------------------ Texto ------------------------#

class QuestaoTexto(Questao):
    tipoCampo = models.CharField("Tipo de Campo", max_length=100, choices=[(i,i) for i in tipoTexto])

    class Meta:
        verbose_name = "Questão Texto"
        verbose_name_plural = "Questões Texto"

#------------------------ Escolha ------------------------#

class QuestaoEscolha(Questao):
    tipoCampo = models.CharField("Tipo de Campo", max_length=100, choices=[(i,i) for i in tipoEscolha])
    #Alternativas
    multipas = models.BooleanField("Multipla escolha", default=False)

class Alternativa(models.Model):
    questaoEscolha = models.ForeignKey("QuestaoEscolha", on_delete=models.SET_NULL, null=True)

    rotulo = models.CharField("Rotulo", max_length=1000)

#------------------------ Numero ------------------------#

class QuestaoNumero(Questao):
    tipoCampo = models.CharField("Tipo de Campo", max_length=100, choices=[(i,i) for i in tipoNumero])
    #Numero
    numeroMinimo = models.FloatField("Numero Minimo",null=True,blank=True)
    numeroMaximo = models.FloatField("Numero Máximo",null=True,blank=True)
