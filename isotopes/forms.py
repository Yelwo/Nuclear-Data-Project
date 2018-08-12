from django import forms
from .models import Isotope


class AddIsotope(forms.ModelForm):

    child = forms.ModelChoiceField(queryset=Isotope.objects.all())

    class Meta:
        model = Isotope
        fields = ['name', 'z_number', 'a_number', 'natural_abund',
                  'binding_energy', 'atomic_mass','iso_type', 'child']
