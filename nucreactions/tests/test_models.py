from django.test import TestCase
from nucreactions.models import Reaction
from db_scripts.set_nuc_reaction_data import get_object
from isotopes.models import Isotope


class NucReactionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.iso1 = Isotope.objects.create(name='Bi209',
                                          z_number=83,
                                          a_number=209,
                                          natural_abund=1.0,
                                          binding_energy=1640.22697345397,
                                          atomic_mass=208.980399068,
                                          child_id=None,
                                          iso_type='S')

        cls.iso2 = Isotope.objects.create(name='H2',
                                          z_number=1,
                                          a_number=2,
                                          natural_abund=0.000115,
                                          binding_energy=2.22455145236997,
                                          atomic_mass=2.01410177812,
                                          child_id=None,
                                          iso_type='S')

        cls.iso3 = Isotope.objects.create(name='Pb208',
                                          z_number=82,
                                          a_number=208,
                                          natural_abund=0.524,
                                          binding_energy=1636.42792580379,
                                          atomic_mass=207.976652481,
                                          child_id=None,
                                          iso_type='S')

        cls.iso4 = Isotope.objects.create(name='He3',
                                          z_number=2,
                                          a_number=3,
                                          natural_abund=1.34e-06,
                                          binding_energy=7.718028816554527,
                                          atomic_mass=3.01602932008,
                                          child_id=None,
                                          iso_type='S')

        cls.react = Reaction.objects.create(
            _target=get_object(cls.iso1.name),
            _projectile=get_object(cls.iso2.name),
            _product_one=get_object(cls.iso3.name),
            _product_two=get_object(cls.iso4.name),
            _product_three=get_object(None)
        )

    def test_germ(self):
        germ = Reaction.objects.get(id=1).germ
        self.assertEqual(germ, (2, 3))

    def test_germ_view(self):
        germ_view = Reaction.objects.get(id=1).germ_view
        self.assertEqual(germ_view, '3n2p')

    def test_germ_shell_view(self):
        germ_shell_view = Reaction.objects.get(id=1).germ_shell_view
        self.assertEqual(germ_shell_view, 'G(3n2p)124n82p')

    def test_reaction_view(self):
        reaction_view = Reaction.objects.get(id=1).reaction_view
        self.assertEqual(reaction_view, 'G(p)n + G(np)125n82p → G(3n2p)124n82p → G(2n)124n82p + G(n)2p')
