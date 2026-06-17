# 🌟 Mathematics Visualiser – Advanced Plotting & Calculus Studio

<!-- ADD DEMO GIF HERE -->

**Interactive desktop app for visualizing functions, 3D surfaces, parametric curves, calculus operations, and animations. Built with tkinter + matplotlib.**

## Why This Exists

Visualizing math makes abstract concepts concrete. This tool lets students and educators:
- Plot 2D/3D functions in real-time
- Animate calculus (derivatives, tangent lines, area under curve)
- Export as GIF or PNG
- Explore 8 color schemes + parametric art

## Key Features

### 📊 Plotting Modes
- **2D Functions** – sin(x), polynomials, exponentials, etc.
- **3D Surfaces** – Heatmap rendering with rotation controls
- **Parametric Curves** – Circle, butterfly, rose, Lissajous, spiral
- **Multi-overlay** – Plot multiple functions on same axes

### 🧮 Calculus Tools
- **Derivatives** – Visualize f'(x) with original function
- **Tangent Lines** – Drag slider to show tangent at any point
- **Integrals** – Shade area under curve, compute definite integrals
- **Area Calculation** – Numerical + symbolic integration

### 🎨 Customization
- **8 Color Schemes** – Neon, Cyberpunk, Ocean, Galaxy, Fire, Forest, Sunset, Pastel
- **Plot Styles** – Line, scatter, stem, step, bar
- **Grid Options** – Show/hide grid, toggle minor divisions, adjust transparency
- **Dark/Light Theme** – System-aware automatic switching

### 🎬 Animation Engine
- **Phase Shift** – Functions move horizontally
- **Amplitude Modulation** – Functions pulse over time
- **Frequency Modulation** – Dynamic oscillation changes
- **Growing Plot** – Watch function draw with gradient colors
- **3D Rotation** – Auto-rotate 3D surfaces
- **Export as GIF** – Save animations

## Tech Stack

- **Python 3.8+**
- **tkinter** – GUI
- **matplotlib 3.5+** – plotting
- **numpy, scipy** – numerical computation
- **sympy** – symbolic math (derivatives, integrals)
- **Pillow (optional)** – GIF export

## Quick Start

```bash
git clone https://github.com/georgepol1023/Mathematics-Visualiser.git
cd Mathematics-Visualiser
pip install -r requirements.txt
python maths.py
```

## Usage Examples

### Simple 2D Plot
1. Enter equation: `sin(x)`
2. Set X range: -2π to 2π
3. Click **Plot**

### Calculate Integral
1. Plot: `x**2`
2. Go to **∫ Calculus** tab
3. Set bounds (0 to 5)
4. Check "Show Area Under Curve"
5. Click "Calculate Area" → symbolic + numerical result

### Create Animation
1. Plot: `sin(x)`
2. Go to **🎬 Animation** tab
3. Select "Phase Shift"
4. Click **Start**
5. Click **Save Animation** → exports GIF

### 3D Visualization
1. Switch to "3D Surface" mode
2. Equation: `sin(sqrt(x**2 + y**2))`
3. Click **Plot**
4. Drag to rotate; adjust elevation/azimuth

## Supported Math Functions

| Category | Syntax | Example |
|----------|--------|----------|
| Trig | sin, cos, tan | sin(x), cos(2*x) |
| Exponential | exp, e**x | exp(-x**2) |
| Log | log, ln | log(x, 10) |
| Hyperbolic | sinh, cosh, tanh | sinh(x) |
| Special | sqrt, abs, factorial | sqrt(x), abs(x-2) |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Ctrl+S | Save plot |
| Ctrl+C | Clear plot |
| Ctrl+Q | Quit |
| F11 | Fullscreen |

## Architecture

```
maths.py (55KB)
├── SuperMathGUI.__init__()      # Setup
├── create_ui()                  # Build tabs
├── create_*_controls()          # Tab-specific UI
├── plot_function()              # 2D plotting
├── plot_3d_surface()            # 3D rendering
├── plot_parametric()            # Parametric curves
├── animate_*()                  # Animation logic
└── calculate_integral()         # Calculus engine
```

**Refactoring Opportunity:** Split into modules (ui/, plotting/, calculus/).

## Limitations

- Single-file architecture (55KB) – should be modularized
- Limited symbolic math (sympy only for simple expressions)
- No LaTeX rendering in plots
- Animations can be slow on large point counts

## Future Enhancements

- [ ] Modularized code structure
- [ ] Complex number visualization
- [ ] Vector field plotting (gradients, curl, divergence)
- [ ] LaTeX equation rendering on plots
- [ ] Fourier analysis tool
- [ ] Optimization visualizer

## Performance Tips

- Reduce point count for complex functions
- Use wireframe for 3D surfaces
- Lower animation frame rate for large ranges

## Files

- `maths.py` – Main application
- `requirements.txt` – Dependencies
- `maths.spec` – PyInstaller config (for .exe builds)

## Author

[George Politis](https://github.com/georgepol1023)

## Resources

- [Sympy Documentation](https://docs.sympy.org/)
- [Matplotlib 3D Guide](https://matplotlib.org/stable/gallery/mplot3d/)
- [Calculus Visualization Best Practices](https://www.desmos.com/)
