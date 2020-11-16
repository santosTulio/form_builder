from django.db import models

from FormBuilderApp.models.Questionario.Resposta import Resposta


class RespostaDuracao(Resposta):
    duracao = models.DurationField("Duração")
    class Meta:
        verbose_name = "Resposta de Duração"
        verbose_name_plural = "Respostas de Duração"

class RespostaHorario(Resposta):
    horario = models.TimeField("Horário")
    class Meta:
        verbose_name = "Resposta de Horario"
        verbose_name_plural = "Respostas de Horario"

class RespostaDataTime(Resposta):
    data = models.DateTimeField("Data\Tempo")
    class Meta:
        verbose_name = "Resposta de Data\Tempo"
        verbose_name_plural = "Respostas de Data\Tempo"