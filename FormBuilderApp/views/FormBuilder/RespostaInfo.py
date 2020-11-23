from django.views.generic import DetailView

from FormBuilderApp.models import Questionario


class RespostaDetailView(DetailView):
    model = Questionario