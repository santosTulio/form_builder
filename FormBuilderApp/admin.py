from django.contrib import admin

# Register your models here.

from .models import *
class QuestaoNumeroInline(admin.StackedInline):
    model = QuestaoNumero
class QuestaoTextoInline(admin.StackedInline):
    model = QuestaoTexto


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    inlines = [QuestaoNumeroInline,QuestaoTextoInline]
    pass
@admin.register(TipoArquivo)
class TipoArquivoAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestaoEscolha)
class QuestaoAlternativaAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestaoUpload)
class QuestaoUploadAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestaoTempo)
class QuestaoTempoAdmin(admin.ModelAdmin):
    pass