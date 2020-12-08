from django.db import models

#from FormBuilderApp.models.Questionario.TipoArquivo import TipoArquivo

RESPOSTA_CURTA = 1
RESPOSTA_LONGA = 2
LISTA_SUSPENSA = 3
OPCOES         = 4
DECIMAL        = 5
INTEIRO        = 6

tipoTexto=[
    RESPOSTA_CURTA,
    RESPOSTA_LONGA
]
tipoTextoChoices=[
    (RESPOSTA_CURTA, 'Resposta Curta'),
    (RESPOSTA_LONGA, 'Resposta Longa'),
]
tipoEscolha=[
    LISTA_SUSPENSA,
    OPCOES
]
tipoEscolhaChoices=[
    (LISTA_SUSPENSA, 'Lista Suspensa'),
    (OPCOES, 'Opções'),
]
tipoNumero=[
    DECIMAL,
    INTEIRO,
]
tipoNumeroChoices=[
    (DECIMAL, 'Decimal'),
    (INTEIRO, 'Inteiro'),
]
TEXTO = 1
NUMERO = 2
ESCOLHAS = 3

tipos =[
    (1,"Texto"),
    (2,"Numero"),
    (3,"Escolhas")
    ]



class Questao(models.Model):
    secao = models.ForeignKey("Secao",on_delete=models.CASCADE)
    pergunta = models.CharField("Pergunta",max_length=1000)

    placeholder = models.CharField("Placeholder", max_length=100,default="", blank=True)

    obrigatorio = models.BooleanField(default=False)

    tipoCampo = models.IntegerField("Tipo de Campo", choices=tipos)

    posicao = models.FloatField("Posicao",default=0, blank=True)

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
        ordering = ["id", "posicao"]

    def getQuestionario(self):
        return self.secao.questionario
    questionario = property(getQuestionario)

    def questaoTipo(self):
        if self.tipoCampo == 1 :
            return self.questaotexto
        if self.tipoCampo == 2:
            return self.questaonumero
        if self.tipoCampo == 3:
            return self.questaoescolha
    questaoTipo = property(questaoTipo)


#------------------------ Texto ------------------------#

class QuestaoTexto(models.Model):
    questao = models.OneToOneField(Questao,on_delete=models.CASCADE)
    subTipoCampo = models.IntegerField("Subtipo de Campo", choices=tipoTextoChoices)

    class Meta:
        verbose_name = "Questão Texto"
        verbose_name_plural = "Questões Texto"

#------------------------ Escolha ------------------------#

class QuestaoEscolha(models.Model):
    questao = models.OneToOneField(Questao,on_delete=models.CASCADE)
    subTipoCampo = models.IntegerField("Subtipo de Campo", choices=tipoEscolhaChoices)
    #Alternativas
    multipas = models.BooleanField("Multipla escolha", default=False)

class Alternativa(models.Model):
    questaoEscolha = models.ForeignKey("QuestaoEscolha", on_delete=models.SET_NULL, null=True)

    rotulo = models.CharField("Rotulo", max_length=1000)

#------------------------ Numero ------------------------#

class QuestaoNumero(models.Model):
    questao = models.OneToOneField(Questao,on_delete=models.CASCADE)
    subTipoCampo = models.IntegerField("Subtipo de Campo", choices=tipoNumeroChoices)
    #Numero
    numeroMinimo = models.FloatField("Numero Minimo",null=True,blank=True)
    numeroMaximo = models.FloatField("Numero Máximo",null=True,blank=True)

    def delete(self, using=None, keep_parents=False):
        self.questao.delete()
        return super(QuestaoNumero, self).delete(using=using, keep_parents=keep_parents)
        