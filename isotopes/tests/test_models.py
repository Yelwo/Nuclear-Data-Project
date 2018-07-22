from django.test import TestCase

# Create your tests here.

from isotopes.models import Isotope


class IsotopeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Isotope.objects.create(name='U236',
                               z_number=90,
                               a_number=233,
                               natural_abund=0.0,
                               binding_energy=771.47012801421,
                               atomic_mass=233.041582278)

    def test_decay_mode(self):
        isotope = Isotope.objects.get(id=1)
        decay_mode = isotope.decay_mode()
        self.assertEqual(decay_mode, (0, 1))
