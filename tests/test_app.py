"""Tests for Mathematics Visualiser.

The maths is checked against known answers, and the app itself is opened in a
real Tk window and driven through each feature. Error pop-ups are captured, so
a test fails if the app would have shown one.
"""

import math
import time
import tkinter as tk

import numpy as np
import pytest
import sympy as sp

from mathviz import app as appmod
from mathviz.app import compile_expression
from mathviz.symbolic import SymbolicWorker


# ---------------------------------------------------------------- the maths --

def test_constant_expression_broadcasts():
    x = np.linspace(-1, 1, 7)
    assert np.array_equal(compile_expression(sp.sympify("5"), sp.symbols("x"), x), np.full(7, 5.0))


def test_expression_values():
    x = np.array([0.0, math.pi / 2, math.pi])
    y = compile_expression(sp.sympify("sin(x)"), sp.symbols("x"), x)
    assert np.allclose(y, [0, 1, 0])


def test_two_variable_expression():
    X, Y = np.meshgrid([0.0, 1.0, 2.0], [0.0, 1.0])
    Z = compile_expression(sp.sympify("x**2 - y**2"), sp.symbols("x y"), X, Y)
    assert Z.shape == (2, 3) and np.allclose(Z, X**2 - Y**2)


@pytest.fixture(scope="session")
def worker():
    w = SymbolicWorker()
    w.start()
    yield w
    w.stop()


def test_symbolic_worker_exact_answers(worker):
    assert worker.integrate("x**2", "x", 0, 3) == ("ok", pytest.approx(9.0))
    assert worker.integrate("sin(x)", "x", 0, math.pi) == ("ok", pytest.approx(2.0))


def test_symbolic_worker_gives_up_and_recovers(worker):
    t = time.monotonic()
    status, _ = worker.integrate("sin(x**3)*exp(cos(x))", "x", 0, 1, timeout=1.0)
    assert status in ("timeout", "no closed form")
    assert time.monotonic() - t < 3.0
    # a fresh worker is ready for the next request
    assert worker.integrate("2*x", "x", 0, 1, timeout=30) == ("ok", pytest.approx(1.0))


def test_symbolic_worker_reports_bad_input(worker):
    assert worker.integrate("sin(", "x", 0, 1)[0] == "error"


# --------------------------------------------------------------- the window --

@pytest.fixture(scope="session")
def tk_root():
    try:
        root = tk.Tk()
    except tk.TclError as e:  # no display
        pytest.skip(f"no display: {e}")
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def gui(tk_root, worker, monkeypatch):
    popups = []
    for name in ("showerror", "showwarning", "showinfo"):
        monkeypatch.setattr(appmod.messagebox, name, lambda title, msg, n=name: popups.append((n, msg)))
    window = tk.Toplevel(tk_root)
    g = appmod.SuperMathGUI(window)
    g.symbolic.stop()
    g.symbolic = worker  # share one SymPy process across tests
    g.popups = popups
    window.update()
    yield g
    g.stop_animation()
    window.destroy()


def labels(g):
    return [line.get_label() for line in g.ax.lines]


def test_opens_with_demo_plot(gui):
    assert gui.root.title().startswith("Mathematics Visualiser")
    assert len(gui.ax.lines) >= 1
    assert gui.popups == []


@pytest.mark.parametrize("eq", ["sin(x)", "x**2", "exp(x)", "log(x)", "1/x", "x**3 - 3*x", "5", "abs(x) - 2"])
def test_plot_2d(gui, eq):
    gui.set_equation(eq)
    gui.plot_function()
    assert gui.popups == []
    assert f"y = {eq}" in labels(gui)


@pytest.mark.parametrize("style", ["line", "scatter", "stem", "step", "bar"])
def test_plot_styles(gui, style):
    gui.plot_style.set(style)
    gui.set_equation("sin(x)")
    gui.plot_function()
    assert gui.popups == []


def test_derivative_is_drawn_and_correct(gui):
    gui.set_equation("x**2")
    gui.show_derivatives.set(True)
    gui.plot_function()
    line = next(l for l in gui.ax.lines if l.get_label() == "f'(x)")
    x, dy = line.get_data()
    inner = slice(5, -5)  # np.gradient is one-sided at the ends
    assert np.allclose(dy[inner], 2 * x[inner], atol=1e-3)


def test_antiderivative_is_drawn_and_correct(gui):
    gui.set_equation("2*x")
    gui.int_lower.set(0)
    gui.show_integrals.set(True)
    gui.plot_function()
    line = next(l for l in gui.ax.lines if l.get_label().startswith("∫"))
    x, F = line.get_data()
    assert np.allclose(F, x**2, atol=1e-3)


def test_tangent_line(gui):
    gui.set_equation("x**2")
    gui.tangent_x.set(1.0)
    gui.show_tangent.set(True)
    gui.plot_function()
    assert "Tangent at x=1.00" in labels(gui)


@pytest.mark.parametrize("eq, lower, upper, expected", [
    ("x**2", 0, 3, 9.0),
    ("sin(x)", 0, math.pi, 2.0),
    ("exp(-x**2)", -2, 2, math.sqrt(math.pi) * math.erf(2)),
    ("5", 0, 2, 10.0),
])
def test_definite_integral(gui, eq, lower, upper, expected):
    gui.set_equation(eq)
    gui.int_lower.set(lower)
    gui.int_upper.set(upper)
    gui.calculate_area()
    assert gui.popups == []
    text = gui.results_text.get("1.0", "end")
    sym = float(text.split("Symbolic integral: ")[1].split()[0])
    num = float(text.split("Numerical integral: ")[1].split()[0])
    assert sym == pytest.approx(expected, abs=1e-5)
    assert num == pytest.approx(expected, abs=1e-5)


def test_integral_without_closed_form_still_reports_numeric(gui):
    gui.set_equation("sin(x**3)*exp(cos(x))")
    gui.int_lower.set(0)
    gui.int_upper.set(1)
    gui.calculate_area()
    assert gui.popups == []
    assert "Numerical integral:" in gui.results_text.get("1.0", "end")


def test_3d_replots_do_not_pile_up_axes(gui):
    gui.plot_mode.set("3D")
    gui.switch_plot_mode()
    for _ in range(3):
        gui.plot_function()
    assert gui.popups == []
    # one 3D axes plus one colourbar
    assert len(gui.fig.axes) == 2
    gui.plot_mode.set("2D")
    gui.switch_plot_mode()
    assert len(gui.fig.axes) == 1


@pytest.mark.parametrize("kind", ["surface", "wireframe", "contour"])
def test_3d_surface_kinds(gui, kind):
    gui.plot_mode.set("3D")
    gui.switch_plot_mode()
    gui.surface_type.set(kind)
    gui.plot_function()
    assert gui.popups == []


def test_parametric_curves(gui):
    gui.plot_mode.set("Parametric")
    gui.switch_plot_mode()
    for curve in [("Circle", "cos(t)", "sin(t)", 0, 2 * np.pi),
                  ("Heart", "16*sin(t)**3", "13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)", 0, 2 * np.pi)]:
        gui.set_parametric_curve(curve)
        gui.plot_function()
    assert gui.popups == []


def test_add_overlays_functions(gui):
    gui.clear_plot()
    gui.set_equation("sin(x)")
    gui.plot_function()
    gui.set_equation("cos(x)")
    gui.add_function()
    assert {"y = sin(x)", "y = cos(x)"} <= set(labels(gui))


def test_invalid_equation_shows_error(gui):
    gui.set_equation("sin(")
    gui.plot_function()
    assert gui.popups and gui.popups[0][0] == "showerror"


@pytest.mark.parametrize("kind", ["phase", "amplitude", "frequency", "growing"])
def test_animations_draw_user_function(gui, kind):
    # exp(x) used to be mangled by the phase animation's text substitution
    gui.set_equation("exp(-x**2)*cos(x)")
    gui.anim_type.set(kind)
    gui.start_animation()
    for frame in (0, 5, 60):
        gui.animation_obj._func(frame)
    assert gui.popups == []
    assert len(gui.ax.lines) >= 1
    gui.stop_animation()


def test_export_csv(gui, tmp_path, monkeypatch):
    out = tmp_path / "data.csv"
    monkeypatch.setattr(appmod.filedialog, "asksaveasfilename", lambda **kw: str(out))
    gui.set_equation("x**2")
    gui.plot_function()
    gui.export_data()
    text = out.read_text()
    assert "# Equation: x**2" in text and "x,y" in text


def test_save_png(gui, tmp_path, monkeypatch):
    out = tmp_path / "plot.png"
    monkeypatch.setattr(appmod.filedialog, "asksaveasfilename", lambda **kw: str(out))
    gui.save_plot()
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_save_animation_gif(gui, tmp_path, monkeypatch):
    # used to hang forever: the animation had no frame count to save
    out = tmp_path / "anim.gif"
    monkeypatch.setattr(appmod.filedialog, "asksaveasfilename", lambda **kw: str(out))
    gui.set_equation("sin(x)")
    gui.anim_type.set("phase")
    gui.start_animation()
    gui.save_animation()
    assert gui.popups and gui.popups[0][0] == "showinfo"
    assert out.read_bytes()[:6] in (b"GIF87a", b"GIF89a")


def test_rotating_3d(gui):
    gui.plot_mode.set("3D")
    gui.switch_plot_mode()
    gui.plot_function()
    gui.anim_type.set("rotate3d")
    gui.start_animation()
    gui.animation_obj._func(20)
    assert round(gui.ax.azim) == 40
