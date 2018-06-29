from django.db import models
from django.urls import reverse
import django_tables2 as tables
import math

# ---------- Constants
MASS_UNIT = 931.4940954 # MeV
PROTON_MASS = 1.00727647 # u
NEUTRON_MASS = 1.00866490 # u
H = 4.135667662 # 10^(-15) * eV * s
C = 299792458 # m/s
E_SQUARED = 1.4396
E = 4.80296

# ---------- Add two tuples
def myAdd(x,y):
    return tuple(map(sum,zip(x,y)))

# ---------- Find garland occupation number
def find_number_of_monads(first_shell_size):
    i = 2
    result = first_shell_size
    while result < 1:
        result = i * first_shell_size
        if(result < 1):
            i += 2
    if(result - 1 > 1 - (first_shell_size*(i-2))):
        result = first_shell_size*(i-2)
    return (result,i)

# ---------- Isotope data tables


class NucStructureTable(tables.Table):
    shell_number = tables.Column()
    shell_occupation = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'


class NucShellSizesTable(tables.Table):
    shell_number = tables.Column()
    shell_radius = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'


class NucShellEnergyTable(tables.Table):
    shell_number = tables.Column()
    binding_energy = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'


class NucShellDipoleMomentTable(tables.Table):
    shell_number = tables.Column()
    dipole_moment = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'


# ---------- Model of isotope
class Isotope(models.Model):

    name = models.CharField(max_length=10)
    z_number = models.IntegerField(default=0)
    a_number = models.IntegerField(default=0)
    natural_abund = models.FloatField(default=0)
    binding_energy = models.FloatField(default=0)
    atomic_mass = models.FloatField(default=0)
    child = models.ForeignKey('Isotope', on_delete=models.CASCADE, null=True)

    ISO_TYPES =(
        ('S', 'Stable'),
        ('U', 'Unstable'),
    )

    iso_type = models.CharField(max_length=1, choices=ISO_TYPES, null=True)

    # ---------- Calculate single step of decay chain
    def decay_mode(self):
        x = self.child
        if (x.z_number < self.z_number):
            if (x.a_number == self.a_number - 4):
                return (0, 0)
            else:
                return (self.z_number - x.z_number, 0)
        elif (x.z_number > self.z_number):
            return (0, x.z_number - self.z_number)
        else:
            return (0, 1)

    # ---------- Calculate germ for both, stable and unstable isotopes
    def _get_germ(self):
        if self.iso_type == 'S':
            if (self.binding_energy > (PROTON_MASS * MASS_UNIT)):
                if (self.z_number % 2 == 0):
                    my_tuple = (0, 2)
                else:
                    my_tuple = (1, 1)
            else:
                if (self.z_number % 2 == 0):
                    my_tuple = (0, 1)
                else:
                    my_tuple = (1, 0)

            return my_tuple
        else:
            i = self
            decay_sum = (0, 0)
            while (i.iso_type != 'S'):
                decay_sum = myAdd(decay_sum, i.decay_mode())
                i = i.child

            germ_sum = myAdd((i.germ[0], i.germ[1]), decay_sum)
            if ((self.z_number - germ_sum[0]) % 2 != 0):
                my_tuple = myAdd(germ_sum, (1, 0))
            else:
                my_tuple = germ_sum

            return my_tuple

    germ = property(_get_germ)

    # ---------- Create germ display view
    def _get_germ_view(self):
        germ = self.germ
        germ_view = ""
        if(germ[1] > 0):
            if(germ[1] == 1):
                germ_view += 'n'
            else:
                germ_view += str(germ[1]) + 'n'
        if(germ[0] > 0):
            if(germ[0] == 1):
                germ_view += 'p'
            else:
                germ_view += str(germ[0]) + 'p'

        return germ_view

    germ_view = property(_get_germ_view)

    # ---------- Create shell-germ display view

    def _get_germ_shell_view(self):
        protons = self.z_number - self.germ[0]
        neutrons = self.a_number - self.z_number - self.germ[1]

        def display(nucleons,n_or_p):
            if nucleons > 1: return str(nucleons) + n_or_p
            elif nucleons == 1: return n_or_p
            else: return ""

        return "G(" + self.germ_view + ")" + display(neutrons,"n") + display(protons,"p")

    germ_shell_view = property(_get_germ_shell_view)


    # ---------- Get isotope id
    def _get_iso_id(self):
        my_id = ''
        for i in range(3 - len(str(self.z_number))):
            my_id += '0'
        my_id += str(self.z_number)
        for i in range(4 - len(str(self.a_number))):
            my_id += '0'
        my_id += str(self.a_number)
        return my_id

    iso_id = property(_get_iso_id)

    # --------- Calculate nuclear shell structure
    def _get_nuc_structure(self):
        protons_left = self.z_number - self.germ[0]
        neutrons_left = self.a_number - self.z_number - self.germ[1]
        max_structure = [6,12,8,24,24,12,30,24,24,8,24,48,6,48]
        my_structure = []
        i = 0

        if (self.germ[0] >= self.germ[1]):
            last = 0
        else:
            last = 1

        while (protons_left > 0) | (neutrons_left > 0):
            if(((last == 0) & (neutrons_left > 0)) | (protons_left == 0)):
                if neutrons_left > max_structure[i]:
                    my_structure.append((0,max_structure[i]))
                    neutrons_left -= max_structure[i]
                    i += 1
                    last = 1
                else:
                    my_structure.append((0,neutrons_left))
                    neutrons_left = 0
                    i += 1
                    last = 1
            elif(last == 1 ) | (neutrons_left == 0):
                if protons_left > max_structure[i]:
                    my_structure.append((max_structure[i],0))
                    protons_left -= max_structure[i]
                    i += 1
                    last = 0
                else:
                    my_structure.append((protons_left,0))
                    protons_left = 0
                    i += 1
                    last = 0

        return my_structure


    nuc_structure = property(_get_nuc_structure)

    # ---------- Create nuclear shell structure table
    def _get_nuc_structure_table(self):
        my_structure = self.nuc_structure
        table = []

        for value in my_structure:
            if (value[0] != 0) or (value[1] != 0):
                if value[0] == 0:
                    table.append(str(value[1]) + 'n')
                else:
                    table.append(str(value[0]) + 'p')

        data = []

        for shell_number, shell in enumerate(table):
            data.append({'shell_number': shell_number + 1, 'shell_occupation': shell})

        return NucStructureTable(data)

    nuc_structure_table = property(_get_nuc_structure_table)

    # ---------- Get shell sizes
    def _get_nuc_shell_sizes(self):
        if(self.binding_energy == 0): return []
        A = [1,2,3,4,5,6,8,9,10,11,12,13,15,16,17]
        my_structure = self.nuc_structure
        shell_sizes = []
        my_sum = 0

        for i,shell in enumerate(my_structure):
            my_sum += (shell[0] + shell[1])/math.sqrt(A[i])

        for i,shell in enumerate(my_structure):
            if(i == 0):
                shell_sizes.append((1/2) * (E_SQUARED/self.binding_energy)* my_sum)
                monads = find_number_of_monads(shell_sizes[0])
                shell_sizes[0] = monads[0]
                monads_number = monads[1]
            else:
                shell_sizes.append(math.sqrt(A[i]) * shell_sizes[0])

        return (shell_sizes,monads_number)

    nuc_shell_sizes = property(_get_nuc_shell_sizes)

    def _get_number_of_monads(self):
        monads = self.nuc_shell_sizes[1]
        return monads

    number_of_monads = property(_get_number_of_monads)

    # ---------- Create shell sizes table
    def _get_nuc_shell_sizes_table(self):
        shell_sizes = self.nuc_shell_sizes[0]
        table = []

        for i, shell in enumerate(shell_sizes):
            table.append({'shell_number': i + 1 , 'shell_radius' : format(shell, '.5g')})

        return NucShellSizesTable(table)

    nuc_shell_sizes_table = property(_get_nuc_shell_sizes_table)

    # ---------- Create shell binding energy table
    def _get_nuc_shell_binding_energy_table(self):
        shell_sizes = self.nuc_shell_sizes[0]
        table = []
        for i, shell in enumerate(shell_sizes):
            table.append({'shell_number': i + 1, 'binding_energy': format(((1/2) * E_SQUARED * self.number_of_monads)/shell_sizes[i],'.5g')})

        return NucShellEnergyTable(table)

    nuc_shell_binding_energy_table = property(_get_nuc_shell_binding_energy_table)

    # ---------- Create shell dipole moment table
    def _get_nuc_shell_dipole_moment_table(self):
        shell_sizes = self.nuc_shell_sizes[0]
        table = []
        for i, shell in enumerate(shell_sizes):
            table.append({'shell_number': i + 1, 'dipole_moment': format(shell*E,'.5g')})

        return NucShellDipoleMomentTable(table)

    nuc_shell_dipole_moment_table = property(_get_nuc_shell_dipole_moment_table)

    # ---------- Get size of the nucleus
    def _get_nuc_size(self):
        return (H*10**(-21))*(C*100)/(self.atomic_mass*MASS_UNIT)

    nuc_size = property(_get_nuc_size)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('isotopes:isotope-detail', args = [str(self.id)])

    class Meta:
        ordering = ['z_number','a_number']
