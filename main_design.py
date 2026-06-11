
import os
from girders import find_sufficient_girder
from utils import (calculate_moments, get_aci_stress_limits, 
                   calculate_required_S, calculate_prestress_force, 
                   calculate_eccentricity, calculate_detailed_losses,
                   estimate_tendons, calculate_dynamic_ybs)
from visualizer import draw_girder_section
def run_pro_design():
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    print("# +===============================================================================+")
    print("# |             PCDT Pro - Prestressed Concrete Design Tool                       |")
    print("# |   Designed in accordance with ACI 318 and AASHTO standards                    |")
    print("# +===============================================================================+")

    try:
        L = float(input("Span length (ft): "))
        wd = float(input("Dead load (plf): "))
        wl = float(input("Live load (plf): "))
        RH = float(input("Relative Humidity (%) [70]: ") or 70)
        print("\nEccentricity Type:\n1. Variable\n2. Constant")
        is_variable = (input("Choice (1/2): ") == '1')
    except ValueError:
        L, wd, wl, RH, is_variable = 80.0, 400.0, 1200.0, 70, False

    f_cp, f_cip = 6000, 4200
    limits = get_aci_stress_limits(f_cp, f_cip)
    
    R, w0_assumed, y_bs = 0.85, 287.0, 4.0
    girder = None
    
    print("\n--- Processing Iterations (Section + Losses + Layout) ---")
    for i in range(15):
        M0, Md, Ml = calculate_moments(L, w0_assumed, wd, wl)
        S_req = calculate_required_S(M0, Md, Ml, R, limits, is_variable)
        girder = find_sufficient_girder(S_req)
        Pi = calculate_prestress_force(girder, limits)
        
        # Dynamic physical layout check
        N_est = estimate_tendons(Pi)
        y_bs_new = calculate_dynamic_ybs(N_est, girder)
        
        e = calculate_eccentricity(girder, Pi, M0, limits, y_bs_new, is_variable)
        new_R = calculate_detailed_losses(girder, Pi, e, M0, f_cp, f_cip, RH)
        
        if abs(R - new_R) < 0.001 and abs(w0_assumed - girder.w0) < 1.0 and abs(y_bs - y_bs_new) < 0.1:
            R, y_bs = new_R, y_bs_new
            break
            
        R, w0_assumed, y_bs = (R + new_R) / 2, girder.w0, (y_bs + y_bs_new) / 2
        print(f"Iter {i+1}: {girder.name}, Losses {(1-R)*100:.1f}%, y_bs {y_bs:.2f}\"")
# Output Results
print(f"\n[ENGINEERING SUMMARY - FOR VERIFICATION]")
print(f"Moments (kip-ft): M0={M0:.1f}, Md={Md:.1f}, Ml={Ml:.1f}")
print(f"Stress Limits (psi): f_ti={limits['f_ti']:.0f}, f_ci={limits['f_ci']:.0f}, f_ts={limits['f_ts']:.0f}, f_cs={limits['f_cs']:.0f}")
print(f"Target S required: {S_req:.1f} in^3")

print(f"\n[FINAL DESIGN RESULTS]")
print(f"Sufficient Section: {girder.name} (bf = {girder.b_f} in)")
print(f"Physical Strand Centroid (y_bs): {y_bs:.2f} in from bottom")
print(f"Calculated Eccentricity (e): {e:.2f} in")
print(f"Loss Ratio (Pe/Pi): {R:.3f} ({(1-R)*100:.2f}% loss)")
print(f"Number of Tendons: {estimate_tendons(Pi)} cables")
print("# +===============================================================================+")

    
    # New: Draw the cross section
    draw_girder_section(girder, estimate_tendons(Pi))

if __name__ == "__main__":
    run_pro_design()
