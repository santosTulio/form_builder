
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from FormBuilderApp.models import Formulario
from ..Serializer import FormularioSerializer


class FormularioAPI(
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView
                    ):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super(FormularioAPI, self).get_queryset().filter(criador__username=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve( request, *args, **kwargs)

    def put(self,request, *args, **kwargs):
        instance = self.get_object()
        data = dict()
        titulo = request.data.pop('titulo', None)
        if titulo is not None and titulo != instance.titulo and titulo!='':
            data.update({
                'titulo': titulo
            })
        descricao = request.data.pop('descricao', None)
        if descricao is not None and descricao != instance.descricao:
            data.update({
                'descricao': descricao
            })
        aceitaResposta = request.data.pop('aceitaResposta', None)
        if aceitaResposta is not None and aceitaResposta != instance.aceitaResposta:
            data.update({
                'aceitaResposta': aceitaResposta
            })
        unicaResposta = request.data.pop('unicaResposta', None)
        if unicaResposta is not None and unicaResposta != instance.unicaResposta:
            data.update({
                'unicaResposta': unicaResposta
            })
        mensagemAgradecimento= request.data.pop('mensagemAgradecimento', None)
        if mensagemAgradecimento is not None and mensagemAgradecimento != instance.mensagemAgradecimento:
            data.update({
                'mensagemAgradecimento': mensagemAgradecimento
            })
        dataInicio = request.data.pop('dataInicio', None)
        if dataInicio is not None and dataInicio != instance.dataInicio:
            data.update({
                'dataInicio': dataInicio
            })

        dataTermino = request.data.pop('dataTermino', None)
        if dataTermino is not None and dataTermino != instance.dataTermino:
            data.update({
                'dataTermino': dataTermino
            })
        serializer = FormularioSerializer(instance, data = data, partial=True)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)