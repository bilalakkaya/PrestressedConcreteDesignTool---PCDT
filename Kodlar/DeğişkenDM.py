import os
os.system('cls')

print("""
# +===============================================================================+
# |                Design of Tendons of Beams with Variable Eccentricity          |
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
# Post-tensioned beam: 40 ft
L = int(input("Please enter span lenght(ft): "))
print(f"Span length is: {L} ft\n")
w_d = int(input("Please enter dead uniform load(plf): "))
print(f"Dead load is: {w_d} plf\n")
w_l = int(input("Please enter live uniform load(plf): "))
print(f"Live load is: {w_l} plf\n")

""" Material Properties """
# Concrete properties
f_cp =  6000 #psi
f_cip = 4200 #psi
R = 0.85 # loses
# Tendon steel properties
fpu = 240 # ksi
fpy = .85 * fpu # ksi
"""------------------------"""

""" Section properties """
# TYPE I
type_I = {
    "h":   28,            # in
    "c":   (28/2),        # in (h_I / 2)
    "A":   276,           # in^2
    "I_z": 22750,         # in^4
    "S":   (22750/12.59), # in^3 (I_z_I / 12.59)
    "w0":  287,           # lb/ft
    "r^2": 82.4           # in^2
}

# TYPE II
type_II = {
    "h":   36,               # in
    "c":   (36 / 2),         # in (h_II / 2)
    "A":   369,              # in^2
    "I_z_II": 50980,            # in^4
    "S":   (50980 / 15.83),  # in^3 (I_z_II / 12.59)
    "w0":  384,              # lb/ft
    "r^2": 138.15            # in^2
}

# TYPE III
type_III = {
    "h":   45,                # in
    "c":   (45 / 2),          # in
    "A":   560,               # in^2
    "I_z": 125390,            # in^4
    "S":   (125390 / 20.27),  # in^3
    "w0":  583,               # lb/ft
    "r^2": 224.11             # in^2
}

# TYPE IV
type_IV = {
    "h":   54,                # in
    "c":   (54 / 2),          # in
    "A":   789,               # in^2z
    "I_z": 260730,            # in^4
    "S":   (260730 / 24.73),  # in^3
    "w0":  822,               # lb/ft
    "r^2": 330.47             # in^2
}

# TYPE V
type_V = {
    "h":   63,                # in
    "c":   (63 / 2),          # in
    "A":   1013,              # in^2
    "I_z": 521180,            # in^4
    "S":   (521180 / 31.96),  # in^3
    "w0":  1055,              # lb/ft
    "r^2": 514.47             # in^2
}

# TYPE VI
type_VI = {
    "h":   72,                # in
    "c":   (72 / 2),          # in
    "A":   1085,              # in^2
    "I_z": 733320,            # in^4
    "S":   (733320 / 36.38),  # in^3
    "w0":  1130,              # lb/ft
    "r^2": 675.87             # in^2
}



""" Solution """
"""------------------------"""
# ACI allowed stresses
f_ci = -0.6 * f_cip
f_ti = 3 * np.sqrt(f_cip)

f_cs = -0.45 * f_cp
f_ts = 6 * np.sqrt(f_cp)

# Initialize w0_assumed
w0_assumed = 287  # plf

while True:
    # Calculate moments
    M0 = w0_assumed * (10**-3) * L**2 / 8
    Md = w_d * (10**-3) * L**2 / 8
    Ml = w_l * (10**-3) * L**2 / 8

    # Required section modulus
    S1 = ((1 - R) * M0 + Md + Ml) * 12000 / (R * f_ti - f_cs)
    S2 = ((1 - R) * M0 + Md + Ml) * 12000 / (f_ts - R * f_ci)

    """ Finding the sufficent section """
    def closest(S_lst, S):
        
        S_lst = np.asarray(S_lst)
        idx = (np.abs(S_lst - S)).argmin()
        return S_lst[idx]
    
    # Find the closest section
    S_lst = [type_I["S"], type_II["S"], type_III["S"], type_IV["S"], type_V["S"], type_VI["S"]]
    S_closest = closest(S_lst, max(S1, S2))

    # Determine the sufficient section and update w0_assumed
    if S_closest == type_I["S"]:
        c_design = type_I["c"]
        h_design = type_I["h"]
        A_design = type_I["A"]
        r2_design = type_I["r^2"]
        w0_design = type_I["w0"]
        
    elif S_closest == type_II["S"]:
        c_design = type_II["c"]
        h_design = type_II["h"]
        A_design = type_II["A"]
        r2_design = type_II["r^2"]
        w0_design = type_II["w0"]
        
    elif S_closest == type_III["S"]:
        c_design = type_III["c"]
        h_design = type_III["h"]
        A_design = type_III["A"]
        r2_design = type_III["r^2"]
        w0_design = type_III["w0"]
        
    elif S_closest == type_IV["S"]:
        c_design = type_IV["c"]
        h_design = type_IV["h"]
        A_design = type_IV["A"]
        r2_design = type_IV["r^2"]
        w0_design = type_IV["w0"]
        
    elif S_closest == type_V["S"]:
        c_design = type_V["c"]
        h_design = type_V["h"]
        A_design = type_V["A"]
        r2_design = type_V["r^2"]
        w0_design = type_V["w0"]
        
    elif S_closest == type_VI["S"]:
        c_design = type_VI["c"]
        h_design = type_VI["h"]
        A_design = type_VI["A"]
        r2_design = type_VI["r^2"]
        w0_design = type_VI["w0"]

    # Check if w0_assumed matches the sufficient section's w0
    if w0_assumed == w0_design:
        if w0_design == type_I["w0"]:
            print("Sufficient section is TYPE I")
        elif w0_design == type_II["w0"]:
            print("Sufficient section is TYPE II")
        elif w0_design == type_III["w0"]:
            print("Sufficient section is TYPE III")
        elif w0_design == type_IV["w0"]:
            print("Sufficient section is TYPE IV")
        elif w0_design == type_V["w0"]:
            print("Sufficient section is TYPE V")
        elif w0_design == type_VI["w0"]:
            print("Sufficient section is TYPE VI")
        break  # Exit the loop if the assumption is consistent with the selected section
    else:
        # Update w0_assumed with the w0 of the selected section
        w0_assumed = w0_design
        if w0_design == type_I["w0"]:
            print("Sufficient section is TYPE I")
        elif w0_design == type_II["w0"]:
            print("Sufficient section is TYPE II")
        elif w0_design == type_III["w0"]:
            print("Sufficient section is TYPE III")
        elif w0_design == type_IV["w0"]:
            print("Sufficient section is TYPE IV")
        elif w0_design == type_V["w0"]:
            print("Sufficient section is TYPE V")
        elif w0_design == type_VI["w0"]:
            print("Sufficient section is TYPE VI")
        break


""" Finding the sufficent prestress force """

f_cci = f_ti - (c_design / h_design)*(f_ti - f_ci)
P_i = A_design * -f_cci * 10**-3

""" Finding the sufficent eccentricity"""
e = (((f_ti - f_cci) * (S_closest / (P_i * 10**3))) + ((M0*12000) / (P_i * 10**3)))

P_i_float = "%.2f" % P_i
e_float = "%.2f" % e

""" Checking the limit stresses """
# Pi + M0
f1_Pi = (-P_i*10**3)/A_design * (1-((e*c_design)/r2_design))
f2_Pi = (-P_i*10**3)/A_design * (1+((e*c_design)/r2_design))

f1_M0 = -M0*12e3/S_closest
f2_M0 =  M0*12e3/S_closest

f1_initial = f1_Pi + f1_M0
f2_initial = f2_Pi + f2_M0


# Pe + M0 + Md + Ml
f1_Pe = .85 * f1_Pi
f2_Pe = .85 * f2_Pi

f1_Md_Ml = -(Md + Ml)*12e3/S_closest
f2_Md_Ml =  (Md + Ml)*12e3/S_closest

f1_service = f1_Pe + f1_Md_Ml
f2_service = f2_Pe + f2_Md_Ml

if f1_initial < f_ti and abs(f2_initial) < abs(f_ci):
    print("Initial stresses are within the limits")
else:
    print("Initial stresses are not within the limits")
    
if f1_service < f_ts and abs(f2_service) < abs(f_cs):
    print("Service stresses are within the limits")
else:
    print("Service stresses are not within the limits")

# chooing the tendons 
A_cable = 0.0491 # in^2
fp = min(0.82*fpy, 0.74*fpu) # ksi
A_tendon = P_i/fp # in^2
N_tendon = round(int((A_tendon/A_cable)),0)
print(f"\nNumber of cables is: {N_tendon}\n")

"""------------------------"""
print(f"Corresponding prestress force and eccentricity is:\nPi = {P_i_float} kips\ne = {e_float} in\n")

print("# +===================================================================================")

