from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline

from .models import *


class AlternativaInline(admin.TabularInline):
    model = Alternativa
    fields = ['rotulo','posicao']
    extra = 1

@admin.register(Alternativa)
class AlternativaAdmin(admin.ModelAdmin):
    list_display = ['rotulo','questao','formulario']
    exclude = []

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    fields = ['secao', 'pergunta', 'subTipoCampo', 'obrigatorio', 'numeroMinimo','numeroMaximo','posicao']
    inlines = [AlternativaInline]


class AlternativaNestedInline(NestedTabularInline):
    model = Alternativa
    fields = ['rotulo','posicao']
    extra = 1

class QuestaoInline(NestedStackedInline):
    model = Questao
    fields = ['secao', 'pergunta', 'subTipoCampo', 'obrigatorio', 'numeroMinimo','numeroMaximo','posicao']
    radio_fields = {'subTipoCampo': admin.HORIZONTAL}
    inlines = [AlternativaNestedInline]
    extra = 1

@admin.register(Secao)
class SecaoAdmin(NestedModelAdmin):
    list_display = ['titulo', 'descricao', 'formulario', 'qtdQuestoes']
    fields = ['formulario', 'titulo', 'descricao', 'posicao']
    inlines = [QuestaoInline]
    pass

@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ['titulo','descricao','mensagemAgradecimento','aceitaResposta','unicaResposta','dataCriacao','ultimaAlteracao']
    exclude = []

class RespostaInline(admin.StackedInline):
    model = Resposta
    exclude = []
    extra = 1

@admin.register(Submissao)
class SubmissaoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'dataCriacao']
    exclude = []
    inlines = [RespostaInline]