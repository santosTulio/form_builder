import logging

from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, FormView

logger = logging.getLogger(__name__)
# Create your views here.
class Login(View):

    success_url = reverse_lazy('formbuilder:dashboard')

    def get(self,request):
        return render(request,'registration/login.html')

    def form_valid(self, form):
        login(self.request, form.get_user())
        next_path = self.request.GET.get('next', '')
        return HttpResponseRedirect(self.get_success_url()) if next_path != '' else HttpResponseRedirect(next_path)

    def post(self, request, *args, **kwargs):
        form = authenticate(request,*request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)