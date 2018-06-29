#!/usr/bin/env python3
# -*- coding: utf-8 -*-


wrong0 = ['Li5','P44','V42','Cu68','Ni69','Co49','Br69','Rb73','Tc90','Ru94','Te127','I114','La126',
         'Ce120','Sm130','Gd134','Tb145','Dy139','Dy140','Yb150','Lu154','Lu162','W157','Ir199','Ir200',
         'Re165','Os174','Ir168','Pt185','Au180','Au174','Au176','Tl191','Tl183','Tl185','Pb193','Po217',
         'Po193','Fr228','Ra229','At194','Rn198','Fr203','Fr205','Fr211','Ra211','Ac213','Ac214','U228',
         'Pu230','Cm238','Cm236','Bk241','Bk247','Bk239','Cf244','Cf239','Es242']

missing_decay = []

missing_decay.append({nucname.id('He4'):1.0}) # Li5
missing_decay.append({nucname.id('S44'):1.0}) # P44
missing_decay.append({nucname.id('Ti41'):1.0}) # V42
missing_decay.append({nucname.id('Zn68'):1.0}) # Cu68
missing_decay.append({nucname.id('Cu69'):1.0}) # Ni69
missing_decay.append({nucname.id('Fe48'):1.0}) # Co49
missing_decay.append({nucname.id('Se68'):1.0}) # Br69
missing_decay.append({nucname.id('Kr72'):1.0}) # Rb73
missing_decay.append({nucname.id('Mo90'):1.0}) # Tc90
missing_decay.append({nucname.id('Tc94'):1.0}) # Ru94
missing_decay.append({nucname.id('I127'):1.0}) # Te127
missing_decay.append({nucname.id('Te114'):1.0}) # I114
missing_decay.append({nucname.id('Ba126'):1.0}) # La126
missing_decay.append({nucname.id('La120'):1.0}) # Ce120
missing_decay.append({nucname.id('Pm130'):1.0}) # Sm130
missing_decay.append({nucname.id('Eu134'):1.0}) # Gd134
missing_decay.append({nucname.id('Gd145'):1.0}) # Tb145
missing_decay.append({nucname.id('Tb139'):1.0}) # Dy139
missing_decay.append({nucname.id('Tb140'):1.0}) # Dy140
missing_decay.append({nucname.id('Tm150'):1.0}) # Yb150
missing_decay.append({nucname.id('Yb154'):1.0}) # Lu154
missing_decay.append({nucname.id('Yb162'):1.0}) # Lu162
missing_decay.append({nucname.id('Ta157'):1.0}) # W157
missing_decay.append({nucname.id('Pt199'):1.0}) # Ir199
missing_decay.append({nucname.id('Pt200'):1.0}) # Ir200
missing_decay.append({nucname.id('Ta161'):1.0}) # Re165
missing_decay.append({nucname.id('Re174'):1.0}) # Os174
missing_decay.append({nucname.id('Re164'):1.0}) # Ir168
missing_decay.append({nucname.id('Ir185'):1.0}) # Pt185
missing_decay.append({nucname.id('Pt180'):1.0}) # Au180
missing_decay.append({nucname.id('Ir170'):1.0}) # Au174
missing_decay.append({nucname.id('Ir172'):1.0}) # Au176
missing_decay.append({nucname.id('Hg191'):1.0}) # Tl191
missing_decay.append({nucname.id('Hg183'):1.0}) # Tl183
missing_decay.append({nucname.id('Au181'):1.0}) # Tl185
missing_decay.append({nucname.id('Tl193'):1.0}) # Pb193
missing_decay.append({nucname.id('Pb213'):1.0}) # Po217
missing_decay.append({nucname.id('Pb189'):1.0}) # Po193
missing_decay.append({nucname.id('Ra228'):1.0}) # Fr228
missing_decay.append({nucname.id('Ac229'):1.0}) # Ra229
missing_decay.append({nucname.id('Bi190'):1.0}) # At194
missing_decay.append({nucname.id('Po194'):1.0}) # Rn198
missing_decay.append({nucname.id('At199'):1.0}) # Fr203
missing_decay.append({nucname.id('At201'):1.0}) # Fr205
missing_decay.append({nucname.id('At207'):1.0}) # Fr211
missing_decay.append({nucname.id('Rn207'):1.0}) # Ra211
missing_decay.append({nucname.id('Fr209'):1.0}) # Ac213
missing_decay.append({nucname.id('Fr210'):1.0}) # Ac214
missing_decay.append({nucname.id('Th224'):1.0}) # U228
missing_decay.append({nucname.id('U226'):1.0}) # Pu230
missing_decay.append({nucname.id('Am238'):1.0}) # Cm238
missing_decay.append({nucname.id('Pu232'):1.0}) # Cm236
missing_decay.append({nucname.id('Am237'):1.0}) # Bk241
missing_decay.append({nucname.id('Am243'):1.0}) # Bk247
missing_decay.append({nucname.id('Am235'):1.0}) # Bk239
missing_decay.append({nucname.id('Cm240'):1.0}) # Cf244
missing_decay.append({nucname.id('Cm235'):1.0}) # Cf239
missing_decay.append({nucname.id('Bk238'):1.0}) # Es242

wrong0.append('Tb139')
missing_decay.append({nucname.id('Gd139'):1.0}) # Tb139

wrong0.append('Ta161')
missing_decay.append({nucname.id('Lu157'):1.0}) # Ta161

wrong0.append('Cm240')
missing_decay.append({nucname.id('Pu236'):1.0}) # Cm240

wrong0.append('Cm235')
missing_decay.append({nucname.id('Pu231'):1.0}) # Cm235

wrong0.append('Gd139')
missing_decay.append({nucname.id('Eu139'):1.0}) # Gd139

wrong0.append('Lu157')
missing_decay.append({nucname.id('Tm153'):1.0}) # Lu157



for isotope, decay in zip(wrong0, missing_decay):
    if(data.natural_abund(isotope) > 0):
        nuc_data.append(Stable(isotope,nucname.id(isotope),nucname.znum(isotope),nucname.anum(isotope),
                                   data.natural_abund(isotope),calc_binding_energy(isotope),
                                   data.atomic_mass(isotope),decay))
    else:
        nuc_data.append(Unstable(isotope,nucname.id(isotope),nucname.znum(isotope),nucname.anum(isotope),
                                   data.natural_abund(isotope),calc_binding_energy(isotope),
                                   data.atomic_mass(isotope),decay))





