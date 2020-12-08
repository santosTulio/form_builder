"""FormBuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
#from .views.FormBuilder.API.View.QuestaoAPI import CreateQuestaoNumeroView
from .views.FormBuilder.API.View import *
urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('', Dashboard.as_view(),name='dashboard'),
    path('myforms/', MeusFormularioView.as_view(),name='meus_formularios'),

    path('createforms/', PerguntaView.as_view(), name='criar_formulario'),
    path('form/<int:pk>/questions', PerguntaView.as_view(), name='formulario-perguntas'),
    path('form/<int:pk>/answer', RespostaView.as_view(), name='formulario-respostas'),

    path('form/<int:questionario>/questions/add/section/', SecaoAPIAdd.as_view(), name='questao-api'),
    path('form/<int:questionario>/questions/update/section/<int:pk>', SecaoAPIAdd.as_view(), name='questao-api'),
    path('form/<int:questionario>/questions/delete/section/<int:pk>', SecaoAPIAdd.as_view(), name='questao-api'),

    path('form/<int:questionario>/questions/add/question/', QuestaoAPI.as_view(), name='questao-api'),
    #path('form/<int:questionario>/questions/add/question/text', QuestaoAPI.as_view(), name='questao-api'),
    #path('form/<int:questionario>/questions/add/question/<int:secao>/choices', QuestaoAPI.as_view(), name='questao-api'),
    path('form/<int:questionario>/questions/update/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),
    path('form/<int:questionario>/questions/update/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),
    path('form/<int:questionario>/questions/update/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),
    path('form/<int:questionario>/questions/delete/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),

]
