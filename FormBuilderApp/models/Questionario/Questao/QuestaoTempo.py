from django.db import models

from FormBuilderApp.models import Questao

tipoTempo=[
    "Horário",
    "Duração",
    "Data",
    "Data/Tempo",
]

class QuestaoTempo(Questao, models.Model):
    tipoCampo = models.CharField("Tipo de Campo", max_length=100, choices=[(i,i) for i in tipoTempo])

    #Horário
    horarioMinimo = models.TimeField("Horário Minimo")
    horarioMaximo = models.TimeField("Horário Máximo")

    #Duração
    duracaoMinima = models.DurationField("Duração Minima")
    duracaoMaxima = models.DurationField("Duração Máxima")

    #Data - Tempo
    dataTempoMinima = models.DateTimeField("Data/Tempo Minima")
    dataTempoMaxima = models.DateTimeField("Data/Tempo Máxima")