from django.db import models
from django.urls import reverse

germs_for_radiations = {'α':(0,0),'β-':(0,1),'β+':(1,0)}

# Create your models here.

class Radiation(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('radiations:radiation-detail', args = [str(self.id)])

    def _get_germ(self):
        return germs_for_radiations[self.name]

    germ = property(_get_germ)


