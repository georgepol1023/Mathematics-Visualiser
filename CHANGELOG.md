# Changelog

## 1.0.0

First public release.

- **Install in one step.** A Windows `.exe` built for every release (81 MB, down from 328 MB), or `pipx install` on any platform, then run `mathviz`. The code is now a Python package with a `pyproject.toml`.
- **Show Integral** now draws the running integral ∫f dx from the lower bound. Before, the checkbox did nothing.
- **Exact integrals never freeze the window.** SymPy now runs in a separate process. If it hasn't found an exact answer within 3 seconds, it stops, and the app shows the numerical result and says so. Before, some integrals (for example `sin(x**3)*exp(cos(x))`) locked the app up.
- **Animations use your own function.** Frequency used to always animate `sin(x)`. Phase shift used to break any function containing a name with an `x` in it, such as `exp(x)`.
- Fixed: **Show Derivative** never drew the derivative.
- Fixed: **Save Animation** never finished. It now saves a 4-second GIF.
- Fixed: the **stem** plot style always showed an error.
- Fixed: constant functions such as `5` showed an error.
- Fixed: repeated 3D plots added a new colourbar each time, and switching between 2D and 3D stacked old axes behind the new ones.
- Fixed: an empty legend box on parametric plots, and tab names cut off in the control panel.
- 43 automated tests, run on Windows, macOS and Linux for every change.

## 0.2 (November 2025)

- Calculus tab (tangent line, area under the curve, exact and numerical integrals), 3D surfaces, parametric curves, animations and GIF/PNG/CSV export, eight colour schemes.

## 0.1 (November 2025)

- First version: 2D function plotter.
