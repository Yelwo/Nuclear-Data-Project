#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
