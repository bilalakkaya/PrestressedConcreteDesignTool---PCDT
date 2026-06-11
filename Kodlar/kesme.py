import os
os.system('cls')

print("""
# +===============================================================================+
# |              Design of Shear of Beams with Deflected Eccentricity             |
# +===============================================================================+
""")

""" Importations """
"""------------------------"""
import math
import sympy as symp
import numpy as np
import matplotlib as plt

from sectionproperties.pre import Geometry
from sectionproperties.analysis.section import Section

# the following path is a .dxf file that describes a box section with two holes
dxf_path = "C:/Users/Bilal Akkaya/Desktop/section.dxf"
"""------------------------"""

"""------------------------"""
# SHEAR DESIGN
"""------------------------"""

""" Problem """
# sol mesnetten 10 ft içeride (a-a kesidi) gereken U etriye aralığının bulunması

"""------------------------"""
# Post-tensioned beam: 40 ft
L = int(input("Please enter span lenght(ft): "))
print(f"Span length is: {L} ft\n")
w_d = int(input("Please enter dead uniform load(plf): "))
print(f"Dead load is: {w_d} plf\n")
w_l = int(input("Please enter live uniform load(plf): "))
print(f"Live load is: {w_l} plf\n")

# L = 45 # ft
# w_d = 345 # plf
# w_l = 1220 # plf

""" Material and Section Properties """
# Concrete properties
f_cp =  5000 #psi

# Tendon steel properties
fpu = 270 # ksi
Pe = 288 # kips
Ap = 1.75 # in^2

# Stirrup steel properties
fy = 40 # ksi

# Section properties
h = 29 # in
b_f_1 = 18 # in
t_f = 5 # in
b_w = 5 # in
b_f_2 = 12 # in

Ac = 245 # in^2
Ic = 24200 # in^4
r_2 = 99 # in^2
c1 = 13.1 # in
c2 = 15.9 # in
w_0 = 255 # plf
"""------------------------"""

# Açıklık ortasında tendon derinliği 24.5 in, ağırlık merkezi en alt liften 15.9 in yukarıda
e_midspan = c2-(h-24.5) # in
# 15 ft uzaklıktan itibaren DM azalmakta ve mesnette yaklaşık olarak sıfıra inmektedir.
# a noktasındaki e:
e_a = e_midspan * (10/15)
# karşılık gelen tendon derinliği:
d = c1 + e_a # in
# ACI minimum derinlik:
d_min = 0.8 * h # in
d = d_min

### Eğilme –kesme çatlaması için itibari kesme dayanımı:
# Kesitte sadece ÖG kaynaklı alt yüzeyde beton gerilmesi:
f2p = -(Pe*10**3/Ac) * (1 + (e_a*c2/r_2)) # ksi

# x=10 ft’dezati yük kaynaklı moment ve kesme kuvveti:
x = 10 # ft
M0 = ((w_0*10**-3)*x/2) * (L-x)
V0 = (w_0*10**-3) * ((L/2)-x)
M_max = (((w_d + w_l)*10**-3)*x/2) * (L-x)
Vi = ((w_d + w_l)*10**-3) * ((L/2)-x)

# Kiriş alt yüzünde 𝑀0kaynaklı gerilme:
f0 = (M0*12e3)*c2/Ic # ksi
Mcr = (Ic/c2) * (6*np.sqrt(f_cp) - f2p - f0)/12e3 # in-lbf
Vci = .6*np.sqrt(f_cp) * b_w*d + V0*1000 + (Vi/M_max)*Mcr*1000
fcc = Pe*1000/Ac 
Vp = Pe * (e_midspan/(15*12))
Vcw = (3.5*np.sqrt(f_cp) + 0.3*fcc) * b_w*d + Vp*1000
Vu = (1.4*(w_0 + w_d)/1000 + 1.7*(w_l/1000)) * 12.5
Vs = Vu - .85*Vci*10**-3
upper_limit = 8*0.85*np.sqrt(f_cp)*b_w*d
lower_limit = 4*0.85*np.sqrt(f_cp)*b_w*d

# For trial purposes, No. 3 U stirrups will be selected:
Av = 2* 0.11 # in^2
s = (0.85 * Av * fy*10**3 * d) / (Vs*10**3)

# print(s)

# Minimum values
Av1 = (50*b_w)/(fy*1000)
Av2 = ((Ap/80)*(fpu/fy)*np.sqrt(d/b_w))/d


Av_min = max(Av1, Av2)*s
Av_min = "%.2f" % Av_min
Av = "%.2f" % Av
s = "%.2f" % s

print(f"Minimum stirrup area: {Av_min} in^2")
print(f"Chosen stirrup area: {Av} in^2")
print(f"The stirrup area is: {Av_min} in^2")
print(f"Spacing of stirrups: {s} in")
