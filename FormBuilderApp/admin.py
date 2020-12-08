from django.contrib import admin

# Register your models here.

from .models import *
class QuestaoNumeroInline(admin.StackedInline):
    model = QuestaoNumero
class QuestaoTextoInline(admin.StackedInline):
    model = QuestaoTexto


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    pass
@admin.register(QuestaoNumero)
class QuestaoNumeroAdmin(admin.ModelAdmin):
    pass
@admin.register(Secao)
class SecaoAdmin(admin.ModelAdmin):
    pass

@admin.register(Questionario)
class QuestionarioAdmin(admin.ModelAdmin):
    pass