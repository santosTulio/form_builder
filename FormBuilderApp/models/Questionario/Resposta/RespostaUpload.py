import os

from django.db import models
from django.utils.text import slugify

from FormBuilderApp.models.Questionario.Resposta import Resposta


def content_file_name(obj, file):
    name, ext = os.path.splitext(file)
    return os.path.join( 'upload', '/'.join([obj.proprietarioResposta.id, obj.id]), slugify(name[:50])+ext )

class RespostaUpload(Resposta):
    file = models.FileField(upload_to=content_file_name)
    class Meta:
        verbose_name = "Resposta de Upload"
        verbose_name_plural = "Respostas de Upload"