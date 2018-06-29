from django.db import models
from django.urls import reverse

germs_for_elementaryparticles = {'n':(0,1),'p':(1,0),'γ':(0,0)}

# Create your models here.

class ElementaryParticle(models.Model):

    name = models.CharField(max_length=10)
    mass = models.FloatField(default=0)

    @property
    def germ(self):
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('elementaryparticles:elementary-particle-detail', args = [str(self.id)])

    def _get_germ(self):
        return germs_for_elementaryparticles[self.name]

    germ = property(_get_germ)