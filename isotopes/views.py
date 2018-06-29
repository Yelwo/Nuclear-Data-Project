from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import AddIsotope
from .models import Isotope

# Create your views here.


@login_required
def addisotopes(request):
    form = AddIsotope(request.POST)
    if form.is_valid():
        isotope = form.save(commit=False)
        isotope.save()
    return render(request, 'isotopes/addisotopes.html', {'form': form})


class IsotopeListView(generic.ListView):
    model = Isotope


class IsotopeDetailView(generic.DetailView):
    model = Isotope
