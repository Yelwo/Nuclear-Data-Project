from django.test import TestCase

# Create your tests here.

from isotopes.models import Isotope

class IsotopeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Isotope.object.create()