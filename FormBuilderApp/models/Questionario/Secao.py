from django.db import models

#from FormBuilderApp.models import Questionario


class Secao(models.Model):
    questionario = models.ForeignKey("Questionario", on_delete=models.SET_NULL,null=True)

    titulo = models.CharField("Titulo", max_length=100)
    descricao = models.TextField("Descricao", blank=True, null=True)

    posicao = models.FloatField("Posição",default=0)

    ativo = models.BooleanField()
    class Meta:
        verbose_name = "Seção"
        verbose_name_plural = "Seções"
        ordering = ["id", "posicao"]