from django.urls import path, include

from .views.FormBuilder.FormularioView import FormularioDeleteRedirectView
from .views.FormBuilder.FormularioView import FormularioSubmissaoViewer
from .views.FormBuilder.SubmissaoView import SubmissaoListView, SubmissaoDeleteView
from .views.FormBuilder.SubmissaoView import SubmissaoCreateView
from .views.FormBuilder.FormularioView import ConstrutorDeFormularioView
from .views.Dashboard.Dashboard import Dashboard

from FormBuilderApp.views.API.View.FormularioAPI import FormularioAPI
from FormBuilderApp.views.API.View.QuestaoAPI import QuestaoAPI
from FormBuilderApp.views.API.View.SecaoAPI import SecaoAPI
from FormBuilderApp.views.API.View.AlternativaAPI import AlternativaAPI

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('', Dashboard.as_view(),name='dashboard'),

    path('createforms/', ConstrutorDeFormularioView.as_view(), name='criar_formulario'),
    path('form/<int:pk>', ConstrutorDeFormularioView.as_view(), name='editar-formulario'),
    path('form/<slug>/view', FormularioSubmissaoViewer.as_view(), name='ver-formulario'),
    path('form/<int:pk>/deletar', FormularioDeleteRedirectView.as_view(), name='deletar-formulario'),
    path('form/<slug>/answer', SubmissaoListView.as_view(), name='listar-submissao'),
    path('form/<slug>/answer/<int:pk>/delete', SubmissaoDeleteView.as_view(), name='deletar-submissao'),
    #path('form/<slug>/answer/exportar-csv', some_streaming_csv_view, name='exportar-respostas'),

    path('submissao/<slug>', SubmissaoCreateView.as_view(), name='submissao'),

    path('api/form/<int:pk>/questions/', FormularioAPI.as_view(), name='api-update-formulario'),
    #path('<int:pk>/questions', FormularioView.as_view(), name='formulario'),

    path('api/form/<int:formulario>/questions/section/', SecaoAPI.as_view(), name='api-add-secao'),
    path('api/form/<int:formulario>/questions/section/<int:pk>', SecaoAPI.as_view(), name='api-update-delete-secao'),

    path('api/form/<int:formulario>/questions/question/', QuestaoAPI.as_view(), name='api-add-questao'),
    path('api/form/<int:formulario>/questions/question/<int:pk>', QuestaoAPI.as_view(), name='api-update-delete-questao'),
    path('api/form/<int:formulario>/questions/question/<int:questao>/choice/', AlternativaAPI.as_view(), name='api-add-alternativa'),
    path('api/form/<int:formulario>/questions/question/<int:questao>/choice/<int:pk>', AlternativaAPI.as_view(), name='api-update-delete-alternativa'),


    #path('form/<int:questionario>/questions/add/question/text', QuestaoAPI.as_view(), name='questao-api'),
    #path('form/<int:questionario>/questions/add/question/<int:secao>/choices', QuestaoAPI.as_view(), name='questao-api'),
    #path('form/<int:questionario>/questions/update/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),
    #path('form/<int:questionario>/questions/update/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),
    #path('form/<int:questionario>/questions/update/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),
    #path('form/<int:questionario>/questions/delete/question/<int:secao>/<int:questao>', QuestaoAPI.as_view(), name='questao-api'),

]
