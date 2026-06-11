import numpy as np

class AASHTOGirder:
    def __init__(self, name, h, c, A, I_z, S, w0, r2, b_f, t_w, h_bf):
        self.name = name
        self.h = h        # Total height (in)
        self.c = c        # Neutral axis to bottom (in)
        self.A = A        # Area (in^2)
        self.I_z = I_z    # Inertia (in^4)
        self.S = S        # Section Modulus (in^3)
        self.w0 = w0      # Weight (lb/ft)
        self.r2 = r2      # r^2
        self.b_f = b_f    # Bottom flange width (in)
        self.t_w = t_w    # Web thickness (in)
        self.h_bf = h_bf  # Bottom flange height including taper (in)

# Standard AASHTO I-Beam Dimensions (Approximated for Type I-VI)
GIRDERS = {
    # Name, h, c, A, I, S, w0, r2, b_f, t_w, h_bf
    "TYPE I":   AASHTOGirder("TYPE I",   28, 12.59, 276, 22750, 1807, 287, 82.4, 16, 6, 10),
    "TYPE II":  AASHTOGirder("TYPE II",  36, 15.83, 369, 50980, 3220, 384, 138.2, 18, 6, 12),
    "TYPE III": AASHTOGirder("TYPE III", 45, 20.27, 560, 125390, 6186, 583, 224.1, 22, 7, 14),
    "TYPE IV":  AASHTOGirder("TYPE IV",  54, 24.73, 789, 260730, 10543, 822, 330.5, 26, 8, 16),
    "TYPE V":   AASHTOGirder("TYPE V",   63, 31.96, 1013, 521180, 16307, 1055, 514.5, 28, 8, 18),
    "TYPE VI":  AASHTOGirder("TYPE VI",  72, 36.38, 1085, 733320, 20157, 1130, 675.9, 28, 8, 20)
}

def find_sufficient_girder(required_S):
    sorted_girders = sorted(GIRDERS.values(), key=lambda g: g.S)
    for girder in sorted_girders:
        if girder.S >= required_S:
            return girder
    return sorted_girders[-1]
