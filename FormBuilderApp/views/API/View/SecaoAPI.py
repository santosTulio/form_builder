from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from FormBuilderApp.models import Formulario
from FormBuilderApp.models.Formulario import Secao
from FormBuilderApp.views.API.Serializer import SecaoSerializer

class SecaoAPI(
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView
                  ):
    queryset = Secao.objects.all()
    serializer_class = SecaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super(SecaoAPI, self).get_queryset().filter(formulario__id=self.kwargs['formulario'], formulario__criador__username=self.request.user)

    def post(self, request, *args, **kwargs):
        formulario = get_object_or_404(Formulario, id=kwargs['formulario'])
        serializer = SecaoSerializer(data={
                        'formulario':formulario.id
                    })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        return self.destroy( request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.GET.get('action'):
            if request.GET.get('action')=='UP':
                instance.praCima()
            elif request.GET.get('action')=='DOWN':
                instance.praBaixo()
            elif request.GET.get('action')=='TRASH':
                instance.delete()
                return Response({})

        titulo = request.data.pop('titulo',None)
        descricao = request.data.pop('descricao',None)
        data = dict()
        if titulo is not None and instance.titulo!=titulo and titulo!='':
            data.update({
                'titulo':titulo
            })
        if descricao is not None and instance.descricao!=descricao:
            data.update({
                'descricao':descricao
            })

        serializer = SecaoSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)