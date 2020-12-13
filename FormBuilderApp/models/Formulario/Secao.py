from django.db import models

#from FormBuilderApp.models import Questionario


class Secao(models.Model):
    formulario = models.ForeignKey("Formulario",verbose_name='Formulário', on_delete=models.CASCADE)

    titulo = models.CharField("Título", max_length=100,blank=True, null=True)
    descricao = models.TextField("Descrição", blank=True, null=True)

    posicao = models.FloatField("Posição",default=0,blank=True, null=True)

    dataCriacao = models.DateTimeField("Data Criaçãoo", editable=False, auto_now_add=True)
    dataUltimaAlteracao = models.DateTimeField("Data da Última Alteração", editable=False, auto_now=True)

    class Meta:
        verbose_name = "Seção"
        verbose_name_plural = "Seções"
        ordering = ["posicao",'id']

    def save(self,*args,**kwargs):
        if self.pk is None:
            if hasattr(self.formulario,'secao_set'):
                last = self.formulario.secao_set.last()
                self.posicao = last.posicao + 1 if last else 0
            else:
                self.posicao = 0
            if self.titulo is None or self.titulo=='':
                self.titulo = 'Secao'
        return super(Secao, self).save(*args,**kwargs)

    def praCima(self):
        if self.pk is None:
            raise Exception(f'Error: "{self}" não é um objeto no banco de dados')
        anterior = self.formulario.secao_set.filter(posicao__lt=self.posicao).first()
        if anterior is None:
            raise Exception(f'Error: Não é possivel subir mais')
        anterior.posicao, self.posicao = self.posicao, anterior.posicao
        anterior.save()
        self.save()

    def praBaixo(self):
        if self.pk is None:
            raise Exception(f'Error: "{self}" não é um objeto no banco de dados')

        proximo = self.formulario.secao_set.filter(posicao__gt=self.posicao).first()
        if proximo is None:
            raise Exception(f'Error: Não é possivel subir mais')

        proximo.posicao, self.posicao = self.posicao, proximo.posicao
        proximo.save()
        self.save()

    def ultimaAlteracao(self):
        questaoAlteradaRecentemente = self.questao_set.order_by('-dataUltimaAlteracao').first()
        if questaoAlteradaRecentemente:
            return max(self.dataUltimaAlteracao,questaoAlteradaRecentemente.dataUltimaAlteracao)
        return self.dataUltimaAlteracao if self.dataUltimaAlteracao else self.dataCriacao

    def getQuestoes(self):
        if hasattr(self,'questao_set'):
            return self.questao_set.all()
        return None

    def qtdQuestoes(self):
        questoes=self.getQuestoes()
        return questoes.count() if questoes else 0
    qtdQuestoes.short_description  = "Quantidade de Questões"