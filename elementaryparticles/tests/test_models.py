from django.test import TestCase

from elementaryparticles.models import ElementaryParticle, germs_for_elementaryparticles


class ElementaryParticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ElementaryParticle.objects.create(name='p', mass=938.279)

    def test_germ(self):
        elem = ElementaryParticle.objects.get(id=1)
        name, germ = elem.name, elem.germ
        self.assertEqual(germ, germs_for_elementaryparticles[name])
