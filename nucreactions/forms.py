from django import forms
from .models import Reaction
from elementaryparticles.models import ElementaryParticle
from isotopes.models import Isotope
from radiations.models import Radiation

class AddReaction(forms.Form):

    target = forms.CharField(label='Reaction\'s target', max_length=10)
    projectile = forms.CharField(label='Reaction\'s projectile', max_length=10)
    product_one = forms.CharField(label='Reaction\'s product one', max_length=10)
    product_two = forms.CharField(label='Reaction\'s product two', max_length=10)
    product_three = forms.CharField(label='Reaction\'s product three', max_length=10, required=False)