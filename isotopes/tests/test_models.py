from django.test import TestCase

from isotopes.models import Isotope


class IsotopeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Isotope.objects.create(name='Th232',
                               z_number=90,
                               a_number='232',
                               natural_abund=0.0,
                               binding_energy=1790.40650171588,
                               atomic_mass=236.04556821,
                               child_id=None,
                               iso_type='S')

        Isotope.objects.create(name='U236',
                               z_number=92,
                               a_number=236,
                               natural_abund=0.0,
                               binding_energy=1790.40650171588,
                               atomic_mass=236.04556821,
                               child_id=1,
                               iso_type='U')

    def test_decay_mode(self):
        isotope = Isotope.objects.get(id=2)
        decay_mode = isotope.decay_mode()
        self.assertEqual(decay_mode, (0, 0))

    def test_germ(self):
        isotope = Isotope.objects.get(id=2)
        germ = isotope.germ
        self.assertEqual(germ, (0, 2))

    def test_germ_view(self):
        isotope = Isotope.objects.get(id=2)
        germ_view = isotope.germ_view
        self.assertEqual(germ_view, '2n')

    def test_germ_shell_view(self):
        isotope = Isotope.objects.get(id=2)
        germ_shell_view = isotope.germ_shell_view
        self.assertEqual(germ_shell_view, 'G(2n)142n92p')

    def test_iso_id(self):
        isotope = Isotope.objects.get(id=2)
        iso_id = isotope.iso_id
        self.assertEqual(iso_id, '0920236')

    def test_nuc_structure(self):
        isotope = Isotope.objects.get(id=2)
        nuc_structure = isotope.nuc_structure
        self.assertEqual(nuc_structure, [(6, 0), (0, 12), (8, 0), (0, 24), (24, 0), (0, 12),
                                         (30, 0), (0, 24), (24, 0), (0, 8), (0, 24), (0, 38)])

    def test_nuc_shell_sizes(self):
        isotope = Isotope.objects.get(id=2)
        nuc_shell_sizes = isotope.nuc_shell_sizes
        self.assertEqual(nuc_shell_sizes, ([0.9701457767192287, 1.3719933149153138, 1.6803417760260757,
                                           1.9402915534384575, 2.1693119048285285, 2.37636212907817,
                                           2.7439866298306277, 2.910437330157686, 3.067870316825918,
                                           3.2176095333255885, 3.3606835520521514, 3.4979103426360174], 28))
