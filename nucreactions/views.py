from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Reaction
from .forms import AddReaction
from db_scripts.set_nuc_reaction_data import get_object


class ReactionListView(generic.ListView):
    model = Reaction
    paginate_by = 20


class ReactionDetailView(generic.DetailView):
    model = Reaction
    paginate_by = 50


@login_required
def addreactions(request):
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
    return render(request, 'nucreactions/addreactions.html', {'form': form})


