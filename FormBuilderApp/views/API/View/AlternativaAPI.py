import numbers

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from FormBuilderApp.models import Questao, Formulario, Secao, RESPOSTA_LONGA, \
    RESPOSTA_CURTA, OPCOES, LISTA_SUSPENSA, INTEIRO, DECIMAL, Alternativa
from ..Serializer import QuestaoSerializer
from ..Serializer import AlternativaSerializer


class AlternativaAPI(
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView
                    ):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super(AlternativaAPI, self).get_queryset().filter(questao__secao__formulario__id=self.kwargs['formulario'], questao__id =self.kwargs['questao'] ,questao__secao__formulario__criador__username=self.request.user)

    def post(self, request, *args, **kwargs):
        formulario = get_object_or_404(Formulario, id=kwargs['formulario'])
        questao = get_object_or_404(Questao, id=kwargs['questao'], secao__formulario=formulario)
        alternativa = Alternativa(questao = questao)
        alternativa.save()
        serializer = AlternativaSerializer(alternativa)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def put(self,request, *args, **kwargs):

        instance = self.get_object()
        if request.GET.get('action'):
            if request.GET.get('action') == 'UP':
                instance.praCima()
            elif request.GET.get('action') == 'DOWN':
                instance.praBaixo()
            elif request.GET.get('action') == 'TRASH':
                if instance.questao.alternativa_set.count()>1:
                    instance.delete()
                    return Response({})
                else:
                    raise Exception('Não é possivel remover, necessario no minimo uma uma alternativa')

        data = dict()
        rotulo = request.data.pop('rotulo', None)
        if rotulo is not None and rotulo != instance.rotulo and rotulo!='':
            data.update({
                'rotulo': rotulo
            })

        serializer = AlternativaSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)