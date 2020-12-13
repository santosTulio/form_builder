
from rest_framework import serializers

from FormBuilderApp.models import Alternativa, Questao, Secao, INTEIRO, RESPOSTA_CURTA, OPCOES, LISTA_SUSPENSA, \
    RESPOSTA_LONGA, DECIMAL, Formulario


class QuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questao
        exclude = ['posicao']

class QuestaoGetterSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    required = serializers.SerializerMethodField()
    params = serializers.SerializerMethodField()

    class Meta:
        model = Questao
        fields = ['id','pergunta','required','type','params']

    def get_params(self,obj):
        tipo = obj.subTipoCampo
        if tipo in [INTEIRO, DECIMAL]:
            return dict({
                'min':obj.numeroMinimo,
                'max':obj.numeroMaximo,
                'decimal':tipo == DECIMAL
            })
        elif tipo in [OPCOES, LISTA_SUSPENSA]:
            return dict({
                'choices': AlternativaSerializer(obj.alternativa_set, many=True).data,
                'multiple': tipo == OPCOES and obj.multiplas,
                'dropdownlist': tipo == LISTA_SUSPENSA
            })
        elif tipo in [RESPOSTA_LONGA,RESPOSTA_CURTA]:
            return dict({
                'long': tipo == RESPOSTA_LONGA
            })
        return None

    def get_required(self,obj):
        return obj.obrigatorio

    def get_type(self,obj):
         tipo=obj.subTipoCampo
         if tipo in [INTEIRO, DECIMAL]:
             return 'NUMBER'
         elif tipo in [OPCOES,LISTA_SUSPENSA]:
             return 'CHOICES'
         elif tipo in [RESPOSTA_LONGA, RESPOSTA_CURTA]:
             return 'TEXT'
         return None

class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields=['id','rotulo']

class SecaoSerializer(serializers.ModelSerializer):
    questoes = serializers.SerializerMethodField()

    class Meta:
        model = Secao
        exclude = ['posicao']

    def get_questoes(self,obj):
        return QuestaoGetterSerializer(obj.questao_set.all(), many=True).data

class FormularioSerializer(serializers.ModelSerializer):

    secoes = serializers.SerializerMethodField()
    class Meta:
        model=Formulario
        exclude = []

    def get_secoes(self,obj):
        if hasattr(obj, 'secao_set'):
            return SecaoSerializer(obj.secao_set.all(),many=True).data
