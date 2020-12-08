from FormBuilderApp.models import QuestaoTexto, QuestaoNumero, QuestaoEscolha, Alternativa, Questao, Secao, NUMERO, \
    TEXTO, ESCOLHAS, INTEIRO, RESPOSTA_CURTA
from rest_framework import serializers

class QuestaoSerializer(serializers.ModelSerializer):
    subTipo = serializers.SerializerMethodField()

    class Meta:
        model = Questao
        fields='__all__'

    def validate(self, attrs):
        if attrs.get('secao') and attrs.get('pergunta') and attrs.get('posicao') \
                and attrs.get('subTipo') and attrs.get('tipoCampo'):
            return attrs
        raise serializers.ValidationError("finish must occur after start")

    def create(self, validated_data):
        questaoSub = validated_data.pop('subTipo',{})
        tipoCampo = validated_data['tipoCampo']
        questao = Questao(
            secao = validated_data['secao'],
            tipoCampo= tipoCampo,
            pergunta = validated_data.get('pergunta',"Pergunta"),
            obrigatorio=validated_data.get('obrigatorio',False)
        )
        questao.save()
        print('create',tipoCampo)
        if tipoCampo == NUMERO:
            return QuestaoNumero(
                questao = questao,
                subTipoCampo = questaoSub.get('subTipoCampo',INTEIRO),
                numeroMinimo = questaoSub.get('numeroMinimo',None),
                numeroMaximo = questaoSub.get('numeroMaximo',None),
                )
        elif tipoCampo == TEXTO:
            return QuestaoTexto(
                    questao = questao,
                    subTipoCampo = questaoSub.get('subTipoCampo',RESPOSTA_CURTA),
                )
        elif tipoCampo == ESCOLHAS:
            return QuestaoEscolha(
                questao=questao,
                subTipoCampo=questaoSub.get('subTipoCampo', RESPOSTA_CURTA),
            )

    def get_subTipo(self, obj):
        if obj.tipoCampo ==NUMERO:
            return QuestaoNumeroSerializer(obj.questaonumero).data
        if obj.tipoCampo == TEXTO:
            return QuestaoTextoSerializer(obj.questaotexto).data
        if obj.tipoCampo == ESCOLHAS:
            return QuestaoEscolhaSerializer(obj.questaoescolha).data

class QuestaoNumeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestaoNumero
        fields='__all__'

class QuestaoTextoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestaoTexto
        fields='__all__'

class QuestaoEscolhaSerializer(serializers.ModelSerializer):
    alternativas = serializers.SerializerMethodField()

    class Meta:
        model = QuestaoEscolha
        fields='__all__'

    def get_alternativa(self,obj):
        return obj.alternativa_set

class AlternativasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields='__all__'


class SecaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secao
        fields = '__all__'


class CreateQuestaoNumeroSerializer(serializers.ModelSerializer):
    pergunta = serializers.SerializerMethodField()
    placeholder = serializers.SerializerMethodField()
    secao = serializers.SerializerMethodField()
    posicao = serializers.SerializerMethodField()

    class Meta:
        model = QuestaoNumero
        fields='__all__'

    def get_pergunta(self, obj):
        return obj.questao.pergunta
    def get_placeholder(self,obj):
        return obj.questao.placeholder
    def get_posicao(self,obj):
        return obj.questao.posicao
    def get_secao(self,obj):
        return obj.questao.secao

class UpdateQuestaoNumeroSerializer(CreateQuestaoNumeroSerializer):
    id = serializers.SerializerMethodField()
    def get_id(self, obj):
        return obj.questao.id


