from django.contrib import admin
from .models import Isotope
from nucreactions.models import Reaction
from radiations.models import Radiation
from elementaryparticles.models import ElementaryParticle

# Register your models here.

admin.site.register(Isotope)
admin.site.register(ElementaryParticle)
admin.site.register(Radiation)
admin.site.register(Reaction)

