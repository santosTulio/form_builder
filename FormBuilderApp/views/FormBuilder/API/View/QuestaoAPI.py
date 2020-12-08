from django.shortcuts import get_object_or_404
from rest_framework import generics, status, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from FormBuilderApp.models import Questao, QuestaoNumero, NUMERO, INTEIRO, Questionario, Secao, RESPOSTA_LONGA, \
    RESPOSTA_CURTA, TEXTO, QuestaoTexto, QuestaoEscolha, ESCOLHAS, OPCOES
from ..Serializer import QuestaoSerializer

class QuestaoAPI(
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView
                    ):
    queryset = Questao.objects.all()
    serializer_class = QuestaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Questao.objects.filter(secao__questionario__criador__username=self.request.user)

    def post(self, request, *args, **kwargs):
        questionario = get_object_or_404(Questionario, id=kwargs['questionario'])
        if questionario.secao_set.count()>0:
            secao  = questionario.secao_set.last()
        else:
            secao = Secao(questionario=questionario)
            secao.save()
        count = secao.questao_set.count() if (hasattr(secao, 'questao_set')) else 0
        tipo = request.data.get('tipo', 'text')

        tipoCampo = TEXTO
        subTipoCampo = RESPOSTA_CURTA
        if tipo == 'number':
            tipoCampo = NUMERO
            subTipoCampo = INTEIRO
        elif tipo == 'text':
            tipoCampo = TEXTO
            subTipoCampo = RESPOSTA_CURTA
        elif tipo == 'choices':
            tipoCampo = ESCOLHAS
            subTipoCampo = OPCOES

        questao = Questao(
            secao=secao,
            tipoCampo=tipoCampo,
            pergunta=request.data.get('pergunta', "Pergunta"),
            obrigatorio=request.data.get('obrigatorio', False)
        )
        questao.save()
        print('create', tipoCampo)
        if tipoCampo == NUMERO:
            QuestaoNumero(
                questao=questao,
                subTipoCampo=subTipoCampo,
            ).save()
        elif tipoCampo == TEXTO:
            QuestaoTexto(
                questao=questao,
                subTipoCampo=subTipoCampo,
            ).save()
        elif tipoCampo == ESCOLHAS:
            QuestaoEscolha(
                questao=questao,
                subTipoCampo=subTipoCampo,
            ).save()

        serializer = QuestaoSerializer(questao)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def put(self,request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)