from django.db import models
from django.urls import reverse
from isotopes.models import Isotope
from radiations.models import Radiation
from elementaryparticles.models import ElementaryParticle
from functools import reduce


# ---------- Add two tuples
def my_add(x, y):
    return tuple(map(sum, zip(x, y)))


# ---------- Multiply tuple by a scalar
def my_multiply(x, tup):
    return tuple([x * y for y in tup])


class ReactionsField(models.Model):
    isotope = models.ForeignKey(Isotope, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='reaction_isotope')
    elementary_particle = models.ForeignKey(ElementaryParticle, null=True, blank=True, on_delete=models.CASCADE,
                                            related_name='reaction_elementary_particle')
    radiation = models.ForeignKey(Radiation, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='reaction_radiation')

    quantity = models.IntegerField(default=1)

    @property
    def field_content(self):
        if self.isotope is not None:
            return self.isotope
        elif self.elementary_particle is not None:
            return self.elementary_particle
        elif self.radiation is not None:
            return self.radiation
        else:
            return '0'

    def __str__(self):
        if self.quantity > 1:
            return str(self.quantity) + self.field_content.name
        else:
            return self.field_content.name

    class Meta:
        ordering = ['isotope', 'elementary_particle', 'radiation']


class Reaction(models.Model):
    _target = models.ForeignKey(ReactionsField, on_delete=models.CASCADE, related_name='target', null=True)
    _projectile = models.ForeignKey(ReactionsField, on_delete=models.CASCADE, related_name='projectile', null=True)
    _product_one = models.ForeignKey(ReactionsField, on_delete=models.CASCADE, related_name='product_one', null=True)
    _product_two = models.ForeignKey(ReactionsField, on_delete=models.CASCADE, related_name='product_two', null=True)
    _product_three = models.ForeignKey(ReactionsField, on_delete=models.CASCADE, related_name='product_three',
                                       null=True)

    @property
    def target(self):
        return self._target.field_content

    @property
    def projectile(self):
        return self._projectile.field_content

    @property
    def product_one(self):
        return self._product_one.field_content

    @property
    def product_two(self):
        return self._product_two.field_content

    @property
    def product_three(self):
        return self._product_three.field_content

    @property
    def print_target(self):
        return self._target

    @property
    def print_projectile(self):
        return self._projectile

    @property
    def print_product_one(self):
        return self._product_one

    @property
    def print_product_two(self):
        return self._product_two

    @property
    def print_product_three(self):
        return self._product_three

    @property
    def reaction_items(self):
        _reaction_items = []
        if self._projectile: _reaction_items.append(self._projectile)
        if self._target: _reaction_items.append(self._target)
        if self._product_one: _reaction_items.append(self._product_one)
        if self._product_two: _reaction_items.append(self._product_two)
        if self._product_three: _reaction_items.append(self._product_three)
        return _reaction_items

    @property
    def left_right(self):
        i = self.reaction_items.index(self._target)
        return self.reaction_items[:i + 1], self.reaction_items[i + 1:]

    @property
    def germ(self):

        left = reduce(lambda x, y: my_add(x, my_multiply(y.quantity, y.field_content.germ)), self.left_right[0], (0, 0))
        right = reduce(lambda x, y: my_add(x, my_multiply(y.quantity, y.field_content.germ)), self.left_right[1], (0, 0))

        return max(left[0], right[0]), max(left[1], right[1])

    @property
    def germ_view(self):
        _germ = self.germ
        _germ_view = ""
        if _germ[1] > 0:
            if _germ[1] == 1:
                _germ_view += 'n'
            else:
                _germ_view += str(_germ[1]) + 'n'
        if _germ[0] > 0:
            if _germ[0] == 1:
                _germ_view += 'p'
            else:
                _germ_view += str(_germ[0]) + 'p'

        return _germ_view

    @property
    def germ_shell_view(self):

        def shell_occupation(reaction_item):
            protons = neutrons = 0
            if reaction_item:
                item = reaction_item.field_content
                quan = reaction_item.quantity
                if type(item) is Isotope:
                    protons += quan * item.z_number
                    neutrons += quan * (item.a_number - item.z_number)
                elif item.name == 'α':
                    protons += quan * 2
                    neutrons += quan * 2
                elif item.name in ['n', 'p']:
                    protons += quan * item.germ[0]
                    neutrons += quan * item.germ[1]

            return protons, neutrons

        sum_of_items = [shell_occupation(self._target), shell_occupation(self._projectile), my_multiply(-1, self.germ)]

        protons, neutrons = tuple(sum(x) for x in zip(*sum_of_items))

        def display(nucleons, n_or_p):
            if nucleons > 1:
                return str(nucleons) + n_or_p
            elif nucleons == 1:
                return n_or_p
            else:
                return ""

        return "G(" + self.germ_view + ")" + display(neutrons, "n") + display(protons, "p")

    @property
    def reaction_view(self):

        def item_view(reaction_item):
            if reaction_item.quantity == 1:
                quant = ''
            else:
                quant = '%s' % reaction_item.quantity
            if type(reaction_item.field_content) is Isotope:
                return quant + reaction_item.field_content.germ_shell_view
            else:
                return quant + reaction_item.field_content.name

        print(self)

        if any((type(x.field_content) is ElementaryParticle) and (x.field_content.name not in ['n', 'p', 'γ'])
               for x in self.reaction_items):
            return 'Cant create reaction view'
        else:
            i = self.reaction_items.index(self._target)
            reaction_items_view = list(map(item_view, self.reaction_items))
            left, right = ' + '.join(reaction_items_view[:i + 1]), \
                          ' + '.join(reaction_items_view[i + 1:])

            return " → ".join([left, self.germ_shell_view, right])

    def get_absolute_url(self):
        return reverse('nucreactions:reaction-detail', args=[str(self.id)])

    @property
    def product_sum_names(self):
        return ' + '.join([x.__str__() for x in self.left_right[1][1:]])

    def __str__(self):
        return '%s(%s,%s)%s' % (self._target.__str__(), self._projectile.__str__(),
                                self.product_sum_names, self._product_one.__str__())

    def __unicode__(self):
        return self.__str__()

    class Meta:
        ordering = ['_target']
