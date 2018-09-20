from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import AddIsotope
from .models import Isotope

# Create your views here.


@login_required
def add_isotopes(request):
    form = AddIsotope(request.POST)
    if form.is_valid():
        isotope = form.save(commit=False)
        isotope.save()
    return render(request, 'isotopes/add_isotopes.html', {'form': form})


class IsotopeListView(generic.ListView):
    model = Isotope
    paginate_by = 20

    def get_queryset(self):
        qs = Isotope.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(name__contains=query)
        return qs


class IsotopeDetailView(generic.DetailView):
    model = Isotope
