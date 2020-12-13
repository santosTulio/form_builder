import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import View, ListView, DeleteView, DetailView
from FormBuilderApp.models import Submissao, Formulario, Questao, Resposta, LISTA_SUSPENSA, OPCOES, RESPOSTA_CURTA, \
    RESPOSTA_LONGA, DECIMAL, INTEIRO


class SubmissaoCreateView(LoginRequiredMixin,View):

    template_status_submit = 'submissao/StatusSubmissao.html'

    def get(self,request, *args, **kwargs):
        formulario = get_object_or_404(Formulario, slug=kwargs['slug'])
        if formulario.aceitaResposta and formulario.questoes.count() > 0:
            if hasattr(formulario,'submissao_set') and formulario.unicaResposta:
                if formulario.submissao_set.filter(proprietarioResposta=self.request.user).count()>0:
                    return render(request, self.template_status_submit,
                                  {'formulario': formulario, 'user': self.request.user, 'status': 'ALREADY_ANSWERED'})
            return render(request, 'formbuilder/Formulario.html', {'formulario': formulario, 'status':'ACCEEPT'})
        return render(request, self.template_status_submit,
                   {'formulario': formulario, 'user': self.request.user, 'status': 'NOT_ACCEPTING'})

    def valida(self,request, *args,**kwargs):
        formulario = get_object_or_404(Formulario, slug=kwargs['slug'])

        submissao = Submissao(proprietarioResposta=self.request.user, formulario=formulario)
        status = submissao.checkSubmissao()
        response = dict({'submissao':submissao})

        if status == 'ALREADY_ANSWERED':
            submissao = Submissao.objects.filter(proprietarioResposta=self.request.user, formulario=formulario).order_by('-dataCriacao').first()
            response.update({'status':'ALREADY_ANSWERED','submissao':submissao,'formulario':formulario,'user':self.request.user})
            return response

        if status=='NOT_ACCEPTING':
            response.update({'status':'NOT_ACCEPTING','submissao':submissao,'formulario':formulario,'user':self.request.user})
            return response
        questoes = formulario.questoes
        if questoes.count()>0:
            respostasObject = dict({})
            # Esse primeiro for verifica as resposta e colhe elas,
            # caso haja algum erro ele emite uma Exception, consequentemente não salvando a submissão
            for questao in questoes.all():
                res = Resposta(questao=questao)
                if questao.subTipoCampo in [OPCOES, LISTA_SUSPENSA]:
                    escolhidas = []
                    if questao.multiplas:
                        for alternativa in questao.alternativa_set.all():
                            escolhida = request.POST.get(alternativa.slug)
                            if escolhida is not None:
                                escolhidas.append(alternativa)
                    else:
                        resposta = self.request.POST.get(questao.slug)
                        if resposta is not None:
                            for alternativa in questao.alternativa_set.all():
                                # escolhida = resposta.get(alternativa.slug)
                                if alternativa.slug == resposta:
                                    escolhidas.append(alternativa)
                                    break
                            if len(escolhidas) == 0 and questao.obrigatorio:
                                raise Exception('Pergunta com resposta obrigatoria. É necessario a escolha de pelo menos 1')
                        elif questao.obrigatorio:
                            raise Exception('Resposta não encontrada')

                    respostasObject.update({
                        questao.slug: {
                            'res': res,
                            'escolhas': escolhidas,
                            'tipo': 'ESCOLHA'
                        }
                    })
                elif questao.subTipoCampo in [RESPOSTA_CURTA, RESPOSTA_LONGA]:
                    resposta = self.request.POST.get(questao.slug)
                    if resposta is not None:
                        res.texto = resposta
                    elif questao.obrigatorio:
                        raise Exception('Resposta não encontrada')
                    respostasObject.update({
                        questao.slug: {
                            'res': res,
                            'tipo': 'TEXTO'
                        }
                    })
                elif questao.subTipoCampo in [INTEIRO, DECIMAL]:
                    resposta = self.request.POST.get(questao.slug)
                    if resposta is not None:
                        res.numero = float(resposta) #Salvamos tudo como float
                        if not res.checkNumber():
                            raise Exception('Numero fora dos parametros')
                    elif questao.obrigatorio:
                        raise Exception('Resposta não encontrada')
                    respostasObject.update({
                        questao.slug: {
                            'res': res,
                            'tipo': 'NUMERO'
                        }
                    })
            submissao.save()
            for _, item in respostasObject.items():
                item['res'].submissao = submissao
                item['res'].save()
                if item['tipo'] == 'ESCOLHA':
                    print(item['escolhas'])
                    for escolha in item['escolhas']:
                        item['res'].opcoes.add(escolha)
                    item['res'].save()
                    print(item['res'].resposta)

            response.update({'status': 'ACCEPT', 'submissao': submissao, 'formulario': formulario,
                             'user': self.request.user})
            return response
        response.update({'status': 'NOT_ACCEPTING', 'submissao': submissao, 'formulario': formulario,
                         'user': self.request.user})
        return response

    def post(self, request, *args, **kwargs):
        response = self.valida(request, *args, **kwargs)
        if response is None:
            response = {'status': 'ERROR', 'formulario': get_object_or_404(Formulario,kwargs['slug']),
                         'user': self.request.user}
        return render(request, self.template_status_submit,response)

class SubmissaoListView(LoginRequiredMixin, ListView):
    model = Submissao
    template_name = 'formbuilder/Respostas.html'
    context_object_name = 'submissoes'

    def get_queryset(self):
        return super(SubmissaoListView, self).get_queryset().filter(formulario__slug=self.kwargs['slug'], formulario__criador__username=self.request.user)
    
    def get(self,request,*args,**kwargs):
        if request.GET.get('exportar', None) == 'CSV':

            questoes = Questao.objects.filter(secao__formulario__slug=kwargs['slug'])
            submissoes = Submissao.objects.filter(formulario__slug=kwargs['slug'])
            rows = []
            row = []
            row.append(f'Nome Completo')
            row.append(f'Email')
            row.append(f'Data de Submissão')
            for questao in questoes:
                row.append(questao.slug)
            rows.append(row)
            for submissao in submissoes:
                row = []
                if submissao.proprietarioResposta:
                    row.append(f'{submissao.proprietarioResposta.get_full_name()}')
                    row.append(f'{submissao.proprietarioResposta.email}')
                else:
                    row.append(f'Usuario desconhecido')
                    row.append(f'Sem Email')
                row.append(f'{submissao.dataCriacao}')
                for questao in questoes:
                    resposta = submissao.resposta_set.filter(questao=questao).first()
                    if resposta is not None:
                        resposta = resposta.resposta
                        row.append(''.join(['[{}]']*len(resposta)).format(*resposta) if isinstance(resposta, list) else resposta)
                    else:
                        row.append('')
                rows.append(row)
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer,delimiter=';')
            response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                             content_type="text/csv")
            response['Content-Disposition'] = f'attachment; filename="Submissoes-{kwargs["slug"]}-{now().timestamp()}.csv"'
            return response
    
        return super(SubmissaoListView, self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissaoListView, self).get_context_data(**kwargs)
        formulario=get_object_or_404(Formulario, slug=self.kwargs['slug'])
        context.update({
            'formulario':formulario,
            'listando':True
        })
        return context

class SubmissaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Submissao
    template_name = 'formbuilder/DeletarSubmissao.html'
    context_object_name = 'submissao'
    success_url = reverse_lazy('formbuilder:dashboard')

    def get_queryset(self):
        return super(SubmissaoDeleteView, self).get_queryset().filter(formulario__slug=self.kwargs['slug'],
                                                                    formulario__criador__username=self.request.user)
    def get_success_url(self):
        return reverse('formbuilder:listar-submissao',kwargs={'slug':self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(SubmissaoDeleteView, self).get_context_data(**kwargs)
        formulario = get_object_or_404(Formulario, slug=self.kwargs['slug'])
        context.update({
            'formulario': formulario
        })
        return context

class StatusSubmissaoView(LoginRequiredMixin, DetailView):
    model = Submissao
    template_name = 'submissao/StatusSubmissao.html'

    def get_context_data(self, **kwargs):
        context = super(StatusSubmissaoView, self).get_context_data(**kwargs)
        print(kwargs)
        if self.kwargs.get('status') == 'success':
            context.update({
                'success':True
            })
        else:
            context.update({
                'error': True
            })
        return context

class Echo:
    def write(self, value):
        return value