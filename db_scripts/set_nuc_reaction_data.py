import db_scripts.nuc_reaction_data as data
import re
from nucreactions.models import Reaction, ReactionsField
from elementaryparticles.models import ElementaryParticle
from radiations.models import Radiation
from isotopes.models import Isotope

"""
Reaction.objects.all().delete()
ReactionsField.objects.all().delete()
"""

reactions = data.reactions
  

def check_if_there_are_many_objects(name, object_class):
    for element in object_class.objects.all().values_list('name', flat='True'):
        m = re.fullmatch('[0-9]+' + element,name)
        if m:
            return element, int(re.search('[0-9]+', name)[0])

    return name, 1


def create_reactions_field(name, object_class):
    many = check_if_there_are_many_objects(name, object_class)
    if object_class is Isotope:
        obj, created = ReactionsField.objects.get_or_create(isotope = Isotope.objects.get(name = many[0]),
                                                            quantity = many[1])
    elif object_class is ElementaryParticle:
        obj, created = ReactionsField.objects.get_or_create(elementary_particle=ElementaryParticle.objects.get(name=many[0]),
                                                            quantity = many[1])
    elif object_class is Radiation:
        obj, created = ReactionsField.objects.get_or_create(radiation=Radiation.objects.get(name=many[0]),
                                                            quantity = many[1])
    else:
        print('Not a valid class')
        return None
    if created: obj.save()
    return obj


def get_object(name):
    if (name is None) | (name == ''):
        return None
    try:
        return create_reactions_field(name, Isotope)

    except Isotope.DoesNotExist:
        try:
            return create_reactions_field(name, ElementaryParticle)

        except ElementaryParticle.DoesNotExist:
            try:
                return create_reactions_field(name, Radiation)
            except Radiation.DoesNotExist:
                print('Cant find %s in data base' % name)


"""
for index,react in reactions.iterrows():
    Reaction.objects.create(
    _target = get_object(react['Target']),
    _projectile = get_object(react['Projectile']),
    _product_one = get_object(react['Product_One']),
    _product_two = get_object(react['Product_Two']),
    _product_three = get_object(react['Product_Three'])
    )
    print('%s + %s -> %s + %s + %s' % (get_object(react['Target']),
                                       get_object(react['Projectile']),
                                       get_object(react['Product_One']),
                                       get_object(react['Product_Two']),
                                       get_object(react['Product_Three'])))
"""

