import numpy as np

def calculate_moments(L, w0, wd, wl):
    """Calculates moments M0, Md, and Ml in kip-ft."""
    M0 = (w0 / 1000) * L**2 / 8
    Md = (wd / 1000) * L**2 / 8
    Ml = (wl / 1000) * L**2 / 8
    return M0, Md, Ml

def get_aci_stress_limits(f_cp, f_cip):
    """Returns ACI allowed stresses in psi."""
    return {
        "f_ci": -0.6 * f_cip,
        "f_ti": 3 * np.sqrt(f_cip),
        "f_cs": -0.45 * f_cp,
        "f_ts": 6 * np.sqrt(f_cp)
    }

def calculate_required_S(M0, Md, Ml, R, limits, variable_ecc=True):
    """Calculates required section modulus S (in^3)."""
    f_ti, f_ci, f_ts, f_cs = limits["f_ti"], limits["f_ci"], limits["f_ts"], limits["f_cs"]
    
    if variable_ecc:
        S1 = ((1 - R) * M0 + Md + Ml) * 12000 / (R * f_ti - f_cs)
        S2 = ((1 - R) * M0 + Md + Ml) * 12000 / (f_ts - R * f_ci)
    else:
        S1 = (M0 + Md + Ml) * 12000 / (R * f_ti - f_cs)
        S2 = (M0 + Md + Ml) * 12000 / (f_ts - R * f_ci)
    return max(S1, S2)

def calculate_prestress_force(girder, limits):
    """Calculates initial prestress force Pi in kips."""
    f_ti, f_ci = limits["f_ti"], limits["f_ci"]
    f_cci = f_ti - (girder.c / girder.h) * (f_ti - f_ci)
    return girder.A * -f_cci / 1000

def calculate_dynamic_ybs(N_tendons, girder):
    """
    Calculates y_bs based on a 2x2 grid, respecting flange vs web width.
    """
    if N_tendons <= 0: return 2.0
    
    remaining = N_tendons
    row = 0
    total_moment = 0
    
    while remaining > 0:
        height = 2.0 + (row * 2.0)
        # Determine available width at this height
        # If in bottom flange, use b_f. If in web, use t_w.
        if height <= girder.h_bf:
            current_width = girder.b_f
        else:
            current_width = girder.t_w
            
        available_width = current_width - 4.0 # 2" cover
        strands_per_row = max(1, int(available_width // 2) + 1)
        
        count_in_row = min(remaining, strands_per_row)
        total_moment += count_in_row * height
        remaining -= count_in_row
        row += 1
        
    return total_moment / N_tendons

def calculate_eccentricity(girder, Pi, M0, limits, y_bs, variable_ecc=True):
    """Calculates required eccentricity e in inches, limited by dynamic y_bs."""
    f_ti, f_ci = limits["f_ti"], limits["f_ci"]
    f_cci = f_ti - (girder.c / girder.h) * (f_ti - f_ci)
    
    if variable_ecc:
        e = (((f_ti - f_cci) * (girder.S / (Pi * 1000))) + ((M0 * 12000) / (Pi * 1000)))
    else:
        e = (((f_ti - f_cci) * (girder.S / (Pi * 1000))))
    
    max_e = girder.c - y_bs
    return min(e, max_e)

def calculate_detailed_losses(girder, Pi, e, M0, f_cp, f_cip, RH=70):
    """Calculates detailed prestress losses. Returns R (Pe/Pi)."""
    Es, f_pi = 28500000, 0.70 * 270000
    Ec, Eci = 57000 * np.sqrt(f_cp), 57000 * np.sqrt(f_cip)
    ni = Es / Eci
    
    Pi_lb, M0_lbin = Pi * 1000, M0 * 12000
    f_cgp = (Pi_lb / girder.A) + (Pi_lb * (e**2) / girder.I_z) - (M0_lbin * e / girder.I_z)
    
    ES = ni * f_cgp
    SH = 17000 - 150 * RH
    CR = 12 * f_cgp
    RE = 5000 - 0.1 * ES - 0.05 * (SH + (12 * f_cgp)) # Simplified CR in RE
    
    total_loss_psi = ES + SH + CR + RE
    R = (f_pi - total_loss_psi) / f_pi
    return max(0.60, min(0.95, R))

def estimate_tendons(Pi, fpu=270):
    """Estimates number of cables based on A_cable=0.0491 in^2."""
    A_cable, fpy = 0.0491, 0.85 * fpu
    fp = min(0.82 * fpy, 0.74 * fpu)
    return int(np.ceil(Pi / fp / A_cable))
