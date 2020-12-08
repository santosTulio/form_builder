from django.db import models

#from FormBuilderApp.models import Questionario


class Secao(models.Model):
    questionario = models.ForeignKey("Questionario", on_delete=models.CASCADE)

    titulo = models.CharField("Titulo", max_length=100)
    descricao = models.TextField("Descricao", blank=True, null=True)

    posicao = models.FloatField("Posição",default=0)

    ativo = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Seção"
        verbose_name_plural = "Seções"
        ordering = ["id", "posicao"]

    def save(self,*args,**kwargs):
        if self.titulo is None:
            count = 0
            if(hasattr(self.questionario,'secao_set')):
                count = self.questionario.secao_set.count()
            self.posicao = count + 1
            self.titulo = f'Seção {count+1}'
        return super(Secao, self).save(*args,**kwargs)