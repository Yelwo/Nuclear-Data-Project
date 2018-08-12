from django.test import TestCase

from radiations.models import Radiation, germs_for_radiations


class RadiationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Radiation.objects.create(name='β-')

    def test_germ(self):
        rad = Radiation.objects.get(id=1)
        name, germ = rad.name, rad.germ
        self.assertEqual(germ, germs_for_radiations[name])