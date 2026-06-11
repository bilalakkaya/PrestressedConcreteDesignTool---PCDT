import os
os.system('cls')

print("""
# +===============================================================================+
# | Değişken Dışmerkezlik için Kısmi Öngerme Kiriş Tasarımı-Dayanıma Göre Tasarım |
# +===============================================================================+
""")

""" Importations """
"""------------------------"""

import math
import sympy as symp
import numpy as np
import matplotlib as plt
"""------------------------"""

"""------------------------"""
""" Info """
# AASHTO STANDART GIRDERS 
# FLEXURAL DESIGN
"""------------------------"""

""" Problem """
"""------------------------"""
# Kısmi ÖG T-kesit dayanım tasarımı tam kullanım ölü
# yükü altında sıfır yer değiştirme gereksinimine göre
# yapılacaktır.

L = 80 # ft
wd = 400 # plf
wl = 1200 # plf

""" Material Properties """
# Concrete properties
f_cp =  5000 #psi
f_cip = .7*f_cp #psi
R = 0.85
# Tendon steel properties
fpu = 250 # ksi
fpy = .85 * fpu # ksi
"""------------------------"""

""" Solution """
"""------------------------"""
# Test section properties
L_h_ratio = 20
h = (L/L_h_ratio) * 12
bf = 70 # in
tf = 6 # in
tw = 14 # in

# section properties
Ic = 229e3 # in^4
S1 = 13500 # in^3
S2 = 7380 # in^3
c1 = 17 # in
c2 = 31 # in
Ac = 1010 # 𝑖𝑛2
r2 = 227 # 𝑖𝑛2
w0 = 1050 # 𝑝𝑙𝑓

# required flexural strength
M0 = w0*10**-3 * L**2 / 8
Md = wd*10**-3 * L**2 / 8
Ml = wl*10**-3 * L**2 / 8

Mu = 1.4*(M0+Md) + 1.7*Ml
Mn = Mu/0.9
Mn_float = "%.2f" % Mn
print(f"Required flexural strength Mn: {Mn_float} ft-kips")

# required tendon area
z = h-(tf/2)-8
Ap = Mn*12/(0.9*fpu*z)
Ap_float = "%.2f" % Ap
print(f"Required tendon area Ap: {Ap_float} in^2")

# required concrete compression area
Ac_p = Mn*12/(0.85*(f_cp*10**-3)*z)
a = Ac/bf
z = h-(a/2)-8
Ac_p_float = "%.2f" % Ac_p
print(f"Required concrete compression area A'c: {Ac_p_float} in^2")

# steel stress at ultimate load
ro_p = Ap/(bf*(h-8))
gama_p = 0.40
fps = fpu*(1-0.5*ro_p*(fpu/(f_cp*10**-3)))
fps_float = "%.2f" % fps
print(f"Steel stress at ultimate load fps: {fps_float} ksi")

# required eccentricity and prestress force
e = h-8-17
Pe = ((w0+wd)*12*L**2)/(8*e) * 10**-3
Pi = Pe/R
fpi = Pi/Ap
At = 0.0018*(tw*h+tf*(bf-tw))
Pi_float = "%.2f" % Pi
print(f"Required prestress force Pi: {Pi_float} kips")
print(f"Required eccentricity e: {e} in")

""" Checking the limit stresses """
# ACI allowed stresses
f_ci = -0.6 * f_cip
f_ti = 3 * np.sqrt(f_cip)

f_cs = -0.45 * f_cp
f_ts = 6 * np.sqrt(f_cp)

# Pi + M0
f1_Pi = (-Pi*10**3)/Ac * (1-((e*c1)/r2))
f2_Pi = (-Pi*10**3)/Ac * (1+((e*c2)/r2))

f1_M0 = -M0*12e3*c1/Ic
f2_M0 =  M0*12e3*c2/Ic

f1_initial = f1_Pi + f1_M0
f2_initial = f2_Pi + f2_M0

# Pe + M0 + Md + Ml
f1_Pe = .85 * f1_Pi
f2_Pe = .85 * f2_Pi

f1_Md_Ml = -(Md + Ml)*12e3*c1/Ic
f2_Md_Ml =  (Md + Ml)*12e3*c2/Ic
f1_service = f1_Pe + f1_M0 + f1_Md_Ml
f2_service = f2_Pe + f2_M0  + f2_Md_Ml

if f1_initial < f_ti and abs(f2_initial) < abs(f_ci):
    print("\nInitial stresses are within the limits")
else:
    print("\nInitial stresses are not within the limits")
    
if f1_service < f_ts and abs(f2_service) < abs(f_cs):
    print("Service stresses are within the limits\n")
else:
    print("Service stresses are not within the limits\n")
"""------------------------"""