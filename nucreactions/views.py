from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Reaction
from .forms import AddReaction
from db_scripts.set_nuc_reaction_data import get_object


class ReactionListView(generic.ListView):
    model = Reaction
    paginate_by = 20

    def get_queryset(self):
        qs = Reaction.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(_product_one__isotope__name__contains=query) |
                Q(_product_one__elementary_particle__name__contains=query) |
                Q(_product_one__radiation__name__contains=query) |
                Q(_product_two__isotope__name__contains=query) |
                Q(_product_two__elementary_particle__name__contains=query) |
                Q(_product_two__radiation__name__contains=query) |
                Q(_product_three__isotope__name__contains=query) |
                Q(_product_three__elementary_particle__name__contains=query) |
                Q(_product_three__radiation__name__contains=query) |
                Q(_target__isotope__name__contains=query) |
                Q(_target__elementary_particle__name__contains=query) |
                Q(_target__radiation__name__contains=query) |
                Q(_projectile__isotope__name__contains=query) |
                Q(_projectile__elementary_particle__name__contains=query) |
                Q(_projectile__radiation__name__contains=query)

            )
        return qs


class ReactionDetailView(generic.DetailView):
    model = Reaction
    paginate_by = 50


@login_required
def add_reactions(request):
    form = AddReaction(request.POST)
    if form.is_valid():
        target = get_object(form.cleaned_data['target'])
        projectile = get_object(form.cleaned_data['projectile'])
        product_one = get_object(form.cleaned_data['product_one'])
        product_two = get_object(form.cleaned_data['product_two'])
        product_three = get_object(form.cleaned_data['product_three'])
        reaction = Reaction(_target=target,
                            _projectile=projectile,
                            _product_one=product_one,
                            _product_two=product_two,
                            _product_three=product_three)
        reaction.save()
    return render(request, 'nucreactions/add_reactions.html', {'form': form})


