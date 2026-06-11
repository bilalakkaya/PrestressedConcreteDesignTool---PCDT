# Prestressed Concrete Design Tools (PCDT)

This is a tool for designing prestressed concrete beams in accordance with ACI 318 and AASHTO standards.

## 🚀 Features
- **AASHTO Section Library:** Built-in properties for Standard Girders (Type I to VI).
- **Automated Section Selection:** Iteratively finds the most efficient section for a given span and load.
- **Flexural Design:** Supports both Variable (Deflected) and Constant eccentricity.
- **Tendon Estimation:** Calculates required prestress force and estimates the number of cables.

## 📂 Project Structure
- `main_design.py`: Main interactive entry point for flexural design.
- `girders.py`: AASHTO girder database and section selection logic.
- `utils.py`: Core engineering formulas and ACI stress limit calculations.
- `Kodlar/`: Original source scripts (kept for reference).

## 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/prestressed-concrete-design.git
   ```
2. Install dependencies:
   ```bash
   pip install numpy
   ```

## 📖 Usage
Run the main design script:
```bash
python main_design.py
```

## ⚖️ License
MIT License

## 🎓 Author
**Mustafa Bilal Akkaya**
*Structural Engineer*
