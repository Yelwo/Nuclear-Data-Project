
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


exec(open("db_scripts/MissingData.py").read())

"""germs = []
germs_size = []

for isotope in nuc_data:
    germs.append(isotope.germ())
    germs_size.append(sum(isotope.germ()))"""



    




    

    


