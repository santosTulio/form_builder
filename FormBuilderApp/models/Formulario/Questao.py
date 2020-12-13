from django.db import models
from autoslug import AutoSlugField

#from FormBuilderApp.models.Questionario.TipoArquivo import TipoArquivo
from django.utils.text import slugify
from django.utils.timezone import now

from Utils import unique_slug

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
    *tipoEscolhaChoices,
    *tipoNumeroChoices,
    *tipoTextoChoices
]



class Questao(models.Model):
    secao = models.ForeignKey("Secao",on_delete=models.CASCADE)
    pergunta = models.CharField("Pergunta",max_length=1000)
    obrigatorio = models.BooleanField(default=True)
    subTipoCampo = models.IntegerField("Tipo de Campo", choices=tipos)
    posicao = models.FloatField("Posicao",default=0, blank=True)
    slug = AutoSlugField(populate_from='pergunta', unique=True)
    #Alternativas
    multiplas = models.BooleanField("Multipla escolha", default=False, blank=True)

    dataCriacao = models.DateTimeField("Data Criacao", editable=False, auto_now_add=True)
    dataUltimaAlteracao = models.DateTimeField("Data da Ultima Alteração", editable=False, auto_now=True)

    #Numero
    numeroMinimo = models.FloatField("Numero Minimo",default=0, null=True,blank=True)
    numeroMaximo = models.FloatField("Numero Máximo",default=10000000, null=True,blank=True)

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
        ordering = ["posicao","id"]
    def __str__(self):
        return self.pergunta
    def save(self,*args,**kwargs):
        if self.pk is None:
            if hasattr(self.secao,'questao_set'):
                last=self.secao.questao_set.last()
                self.posicao = last.posicao + 1 if last else 0
        return super(Questao, self).save(*args,**kwargs)

    def getFormulario(self):
        return self.secao.formulario
    formulario = property(getFormulario)

    def praCima(self):
        if self.pk is None:
            raise Exception(f'Error: "{self}" não é um objeto no banco de dados')
        anterior = self.secao.questao_set.filter(posicao__lt=self.posicao).first()
        if anterior is None:
            ant_secao = self.formulario.secao_set.filter(posicao__lt=self.secao.posicao).last()
            if ant_secao is None:
                raise Exception(f'Error: Não é possivel subir mais')
            self.secao = ant_secao
            if hasattr(self.secao, 'questao_set'):
                last = self.secao.questao_set.last()
                self.posicao = last.posicao + 1 if last else 0
            else:
                self.posicao = 0
        else:
            anterior.posicao, self.posicao = self.posicao, anterior.posicao
            anterior.save()
        self.save()

    def praBaixo(self):
        if self.pk is None:
            raise Exception(f'Error: "{self}" não é um objeto no banco de dados')

        proximo = self.secao.questao_set.filter(posicao__gt=self.posicao).first()
        if proximo is None:
            prox_secao = self.formulario.secao_set.filter(posicao__gt=self.secao.posicao).first()
            if prox_secao is None:
                raise Exception(f'Error: Não é possivel subir mais')
            self.secao = prox_secao
            if hasattr(self.secao, 'questao_set'):
                first = self.secao.questao_set.first()
                self.posicao = first.posicao - 1 if first else 0
            else:
                self.posicao = 0
        else:
            proximo.posicao,self.posicao = self.posicao,proximo.posicao
            proximo.save()
        self.save()

class Alternativa(models.Model):
    questao = models.ForeignKey("Questao", on_delete=models.CASCADE)
    rotulo = models.CharField("Rotulo", max_length=1000)
    posicao = models.FloatField("Posicao",default=0, blank=True)
    slug = AutoSlugField(unique=True,populate_from='questao')

    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"
        ordering = ["posicao","id"]

    def save(self,*args,**kwargs):
        if self.pk is None:
            if hasattr(self.questao,'alternativa_set'):
                last=self.questao.alternativa_set.last()
                self.posicao = last.posicao + 1 if last else 0
            if self.rotulo is None or self.rotulo=='':
                self.rotulo = 'Opção'+ f' {self.questao.alternativa_set.count() + 1}' if hasattr(self.questao, 'alternativa_set') else ' 1'
        return super(Alternativa, self).save(*args,**kwargs)

    def __str__(self):
        return self.rotulo

    def praCima(self):
        if self.pk is None:
            raise Exception(f'Error: "{self}" não é um objeto no banco de dados')
        anterior = self.questao.alternativa_set.filter(posicao__lt=self.posicao).last()
        if anterior is None:
            raise Exception(f'Error: Não é possivel subir mais')
        else:
            anterior.posicao, self.posicao = self.posicao, anterior.posicao
            anterior.save()
            self.save()

    def praBaixo(self):
        if self.pk is None:
            raise Exception(f'Error: "{self}" não é um objeto no banco de dados')
        proximo = self.questao.alternativa_set.filter(posicao__gt=self.posicao).first()
        if proximo is None:
            raise Exception(f'Error: Não é possivel subir mais')
        else:
            proximo.posicao,self.posicao = self.posicao,proximo.posicao
            proximo.save()
            self.save()

    def formulario(self):
        return self.questao.secao.formulario
    formulario.short_description = "Formulário"