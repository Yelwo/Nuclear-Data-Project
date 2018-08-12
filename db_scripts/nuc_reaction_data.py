import pandas as pd
from elementaryparticles.models import ElementaryParticle
from radiations.models import Radiation
import re

"""
ElementaryParticle.objects.all().delete()
Radiation.objects.all().delete()
"""

# ---------- Adding elementary particles and radiation
"""
Radiation.objects.create(name = 'α')
Radiation.objects.create(name = 'β-')
Radiation.objects.create(name = 'β+')

elementary_names = ['π+', 'π-', 'π0', 'K+', 'K-', 'K0', 'Σ+', 'Σ0', 'Σ-', 'Λ', 'Ω-', 'p', 'n', 'γ', 'e-']
elementary_masses = [139.569, 139.569, 134.965, 493.707, 493.707, 497.7, 1189.37, 1192.47, 1197.35, 1115.6, 1672.2,
                     938.279, 939.573, 0.0, 0.511]

for name, mass in zip(elementary_names,elementary_masses):
    ElementaryParticle.objects.create(name = name, mass = mass)
"""
# ---------- Opening files
file = 'db_scripts/Nuclear_Reactions.xlsx'
xl = pd.ExcelFile(file)
reactions_first_type = xl.parse('Sheet1')
reactions_second_type = xl.parse('Sheet2')

# ---------- Slicing data from first sheet into columns
reactions_first_type['Left'] = reactions_first_type['Reaction'].str.split('→').apply(lambda x: x[0].strip())
reactions_first_type['Right'] = reactions_first_type['Reaction'].str.split('→').apply(lambda x: x[1].strip())
reactions_first_type['Projectile'] = reactions_first_type['Left'].apply(lambda x: re.split(' \+ ',x)[0].strip())
reactions_first_type['Target'] = reactions_first_type['Left'].apply(lambda x: re.split(' \+ ',x)[1].strip())
reactions_first_type['Product_One'] = reactions_first_type['Right'].apply(lambda x: re.split(' \+ ',x)[0].strip())
reactions_first_type['Product_Two'] = reactions_first_type['Right'].apply(lambda x: re.split(' \+ ',x)[1].strip())


def get_product_three_first_type(x):
    try:
        return re.split(' \+ ',x)[2].strip()
    except IndexError:
        return ''

reactions_first_type['Product_Three'] = reactions_first_type['Right'].apply(get_product_three_first_type)

# ---------- Slicing data from second sheet into columns
reactions_second_type['Left'] = reactions_second_type['Reaction'].str.split(',').apply(lambda x: x[0].strip())
reactions_second_type['Right'] = reactions_second_type['Reaction'].str.split(',').apply(lambda x: x[1].strip())
reactions_second_type['Projectile'] = reactions_second_type['Left'].str.split('(').apply(lambda x: x[1].strip())
reactions_second_type['Target'] = reactions_second_type['Left'].str.split('(').apply(lambda x: x[0].strip())
reactions_second_type['Product_One'] = reactions_second_type['Right'].str.split(')').apply(lambda x: x[1].strip())
reactions_second_type['Product_Two'] = reactions_second_type['Right'].str.split(')').apply(lambda x: re.split(' \+ ',x[0])[0].strip())


def get_product_three_second_type(x):
    try:
        return re.split('\+',x[0])[1].strip()
    except IndexError:
        return ''

reactions_second_type['Product_Three'] = reactions_second_type['Right'].str.split(')').apply(get_product_three_second_type)

# ---------- Converting isotopes to form that matches isotope.name in our isotope model
# Converting first table


def conv_isotopes_first_type(value):
    if ' ' in value:
        return value.split()[1] + value.split()[2]
    else:
        return value

columns = ['Projectile','Target','Product_One','Product_Two','Product_Three']

for column in columns:
    reactions_first_type[column] = reactions_first_type[column].apply(conv_isotopes_first_type)

# Converting second table

def conv_isotopes_second_type(value):
    if re.fullmatch('[0-9]+[A-Z][a-z]*',value) is not None:
        return re.search('[A-Z][a-z]*',value)[0] + re.search('[0-9]+',value)[0]
    else:
        return value

for column in columns:
    reactions_second_type[column] = reactions_second_type[column].apply(conv_isotopes_second_type)

# ---------- Adding type column

reactions_first_type['Type'] = 'first'
reactions_second_type['Type'] = 'second'

# ---------- Creating joint data frame

reactions = pd.concat([reactions_first_type,reactions_second_type], ignore_index = True)
reactions = reactions.replace(['D','d'],'H2')
reactions = reactions.replace(['2d','2D'],'2H2')
reactions = reactions.replace('EL','e-')
reactions = reactions.replace({'0':None})
