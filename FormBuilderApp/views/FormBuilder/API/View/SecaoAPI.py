from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from FormBuilderApp.models import Questionario
from FormBuilderApp.models.Questionario import Secao
from FormBuilderApp.views.FormBuilder.API.Serializer import QuestaoSerializer


class SecaoSerializer(serializers.ModelSerializer):
    questoes = serializers.SerializerMethodField()

    class Meta:
        model = Secao
        fields='__all__'

    def validate(self, attrs):
        if attrs.get('questionario') and attrs.get('titulo') and attrs.get('posicao'):
            return attrs
        raise serializers.ValidationError("finish must occur after start")

    def get_questoes(self,obj):
        return QuestaoSerializer(obj.questao_set.all(), many=True).data

class SecaoAPIAdd(
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView
                  ):
    queryset = Secao.objects.all()
    serializer_class = SecaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super(SecaoAPIAdd, self).get_queryset().filter(questionario__id=self.kwargs['questionario'], questionario__criador__username=self.request.user)

    def get(self,  request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        questionario = get_object_or_404(Questionario, id=kwargs['questionario'])
        count = questionario.secao_set.count() if(hasattr(questionario,'secao_set')) else 0

        request.data.clear()
        request.data.update({'questionario':questionario.id,
                             'posicao':count+1,
                            'titulo':f'Seção {count+1}'
                            })
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy( request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        titulo = request.data.pop('titulo', instance.titulo)
        descricao = request.data.pop('descricao', instance.descricao)
        posicao = request.data.pop('posicao', instance.posicao)
        questionario = request.data.pop('questionario',  instance.questionario.id)

        request.data.clear()
        request.data.update({'questionario': questionario,
                             'posicao': posicao,
                             'titulo': titulo,
                             'descricao':descricao
                             })
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)