import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_girder_section(girder, N_tendons):
    """
    Draws a realistic AASHTO girder cross-section and the tendon layout.
    """
    fig, ax = plt.subplots(figsize=(6, 8))
    
    h = girder.h
    bf = girder.b_f
    tw = girder.t_w
    h_bf = girder.h_bf
    
    # Accurate AASHTO-like shape calculation
    # h_bf includes the taper. Let's assume a standard AASHTO proportions:
    # 8" rectangular bottom, then taper to web.
    h_bf_rect = 8.0
    h_tf_rect = 8.0
    b_top = bf * 0.8 # Simplified top flange width
    if girder.name == "TYPE IV": b_top = 20.0
    
    pts = [
        (-bf/2, 0), (bf/2, 0),           # Bottom
        (bf/2, h_bf_rect),               # Bottom flange side
        (tw/2, h_bf),                    # Taper to web
        (tw/2, h - h_bf),                # Web side
        (b_top/2, h - h_tf_rect),        # Taper to top flange
        (b_top/2, h), (-b_top/2, h),     # Top
        (-b_top/2, h - h_tf_rect), 
        (-tw/2, h - h_bf), 
        (-tw/2, h_bf), 
        (-bf/2, h_bf_rect)
    ]
    polygon = patches.Polygon(pts, closed=True, fill=None, edgecolor='black', linewidth=2)
    ax.add_patch(polygon)

    # 2. Draw Strands (Tendon Layout)
    remaining = N_tendons
    row = 0
    strand_pts_x = []
    strand_pts_y = []
    
    while remaining > 0:
        y = 2.0 + (row * 2.0)
        
        if y <= h_bf:
            current_width = bf
        else:
            current_width = tw
            
        available_width = current_width - 4.0 
        strands_per_row = max(1, int(available_width // 2) + 1)
        
        count_in_row = min(remaining, strands_per_row)
        start_x = -((count_in_row - 1) * 2.0) / 2
        
        for i in range(count_in_row):
            x = start_x + (i * 2.0)
            strand_pts_x.append(x)
            strand_pts_y.append(y)
            
        remaining -= count_in_row
        row += 1

    ax.scatter(strand_pts_x, strand_pts_y, color='red', s=20, label=f'Strands (N={N_tendons})')
    
    # 3. Draw Centroid Mark
    y_bs = np.mean(strand_pts_y) if strand_pts_y else 0
    ax.axhline(y=y_bs, color='blue', linestyle='--', alpha=0.5, label=f'Centroid y_bs={y_bs:.2f}"')
    
    # Formatting
    ax.set_aspect('equal')
    ax.set_xlim(-bf, bf)
    ax.set_ylim(-2, h + 5)
    ax.set_title(f"AASHTO {girder.name} Section Layout")
    ax.set_xlabel("Width (in)")
    ax.set_ylabel("Height (in)")
    ax.legend(loc='upper right')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.show()
