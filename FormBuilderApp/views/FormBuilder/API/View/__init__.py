from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView
from rest_framework import serializers

from FormBuilderApp.models.Questionario import Secao
from .QuestaoAPI import QuestaoAPI
from .SecaoAPI import SecaoAPIAdd

@login_required
def SecaoListCreate(request):
    print(request.GET)
    return serializers.serialize('json',{'data':Secao.objects.all()})