
# ---------- Imports
from pyne import data
from pyne import nucname


# ---------- Add two tuples
def myAdd(x,y):
    return tuple(map(sum,zip(x,y)))

# ---------- Constants
mass_unit = 931.4940954
proton_mass = 1.00727647
neutron_mass = 1.00866490

# ---------- List of isotope names
isotopes = []

for i in range(1,115):
    for j in range(1,250):
        try:
            isotopes.append(nucname.name((i*1000 + j)*(10**4)))
        except (RuntimeError):
            pass

# ---------- Calculate binding energy of isotope
def calc_binding_energy(isotope):
    z = nucname.znum(isotope)
    a = nucname.anum(isotope)
    bind = ((z*data.atomic_mass('H1') + (a - z)*neutron_mass) - data.atomic_mass(isotope))*mass_unit
    return bind


# ---------- Find isotope by Z number
def match_z_isotope(isotope,z):
    if(nucname.znum(isotope) == z):
        return True
    else:
        return False


def iso(isotopes,z):
    result = [isotope for isotope in isotopes if match_z_isotope(isotope,z)]
    return result


# ---------- Filter existing isotopes
isotopes_up = list(filter(lambda isotope: (len(data.decay_children(isotope))>0 or
                          data.natural_abund(isotope)>0),isotopes))


# ---------- Get dict of children
def list_branch_ratio(isotope):
    list_branch = list(map(lambda x: data.branch_ratio(isotope, x), list(data.decay_children(isotope))))
    return list_branch


def dit_decay_child(isotope):
    dit_decay = dict(zip(list(data.decay_children(isotope)),list_branch_ratio(isotope)))
    return dit_decay


class Iso_data:

    def __init__(self,name,iso_id,Z,A,natural_abund,binding_energy,atomic_mass,decay_child_list):
        self.name = name
        self.iso_id = iso_id
        self.Z = Z
        self.A = A
        self.natural_abund = natural_abund
        self.binding_energy = binding_energy
        self.atomic_mass = atomic_mass
        self.decay_child_list = decay_child_list

    # Get the most possible child
    def child(self):
        i=0
        max=0
        for decay,ratio in self.decay_child_list.items():
            if(ratio>=max):
                max,i = ratio,decay
        if find_iso_id(i) not in nuc_data:
            return "null"
        else:
            return find_iso_id(i)

    # Return single step of decay chain
    def decay_mode(self):
        if(type(self.child()) is int):
            return (0,0)
        x = self.child()
        if(x.Z < self.Z):
            if(x.A == self.A - 4):
                return (0,0)
            else:
                return (self.Z - x.Z,0)
        elif(x.Z > self.Z):
            return (0,x.Z - self.Z)
        else:
            return (0,1)
        
    def germ(self):
        raise NotImplementedError("Subclass must implement abstract method - error in " + self.name)


class Stable(Iso_data):

    # Calculate germ of stable isotope
    def germ(self):
        if(self.binding_energy > (proton_mass*mass_unit)):
            if(self.Z % 2 == 0):
                return (0,2)
            else:
                return (1,1)
        else:
            if(self.Z % 2 == 0):
                return (0,1)
            else:
                return (1,0)


class Unstable(Iso_data):

    # Calculate germ of unstable isotope
    def germ(self):
        i = self
        decay_sum = (0,0)
        while(type(i) is not Stable):
            decay_sum = myAdd(decay_sum,i.decay_mode())
            i = i.child()
            
        germ_sum = myAdd(i.germ(),decay_sum)
        if((self.Z - germ_sum[0]) % 2 != 0):
            return myAdd(germ_sum,(1,0))
        else:
            return germ_sum


# ---------- Create isotope objects list
def set_nuc_data(isotopes_up):
    nuc_data = []
    for iso_name in isotopes_up:
        if data.natural_abund(iso_name) > 0:
            nuc_data.append(Stable(iso_name,nucname.id(iso_name),nucname.znum(iso_name),nucname.anum(iso_name),
                                   data.natural_abund(iso_name),calc_binding_energy(iso_name),
                                   data.atomic_mass(iso_name),dit_decay_child(iso_name)))
        elif dit_decay_child(iso_name):
            nuc_data.append(Unstable(iso_name,nucname.id(iso_name),nucname.znum(iso_name),nucname.anum(iso_name),
                                     data.natural_abund(iso_name),calc_binding_energy(iso_name),
                                     data.atomic_mass(iso_name),dit_decay_child(iso_name)))
        else:
            print(iso_name)
            
    return nuc_data


nuc_data = set_nuc_data(isotopes_up)


# ---------- Find isotope inside list, by name or id
def find_iso_name(iso_name):
    for isotope in nuc_data:
        if isotope.name == iso_name:
            return isotope


def find_iso_id(iso_id):
    for isotope in nuc_data:
        if isotope.iso_id == iso_id:
            return isotope


wrong0 = ['Li5', 'P44', 'V42', 'Cu68', 'Ni69', 'Co49', 'Br69', 'Rb73', 'Tc90', 'Ru94', 'Te127', 'I114', 'La126',
          'Ce120', 'Sm130', 'Gd134', 'Tb145', 'Dy139', 'Dy140', 'Yb150', 'Lu154', 'Lu162', 'W157', 'Ir199', 'Ir200',
          'Re165', 'Os174', 'Ir168', 'Pt185', 'Au180', 'Au174', 'Au176', 'Tl191', 'Tl183', 'Tl185', 'Pb193', 'Po217',
          'Po193', 'Fr228', 'Ra229', 'At194', 'Rn198', 'Fr203', 'Fr205', 'Fr211', 'Ra211', 'Ac213', 'Ac214', 'U228',
          'Pu230', 'Cm238', 'Cm236', 'Bk241', 'Bk247', 'Bk239', 'Cf244', 'Cf239', 'Es242', 'Tb139', 'Ta161', 'Cm240',
          'Cm235', 'Gd139', 'Lu157', 'Rh122', 'Pd126', 'Ce153', 'Ce155', 'Ce156', 'La128', 'Dy171', 'Dy172', 'Ho146',
          'W165', 'Ra205']

missing_decay = ['He4', 'S44', 'Ti41', 'Zn68', 'Cu69', 'Fe48', 'Se68', 'Kr72', 'Mo90', 'Tc94', 'I127', 'Te114', 'Ba126',
                 'La120', 'Pm130', 'Eu134', 'Gd145', 'Tb139', 'Tb140', 'Tm150', 'Yb154', 'Yb162', 'Ta157', 'Pt199',
                 'Pt200', 'Ta161', 'Re174', 'Re164', 'Ir185', 'Pt180', 'Ir170', 'Ir172', 'Hg191', 'Hg183', 'Au181',
                 'Tl193', 'Pb213', 'Pb189', 'Ra228', 'Ac229', 'Bi190', 'Po194', 'At199', 'At201', 'At207', 'Rn207',
                 'Fr209', 'Fr210', 'Th224', 'U226', 'Am238', 'Pu232', 'Am237', 'Am243', 'Am235', 'Cm240', 'Cm235',
                 'Bk238', 'Gd139', 'Lu157', 'Pu236', 'Pu231', 'Eu139', 'Tm153', 'Pd122', 'Ag126', 'Pr153', 'Pr155',
                 'Pr156', 'Ba128', 'Ho171', 'Ho172', 'Dy146', 'Ta165', 'Fr205']

missing_decay = list(map(lambda x: {nucname.id(x): 1.0}, missing_decay))


for isotope, decay in zip(wrong0, missing_decay):
    if data.natural_abund(isotope) > 0:
        nuc_data.append(Stable(isotope, nucname.id(isotope), nucname.znum(isotope), nucname.anum(isotope),
                               data.natural_abund(isotope), calc_binding_energy(isotope),
                               data.atomic_mass(isotope), decay))
    else:
        nuc_data.append(Unstable(isotope, nucname.id(isotope), nucname.znum(isotope), nucname.anum(isotope),
                                 data.natural_abund(isotope), calc_binding_energy(isotope),
                                 data.atomic_mass(isotope), decay))

"""germs = []
germs_size = []

for isotope in nuc_data:
    germs.append(isotope.germ())
    germs_size.append(sum(isotope.germ()))"""



    




    

    


