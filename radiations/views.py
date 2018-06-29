from django.shortcuts import render
from django.views import generic
from .models import Radiation


class RadiationListView(generic.ListView):
    model = Radiation

class RadiationDetailView(generic.DetailView):
    model = Radiation
