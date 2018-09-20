from django.views import generic
from .models import ElementaryParticle


class ElementaryParticleListView(generic.ListView):
    model = ElementaryParticle


class ElementaryParticleDetailView(generic.DetailView):
    model = ElementaryParticle


