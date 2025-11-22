# 🌟 Math Visualization Studio 🌟

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-2.0-purple)

A powerful, feature-rich mathematical visualization application with stunning aesthetics, advanced calculus tools, 3D plotting capabilities, and real-time animations. Transform your mathematical equations into beautiful, interactive visualizations!

## ✨ Features at a Glance

### 🎨 **Stunning Visual Design**
- **Dark/Light Theme** - Toggle between elegant dark mode and classic light mode
- **8 Color Schemes** - Neon Dreams, Cyberpunk, Ocean, Galaxy, Fire, Forest, Sunset, Pastel
- **Modern UI** - Beautiful interface with intuitive controls and smooth interactions
- **High-DPI Support** - Crystal clear rendering on all displays

### 📊 **Multiple Plot Modes**

#### 2D Plotting
- Standard function plotting with multiple styles
- Real-time equation evaluation
- Multi-function overlay support
- Interactive zoom and pan

#### 3D Surface Plotting
- Beautiful 3D surface visualizations
- Wireframe and contour options
- Interactive rotation and elevation control
- Colormap customization

#### Parametric Curves
- Create stunning mathematical art
- Pre-loaded famous curves (hearts, butterflies, spirals)
- Gradient color effects
- Direction indicators

### 🧮 **Advanced Calculus Tools**
- **Derivatives** - Visualize first derivatives in real-time
- **Integrals** - Calculate definite integrals symbolically and numerically
- **Tangent Lines** - Draw tangent lines at any point
- **Area Under Curve** - Shade and calculate areas between bounds

### 🎬 **Animation Engine**
- **Phase Shift** - Animate functions moving through space
- **Amplitude Modulation** - Vary amplitude dynamically
- **Frequency Modulation** - Change frequency in real-time
- **Growing Plots** - Watch functions draw themselves
- **3D Rotation** - Automatic rotation of 3D plots
- **Export as GIF** - Save your animations

## 📋 Prerequisites

### Required Dependencies
```bash
# Core requirements
python >= 3.8
tkinter (usually comes with Python)
matplotlib >= 3.5.0
numpy >= 1.20.0
sympy >= 1.9
scipy >= 1.7.0
```

### Optional Dependencies
```bash
# For animation export
pillow >= 8.0.0  # For GIF export
```

## 🚀 Installation

### Method 1: Quick Install
```bash
# Clone or download the project
git clone https://github.com/yourusername/super-math-studio.git
cd super-math-studio

# Install dependencies
pip install -r requirements.txt

# Run the application
python super_math_gui.py
```

### Method 2: Manual Installation
```bash
# Install required packages individually
pip install matplotlib numpy sympy scipy pillow

# Run the application
python super_math_gui.py
```

### Method 3: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv math_viz_env

# Activate it
# On Windows:
math_viz_env\Scripts\activate
# On macOS/Linux:
source math_viz_env/bin/activate

# Install dependencies
pip install matplotlib numpy sympy scipy pillow

# Run application
python super_math_gui.py
```

## 📖 User Guide

### Getting Started

1. **Launch the Application**
   ```bash
   python super_math_gui.py
   ```
   The application opens with a beautiful demo function already plotted.

2. **Basic Function Plotting**
   - Enter your equation in the function input box (e.g., `sin(x)`, `x**2`, `exp(x)`)
   - Adjust the X and Y ranges using the spinboxes
   - Click the 🎯 **Plot** button to visualize

3. **Navigation**
   - Use the tabs to switch between different features
   - Each tab contains specific controls for that mode

### 📈 Functions Tab

#### Supported Mathematical Functions
| Function Type | Syntax | Example |
|--------------|--------|---------|
| Power | `x**n` | `x**2`, `x**0.5` |
| Trigonometric | `sin()`, `cos()`, `tan()` | `sin(x)`, `cos(2*x)` |
| Exponential | `exp()`, `e**x` | `exp(x)`, `exp(-x**2)` |
| Logarithmic | `log()`, `ln()` | `log(x)`, `log(x, 10)` |
| Hyperbolic | `sinh()`, `cosh()`, `tanh()` | `sinh(x)`, `cosh(x/2)` |
| Special | `sqrt()`, `abs()` | `sqrt(x)`, `abs(x-2)` |

#### Quick Functions
Pre-loaded common functions for quick access:
- `sin(x)` - Sine wave
- `x²` - Parabola
- `eˣ` - Exponential growth
- `ln(x)` - Natural logarithm
- `1/x` - Reciprocal
- `x³-3x` - Cubic polynomial

#### Multi-Function Plotting
1. Plot your first function using the **Plot** button
2. Enter a new equation
3. Click **Add** to overlay it on the same axes
4. Functions appear in different colors from your selected scheme

### 🎨 Style Tab

#### Color Schemes
- **Neon Dreams** - Vibrant neon colors for a futuristic look
- **Cyberpunk** - Electric cyan, magenta, and yellow
- **Ocean** - Cool blues and aqua tones
- **Galaxy** - Deep purples and cosmic colors
- **Fire** - Warm reds, oranges, and yellows
- **Forest** - Natural greens and earth tones
- **Sunset** - Beautiful warm sunset palette
- **Pastel** - Soft, gentle colors

#### Plot Styles
- **Line** - Continuous line plot (default)
- **Scatter** - Discrete points
- **Stem** - Vertical lines from x-axis
- **Step** - Step function visualization
- **Bar** - Bar chart representation

#### Grid Options
- **Show Grid** - Toggle main grid lines
- **Show Minor Grid** - Add finer grid divisions
- **Grid Alpha** - Adjust grid transparency
- **Show Axes** - Display x=0 and y=0 lines
- **Show Legend** - Display function labels

### ∫ Calculus Tab

#### Derivative Visualization
1. Check "Show Derivative"
2. Plot your function
3. The derivative appears as a dashed line

#### Tangent Lines
1. Check "Show Tangent Line"
2. Adjust the X value slider to move the tangent point
3. The tangent line and slope appear on the plot

#### Integration
1. Set integration bounds (Lower and Upper)
2. Check "Show Area Under Curve" to visualize
3. Click "Calculate Area" for numerical results
4. View both symbolic and numerical integration results

### 🎲 3D Plot Tab

#### Creating 3D Surfaces
1. Switch to "3D Surface" mode in Functions tab
2. Enter a function of x and y (e.g., `sin(sqrt(x**2 + y**2))`)
3. Click Plot to generate the surface

#### 3D Visualization Options
- **Surface** - Solid surface with color mapping
- **Wireframe** - See-through wire mesh
- **Contour** - Contour lines in 3D space

#### View Controls
- **Elevation** - Vertical viewing angle (-90° to 90°)
- **Azimuth** - Horizontal rotation (0° to 360°)

#### Pre-loaded 3D Functions
- **Ripple** - `sin(sqrt(x**2 + y**2))` - Circular waves
- **Saddle** - `x**2 - y**2` - Saddle point
- **Bowl** - `x**2 + y**2` - Paraboloid
- **Wave** - `sin(x) * cos(y)` - 2D wave pattern
- **Peaks** - Complex multi-peak function
- **Spiral** - Damped spiral pattern

### 🌀 Parametric Tab

#### Parametric Equations
Define x(t) and y(t) as functions of parameter t:
- x(t) = `cos(t)`
- y(t) = `sin(t)`
- Creates a circle when t goes from 0 to 2π

#### Famous Curves

| Curve | Description | t Range |
|-------|-------------|---------|
| **Circle** | Perfect circle | 0 to 2π |
| **Lissajous** | Figure-eight patterns | 0 to 2π |
| **Rose** | Flower-like curves | 0 to 2π |
| **Spiral** | Archimedean spiral | 0 to 6π |
| **Heart** | Heart shape | 0 to 2π |
| **Butterfly** | Butterfly curve | 0 to 12π |

### 🎬 Animation Tab

#### Animation Types

1. **Phase Shift**
   - Function moves horizontally
   - Creates wave-like motion
   - Best with periodic functions

2. **Amplitude**
   - Varies the amplitude over time
   - Creates pulsing effect
   - Great for sine waves

3. **Frequency**
   - Changes frequency dynamically
   - Creates morphing effects
   - Interesting with trigonometric functions

4. **Growing**
   - Draws the function progressively
   - Rainbow color gradient
   - Shows function construction

5. **Rotating 3D**
   - Automatically rotates 3D plots
   - 360° view of surfaces
   - Must be in 3D mode

#### Animation Controls
- **Speed** - Adjust animation speed (10-500ms)
- **Start/Stop** - Control animation playback
- **Save Animation** - Export as GIF file

## 🖱️ Interactive Features

### Mouse Interactions
- **Click on plot** - Marks a point and shows coordinates
- **Hover** - Displays current coordinates in toolbar
- **Scroll** - Zoom in/out (when using navigation toolbar)
- **Drag** - Pan the view (when using pan tool)

### Navigation Toolbar
Located below the plot area:
- **Home** - Reset to original view
- **Back/Forward** - Navigate through view history
- **Pan** - Click and drag to move
- **Zoom** - Rectangle zoom selection
- **Configure** - Adjust subplot parameters
- **Save** - Quick save plot

## 💾 Export Options

### Save Plot
Export your visualizations in multiple formats:
- **PNG** - High-quality raster image
- **PDF** - Vector format for publications
- **SVG** - Scalable vector graphics

### Export Data
- Save plot data as CSV
- Includes x,y coordinates
- Multiple functions in one file
- Ready for further analysis

### Save Animation
- Export animations as GIF
- Customizable frame rate
- Requires Pillow library

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save plot |
| `Ctrl+C` | Clear plot |
| `Ctrl+Q` | Quit application |
| `F11` | Toggle fullscreen |
| `Tab` | Navigate controls |

## 🧮 Mathematical Expression Syntax

### Basic Operations
- Addition: `x + 2`
- Subtraction: `x - 3`
- Multiplication: `2 * x` or `2*x`
- Division: `x / 2`
- Power: `x**2` or `x^2`

### Advanced Functions
- Square root: `sqrt(x)`
- Absolute value: `abs(x)`
- Factorial: `factorial(n)`
- Combinations: `binomial(n, k)`

### Constants
- Pi: `pi` (3.14159...)
- Euler's number: `E` (2.71828...)
- Golden ratio: `golden_ratio`

### Complex Examples
```python
# Damped oscillation
exp(-x/5) * sin(2*x)

# Gaussian distribution
exp(-x**2/2) / sqrt(2*pi)

# Interference pattern
sin(x) + sin(1.1*x)

# Polynomial
x**4 - 2*x**3 + x**2 - 3*x + 1
```

## 🎯 Tips and Tricks

### Performance Optimization
1. **Reduce Points** - Lower the points slider for complex functions
2. **Limit Range** - Use smaller x/y ranges for detailed views
3. **Disable Features** - Turn off grid/legend when not needed
4. **Close Other Plots** - Clear before plotting new functions

### Beautiful Visualizations
1. **Combine Functions** - Use Add button to create compositions
2. **Play with Colors** - Try different schemes for different moods
3. **Adjust Transparency** - Use grid alpha for subtle effects
4. **Enable Animations** - Bring your math to life

### Educational Use
1. **Calculus Classes** - Demonstrate derivatives and integrals
2. **Trigonometry** - Visualize periodic functions
3. **Linear Algebra** - Plot transformations
4. **Complex Analysis** - Visualize complex functions

## 🐛 Troubleshooting

### Common Issues

**Problem: Application won't start**
- Solution: Ensure Python 3.8+ is installed
- Check: `python --version`

**Problem: Missing module errors**
- Solution: Install required packages
- Run: `pip install matplotlib numpy sympy scipy`

**Problem: Plot doesn't appear**
- Check equation syntax
- Ensure valid x/y ranges
- Try a simple function like `x` or `sin(x)`

**Problem: 3D plot is slow**
- Reduce number of points
- Use wireframe instead of surface
- Close other applications

**Problem: Animation won't export**
- Install Pillow: `pip install pillow`
- Check file permissions
- Try shorter animations

## 📚 Examples Gallery

### Beautiful 2D Functions
```python
# Butterfly curve
sin(x) * (exp(cos(x)) - 2*cos(4*x) - sin(x/12)**5)

# Damped wave packet
exp(-x**2/10) * sin(5*x)

# Interference pattern
sin(10*x) * sin(x) / x  # (careful near x=0)
```

### Stunning 3D Surfaces
```python
# Mexican hat
(1 - (x**2 + y**2)/4) * exp(-(x**2 + y**2)/4)

# Double spiral
sin(5*sqrt(x**2+y**2)) / sqrt(x**2+y**2+1)

# Egg carton
sin(x) * sin(y)
```

### Parametric Art
```python
# Rhodonea curve
x(t) = cos(7*t) * cos(t)
y(t) = cos(7*t) * sin(t)

# Hypotrochoid
x(t) = 2*cos(t) + 5*cos(2*t/3)
y(t) = 2*sin(t) - 5*sin(2*t/3)
```

