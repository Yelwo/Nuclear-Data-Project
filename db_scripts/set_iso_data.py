from db_scripts import isotope_data as nd
from isotopes.models import Isotope

Isotope.objects.all().delete()


# ---------- Find isotope by its name
def find_iso(iso_name, iso_list):
    for iso in iso_list:
        if iso_name == iso.name:
            return iso


# ---------- Get stable isotopes
iso_list = []

for isotope in nd.nuc_data:
    if type(isotope) is nd.Stable:
        a = Isotope(name=isotope.name, iso_type = 'S', z_number=isotope.Z, a_number=isotope.A,
                    natural_abund=isotope.natural_abund, binding_energy=isotope.binding_energy,
                    atomic_mass=isotope.atomic_mass)
        a.save()
        iso_list.append(a)

# ---------- Get unstable isotopes
for isotope in nd.nuc_data:
    if type(isotope) is nd.Unstable:
        a = Isotope(name=isotope.name, iso_type = 'U', z_number=isotope.Z, a_number=isotope.A,
                    natural_abund=isotope.natural_abund, binding_energy=isotope.binding_energy,
                    atomic_mass=isotope.atomic_mass)
        a.save()
        iso_list.append(a)

# ---------- Set isotope children
for iso in iso_list:
    if iso.iso_type == 'U':
        print(iso.name)
        iso.child = find_iso(nd.find_iso_name(iso.name).child().name, iso_list)
        iso.save()

