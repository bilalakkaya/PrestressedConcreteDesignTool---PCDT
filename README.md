# Prestressed Concrete Design Tools (PCDT Pro)

## About the Project
This software is a terminal-based engineering tool designed for the automated design and analysis of prestressed concrete AASHTO girders. It performs iterative cross-section selection, detailed prestress loss calculations, and stress verification in accordance with **ACI 318** and **AASHTO** standards. The tool is particularly useful for structural engineers seeking a rapid yet rigorous preliminary design for highway bridge girders.

## Features
- **AASHTO Section Library:** Includes a comprehensive database of standard AASHTO Girders (Type I through VI).
- **Iterative Design Engine:** Automatically finds the most efficient girder section for a given span and load by iterating through section properties, losses, and strand layouts.
- **Dynamic Prestress Losses:** Calculates detailed time-dependent losses (Elastic Shortening, Shrinkage, Creep, and Relaxation) instead of assuming a fixed percentage.
- **Physical Strand Layout:** Computes the actual centroid of the strand group ($y_{bs}$) by arranging cables in a 2x2 grid, respecting cover requirements and varying flange/web widths.
- **Stress Limit Verification:** Checks fiber stresses at both the transfer stage and service stage against ACI 318 limits.
- **Visualization:** Generates a cross-section plot showing the girder geometry and the estimated strand distribution.

## Project Structure
- `main_design.py`: Main interactive entry point for the design iteration loop.
- `girders.py`: AASHTO girder database and section selection logic.
- `utils.py`: Core engineering formulas (ACI stress limits, loss equations, dynamic $y_{bs}$).
- `visualizer.py`: Matplotlib-based cross-section and tendon visualization.
- `Kodlar/`: Collection of legacy source scripts for specific calculation modules.

## Installation
### Requirements
- Python 3.8 or higher
- The following libraries:
  - `numpy`
  - `matplotlib`

### Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/bilalakkaya/PrestressedConcreteDesignTool---PCDT.git
cd PrestressedConcreteDesignTool---PCDT

# 2. Install dependencies
pip install numpy matplotlib

# 3. Run the application
python main_design.py
```

## Usage
1. Launch the application via `python main_design.py`.
2. Enter the **Span length (ft)**, **Dead load (plf)**, and **Live load (plf)**.
3. Select the **Eccentricity Type** (1 for Variable/Deflected, 2 for Constant).
4. The software will run up to 15 iterations to converge on:
   - The optimal AASHTO section.
   - Converged loss ratio ($R = P_e/P_i$).
   - Physical strand centroid ($y_{bs}$).
5. Review the **Engineering Summary** for moments, stress limits, and final design parameters.
6. A visualization window will open showing the girder cross-section and cable arrangement.

## Unit System
| Quantity | Unit |
| :--- | :--- |
| Length (Span) | Feet (ft) |
| Dimensions | Inches (in) |
| Force | Kips (k) |
| Stress / Modulus | PSI (lb/in²) |
| Distributed Loads | PLF (lb/ft) |

## Technical Notes

### ACI 318 Stress Limits
The tool enforces the following stress limits during the iteration:
- **Transfer Stage:** $f_{ci} = -0.60 f'_{ci}$, $f_{ti} = 3\sqrt{f'_{ci}}$
- **Service Stage:** $f_{cs} = -0.45 f'_c$, $f_{ts} = 6\sqrt{f'_c}$

### Prestress Loss Calculation
Detailed losses are calculated using AASHTO/ACI approximations:
$$Total Loss = ES + SH + CR + RE$$
Where:
- **ES:** Elastic Shortening
- **SH:** Shrinkage (Relative Humidity dependent)
- **CR:** Creep of concrete
- **RE:** Relaxation of steel

### Dynamic Strand Centroid ($y_{bs}$)
Unlike simplified models that assume a fixed $y_{bs}$, PCDT computes the centroid based on a physical grid. The algorithm checks the available width at each row (accounting for 2" cover) to determine how many cables can fit in the bottom flange vs. the web.

## License
This software was developed for academic and professional engineering use.

## Author
**Mustafa Bilal Akkaya**
*Structural Engineer*
