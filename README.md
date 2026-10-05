# Beam Deflection Solver using Macaulay's Method

A Python-based structural engineering tool to calculate and visualize elastic deflection curves for beams subjected to point loads using **Macaulay's Method** (singularity functions).

---

## 📌 Overview

Determining the deflection curve of beams with multiple concentrated loads conventionally requires dividing the beam into segments, formulating separate bending moment equations for each, and determining numerous integration constants via continuity and boundary conditions.

**Macaulay's method** overcomes this by utilizing bracketed singularity functions:

$$\langle x - a \rangle^n = \begin{cases} (x - a)^n & \text{if } x \ge a \\ 0 & \text{if } x < a \end{cases}$$

This allows the bending moment, slope, and deflection across the entire length of the beam to be expressed in a single unified equation, dramatically simplifying boundary value integration.

---

## ✨ Features

- **Multiple Beam Configurations**:
  - **Simply Supported Beam**: Supports at custom or standard end positions.
  - **Cantilever Beam**: Fixed support at $x = 0$ with zero slope and deflection boundary conditions.
  - **Overhanging Beam**: Supports located at arbitrary positions along the beam ($0 \le a < b \le L$).
- **Cross-Section & Material Properties**:
  - Computes rectangular cross-section moment of inertia:
    $$I = \frac{b \cdot h^3}{12}$$
  - Calculates flexural rigidity $EI$ from Young's Modulus ($E$ in GPa) and cross-section dimensions (mm).
- **Multiple Point Loads**:
  - Supports any number of concentrated loads specified by position and magnitude.
- **Automated Reaction & Constant Solver**:
  - Calculates static equilibrium reactions ($R_A, R_B, M_A$).
  - Solves integration boundary constants ($C_1, C_2$) using `numpy.linalg.solve`.
- **Comprehensive Output & Visualizations**:
  - Prints reaction forces and fixed moments in kN and kNm.
  - Pinpoints maximum deflection value and its exact coordinate along the beam.
  - Generates a formatted ASCII station table using `tabulate`.
  - Plots the elastic deflection curve with supports, undeformed axis, and load vectors using `matplotlib`.

---

## 📐 Mathematical Formulation

From Euler-Bernoulli beam theory:

$$EI \frac{d^2 y}{dx^2} = M(x)$$

Integrating with respect to $x$:

$$EI \frac{dy}{dx} = \int M(x) \, dx + C_1$$

$$EI \cdot y(x) = \iint M(x) \, dx \, dx + C_1 x + C_2$$

Where the integration constants $C_1$ and $C_2$ are resolved through boundary conditions:
- **Cantilever**: $\left. \frac{dy}{dx} \right|_{x=0} = 0 \implies C_1 = 0$, $\left. y \right|_{x=0} = 0 \implies C_2 = 0$
- **Simply Supported / Overhanging**: $y(a) = 0$ and $y(b) = 0$, setting up a $2 \times 2$ linear system:
  $$\begin{bmatrix} a & 1 \\ b & 1 \end{bmatrix} \begin{bmatrix} C_1 \\ C_2 \end{bmatrix} = \begin{bmatrix} -y_{\text{raw}}(a) \\ -y_{\text{raw}}(b) \end{bmatrix}$$

---

## 🛠️ Requirements & Installation

### Prerequisites
- Python 3.8 or later

### Install Dependencies
Install the required packages using `pip`:

```bash
pip install numpy matplotlib tabulate
```

---

## 🚀 Usage

Run the script from your terminal:

```bash
python beam_deflection.py
```

### Interactive Prompts

1. **Select Beam Type**:
   - `1`: Simply Supported
   - `2`: Cantilever
   - `3`: Overhanging
2. **Material & Cross-Section Dimensions**:
   - Young's modulus $E$ (GPa) *(e.g., `200` for structural steel)*
   - Beam width $b$ (mm)
   - Beam height $h$ (mm)
3. **Geometry**:
   - Total length $L$ (m)
   - Left and right support locations (if overhanging beam)
4. **Point Loads**:
   - Number of point loads
   - Position $x$ (m) and magnitude (N downward) for each load

---

## 📊 Sample Output

### Terminal Summary & Station Table
```text
============================================================
       BEAM DEFLECTION SOLVER - MACAULAY METHOD
============================================================

1. Simply Supported
2. Cantilever
3. Overhanging
Choose: 1

Young's modulus E (GPa): 200
Width b (mm): 150
Height h (mm): 300

I = 3.3750e-04 m^4

Beam length (m): 6

Number of point loads: 1
Load 1 position (m): 3
Load 1 magnitude (N downward): 50000

Support reactions
RA = 25.000 kN
RB = 25.000 kN

Maximum deflection:
-2.77778 mm at x=3.000 m

Deflection table
+--------+-------------------+
|   x(m) |   Deflection(mm)  |
+========+===================+
|   0.00 |            0.0000 |
|   0.60 |           -0.7467 |
|   1.20 |           -1.4293 |
|   1.80 |           -1.9947 |
|   2.40 |           -2.4373 |
|   3.00 |           -2.7778 |
|   3.60 |           -2.4373 |
|   4.20 |           -1.9947 |
|   4.80 |           -1.4293 |
|   5.40 |           -0.7467 |
|   6.00 |            0.0000 |
+--------+-------------------+
```

### Visual Plot
A Matplotlib window opens displaying:
- **Elastic curve** showing the downward deflection profile along the span.
- **Support markers** ($\triangle$ pinned/roller supports or vertical bar for fixed end).
- **Annotated force vectors** showing the point load positions and magnitudes.

---

## 📁 File Structure

```text
beam-deflection-macaulay/
├── beam_deflection.py    # Main solver and visualization script
└── README.md             # Project documentation
```

---

## 📄 Sign Conventions

| Quantity | Positive (+) | Negative (-) |
| :--- | :--- | :--- |
| **Deflection ($y$)** | Upward | Downward |
| **Applied Load ($P$)** | Downward in prompt input | — |
| **Reactions ($R_A, R_B$)**| Upward force | Downward force |
| **Fixed Moment ($M_A$)** | Counter-clockwise / resisting | — |

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
