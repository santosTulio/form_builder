
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from FormBuilderApp.models import Questao, Formulario, Secao, RESPOSTA_LONGA, \
    RESPOSTA_CURTA, OPCOES, LISTA_SUSPENSA, INTEIRO, DECIMAL, Alternativa
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
        return Questao.objects.filter(secao__formulario__id=self.kwargs['formulario'],secao__formulario__criador__username=self.request.user)

    def post(self, request, *args, **kwargs):
        formulario = get_object_or_404(Formulario, id=kwargs['formulario'])
        if formulario.secao_set.count()>0:
            secao  = formulario.secao_set.last()
        else:
            secao = Secao(formulario=formulario)
            secao.save()

        tipo = request.data.get('type', 'SHORT_ANSWER')

        questao = dict()
        if tipo in ['DECIMAL', 'INTEGER', 'RADIO', 'CHECKBOX', 'SELECT', 'SHORT_ANSWER', 'LONG_ANSWER']:
            questao.update({
                'subTipoCampo': {
                    'DECIMAL': DECIMAL,
                    'INTEGER': INTEIRO,
                    'RADIO': OPCOES,
                    'CHECKBOX': OPCOES,
                    'SELECT': LISTA_SUSPENSA,
                    'SHORT_ANSWER': RESPOSTA_CURTA,
                    'LONG_ANSWER': RESPOSTA_LONGA}[tipo]
            })
        else:
            raise Exception("Escolha pelo menos um tipo de questão")

        questao.update({
            'secao':secao.id,
            'pergunta': request.data.get('pergunta',"Pergunta"),
            'obrigatorio': request.data.get('obrigatorio', True)
        })
        serializer = QuestaoSerializer(data=questao, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        #Uma questao de alternativas deve ter pelo menos uma alternativa
        if tipo in ['RADIO', 'CHECKBOX', 'SELECT']:
            alternativa = Alternativa(questao=get_object_or_404(Questao,id=serializer.data.get('id')))
            alternativa.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def put(self,request, *args, **kwargs):

        instance = self.get_object()

        #Acoes mover deletar
        if request.GET.get('action'):
            if request.GET.get('action')=='UP':
                instance.praCima()
            elif request.GET.get('action')=='DOWN':
                instance.praBaixo()
            elif request.GET.get('action')=='TRASH':
                instance.delete()
                return Response({})

        subTipoCampo = instance.subTipoCampo
        data=dict()
        # TIPO TEXTO
        if subTipoCampo in [RESPOSTA_CURTA, RESPOSTA_LONGA]:
            long = request.data.get('long',None)
            if long is not  None and ((long == True and RESPOSTA_LONGA != subTipoCampo) or (long==False and RESPOSTA_CURTA !=subTipoCampo)):
                data.update({
                    'subTipoCampo': RESPOSTA_LONGA if long else RESPOSTA_CURTA
                })
        # TIPO ESCOLHA
        if subTipoCampo in [OPCOES, LISTA_SUSPENSA]:
            dropdownlist = request.data.get('dropdownlist', None)
            if dropdownlist is not None and ((dropdownlist == True and subTipoCampo!=LISTA_SUSPENSA) or (dropdownlist == False and subTipoCampo==LISTA_SUSPENSA)):
                data.update({
                    'subTipoCampo':LISTA_SUSPENSA if dropdownlist else OPCOES
                })

            multiple = request.data.get('multiple', None)
            if multiple is not None and ((multiple == True or multiple == False) and data.get('subTipoCampo',subTipoCampo)==OPCOES):
                data.update({
                    'multiplas':multiple
                })

        #TIPO NUMERO
        if subTipoCampo in [INTEIRO, DECIMAL]:
            decimal = request.data.get('decimal', None)
            if decimal is not None and ((decimal == True and DECIMAL != subTipoCampo) or (decimal == False and INTEIRO != subTipoCampo)):
                data.update({
                    'subTipoCampo': DECIMAL if decimal else INTEIRO
                })
            try:
                minimo = float(request.data.get('min', instance.numeroMinimo))
                maximo = float(request.data.get('max', instance.numeroMaximo))
                if maximo < minimo:
                    maximo=minimo
                data.update({
                    'numeroMinimo':minimo,
                    'numeroMaximo':maximo
                })
            except ValueError:
                pass

        obrigatorio = request.data.pop('required', None)
        if obrigatorio is not None and obrigatorio != instance.obrigatorio:
            data.update({
                'obrigatorio': obrigatorio
            })
        pergunta = request.data.pop('pergunta', None)
        if pergunta is not None and pergunta != instance.obrigatorio and pergunta!='':
            data.update({
                'pergunta':pergunta
            })

        #Validando os dados
        serializer = QuestaoSerializer(instance, data = data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)