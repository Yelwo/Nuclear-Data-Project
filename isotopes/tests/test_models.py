from django.test import TestCase

# Create your tests here.

from isotopes.models import Isotope


class IsotopeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Isotope.object.create(name='U235',
                              z_number=92,
                              a_number=235,
                              natural_abund=0.007204,
                              binding_energy=1783.86105944496,
                              atomic_mass=235.043930131)

    def test_decay_mode(self):
        isotope = Isotope.objects.get(id=1)
        decay_mode = isotope.decay_mode
        self.assertEqual()