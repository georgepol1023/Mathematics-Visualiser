import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import tkinter.font as tkfont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
from scipy import integrate
import colorsys
import random
from datetime import datetime
import json
import os

class SuperMathGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Super Math Visualization Studio ✨")
        self.root.geometry("1600x900")
        
        # Set dark theme
        self.setup_dark_theme()
        
        # Animation variables
        self.is_animating = False
        self.animation_obj = None
        self.animation_speed = 50
        
        # History tracking
        self.plot_history = []
        self.current_functions = []
        
        # Color schemes
        self.color_schemes = {
            "Neon Dreams": ['#FF006E', '#FB5607', '#FFBE0B', '#8338EC', '#3A86FF'],
            "Cyberpunk": ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF0080'],
            "Sunset": ['#FF6B6B', '#FFE66D', '#4ECDC4', '#95E1D3', '#F38181'],
            "Ocean": ['#0077B6', '#00B4D8', '#90E0EF', '#CAF0F8', '#03045E'],
            "Forest": ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#95D5B2'],
            "Galaxy": ['#7209B7', '#560BAD', '#480CA8', '#3A0CA3', '#3F37C9'],
            "Fire": ['#FF0000', '#FF4500', '#FF6347', '#FF7F50', '#FFA500'],
            "Pastel": ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF']
        }
        self.current_scheme = "Neon Dreams"
        
        # Variables
        self.setup_variables()
        
        # Create main UI
        self.create_ui()
        
        # Initial plot
        self.reset_and_demo()
        
    def setup_dark_theme(self):
        """Setup beautiful dark theme"""
        self.root.configure(bg='#1a1a2e')
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        dark_bg = '#1a1a2e'
        darker_bg = '#16213e'
        accent = '#0f3460'
        highlight = '#e94560'
        text_color = '#ffffff'
        
        style.configure('Dark.TFrame', background=dark_bg)
        style.configure('Dark.TLabel', background=dark_bg, foreground=text_color, font=('Arial', 11))
        style.configure('Dark.TButton', background=accent, foreground=text_color, 
                       borderwidth=0, focuscolor='none', font=('Arial', 11, 'bold'))
        style.map('Dark.TButton',
                 background=[('active', highlight), ('pressed', '#c23050')])
        
        style.configure('Accent.TButton', background=highlight, foreground=text_color,
                       borderwidth=0, focuscolor='none', font=('Arial', 11, 'bold'))
        style.map('Accent.TButton',
                 background=[('active', '#ff5070'), ('pressed', '#c23050')])
        
        style.configure('Dark.TCheckbutton', background=dark_bg, foreground=text_color,
                       focuscolor='none', font=('Arial', 11))
        style.configure('Dark.TRadiobutton', background=dark_bg, foreground=text_color,
                       focuscolor='none', font=('Arial', 11))
        style.configure('Dark.TLabelframe', background=dark_bg, foreground=text_color,
                       borderwidth=2, relief='groove')
        style.configure('Dark.TLabelframe.Label', background=dark_bg, foreground=text_color,
                       font=('Arial', 12, 'bold'))
        
        # Configure Combobox
        style.configure('Dark.TCombobox', fieldbackground=darker_bg, background=accent,
                       foreground=text_color, borderwidth=0)
        style.map('Dark.TCombobox', fieldbackground=[('readonly', darker_bg)])
        
        # Configure Scale
        style.configure('Dark.Horizontal.TScale', background=dark_bg, troughcolor=darker_bg,
                       borderwidth=0, lightcolor=accent, darkcolor=dark_bg)
        
    def setup_variables(self):
        """Initialize all variables"""
        self.x_min = tk.DoubleVar(value=-10)
        self.x_max = tk.DoubleVar(value=10)
        self.y_min = tk.DoubleVar(value=-10)
        self.y_max = tk.DoubleVar(value=10)
        self.num_points = tk.IntVar(value=1000)
        
        self.show_grid = tk.BooleanVar(value=True)
        self.show_legend = tk.BooleanVar(value=True)
        self.show_axes = tk.BooleanVar(value=True)
        self.show_minor_grid = tk.BooleanVar(value=False)
        self.dark_mode = tk.BooleanVar(value=True)
        self.show_derivatives = tk.BooleanVar(value=False)
        self.show_integrals = tk.BooleanVar(value=False)
        self.show_tangent = tk.BooleanVar(value=False)
        self.show_area = tk.BooleanVar(value=False)
        
        self.plot_style = tk.StringVar(value="line")
        self.line_width = tk.DoubleVar(value=2.0)
        self.marker_size = tk.DoubleVar(value=5.0)
        self.grid_alpha = tk.DoubleVar(value=0.3)
        
        self.plot_mode = tk.StringVar(value="2D")
        self.current_equation = tk.StringVar(value="sin(x) * cos(x/2)")
        
        # 3D variables
        self.z_equation = tk.StringVar(value="sin(sqrt(x**2 + y**2))")
        self.elevation = tk.DoubleVar(value=30)
        self.azimuth = tk.DoubleVar(value=45)
        
        # Parametric variables
        self.param_x = tk.StringVar(value="cos(t) * (1 + 0.5*cos(5*t))")
        self.param_y = tk.StringVar(value="sin(t) * (1 + 0.5*cos(5*t))")
        self.t_min = tk.DoubleVar(value=0)
        self.t_max = tk.DoubleVar(value=2*np.pi)
        
    def create_ui(self):
        """Create the main user interface"""
        # Create main container
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        left_panel = ttk.Frame(main_container, style='Dark.TFrame', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel for plot
        right_panel = ttk.Frame(main_container, style='Dark.TFrame')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create controls in left panel
        self.create_controls(left_panel)
        
        # Create plot in right panel
        self.create_plot_area(right_panel)
        
    def create_controls(self, parent):
        """Create control panel"""
        # Title
        title_label = ttk.Label(parent, text="🎨 Control Studio", 
                               font=('Arial', 18, 'bold'), style='Dark.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Function tab
        func_tab = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(func_tab, text="📈 Functions")
        self.create_function_controls(func_tab)
        
        # Style tab
        style_tab = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(style_tab, text="🎨 Style")
        self.create_style_controls(style_tab)
        
        # Calculus tab
        calc_tab = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(calc_tab, text="∫ Calculus")
        self.create_calculus_controls(calc_tab)
        
        # 3D tab
        three_d_tab = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(three_d_tab, text="🎲 3D Plot")
        self.create_3d_controls(three_d_tab)
        
        # Parametric tab
        param_tab = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(param_tab, text="🌀 Parametric")
        self.create_parametric_controls(param_tab)
        
        # Animation tab
        anim_tab = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(anim_tab, text="🎬 Animation")
        self.create_animation_controls(anim_tab)
        
    def create_function_controls(self, parent):
        """Create function input controls"""
        # Mode selection
        mode_frame = ttk.LabelFrame(parent, text="Plot Mode", style='Dark.TLabelframe')
        mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Radiobutton(mode_frame, text="2D Plot", variable=self.plot_mode,
                       value="2D", style='Dark.TRadiobutton',
                       command=self.switch_plot_mode).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="3D Surface", variable=self.plot_mode,
                       value="3D", style='Dark.TRadiobutton',
                       command=self.switch_plot_mode).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Parametric", variable=self.plot_mode,
                       value="Parametric", style='Dark.TRadiobutton',
                       command=self.switch_plot_mode).pack(side=tk.LEFT, padx=5)
        
        # Equation input
        eq_frame = ttk.LabelFrame(parent, text="Function Equation", style='Dark.TLabelframe')
        eq_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.equation_text = tk.Text(eq_frame, height=3, width=40, bg='#16213e', 
                                    fg='white', insertbackground='white',
                                    font=('Courier', 11))
        self.equation_text.pack(padx=5, pady=5)
        self.equation_text.insert('1.0', self.current_equation.get())
        
        # Quick functions
        quick_frame = ttk.LabelFrame(parent, text="Quick Functions", style='Dark.TLabelframe')
        quick_frame.pack(fill=tk.X, padx=5, pady=5)
        
        quick_funcs = [
            ("sin(x)", "sin(x)"),
            ("x²", "x**2"),
            ("eˣ", "exp(x)"),
            ("ln(x)", "log(x)"),
            ("1/x", "1/x"),
            ("x³-3x", "x**3 - 3*x")
        ]
        
        for i, (label, func) in enumerate(quick_funcs):
            btn = ttk.Button(quick_frame, text=label, style='Dark.TButton',
                           command=lambda f=func: self.set_equation(f))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2, sticky='ew')
        
        # Range controls
        range_frame = ttk.LabelFrame(parent, text="Plot Range", style='Dark.TLabelframe')
        range_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # X range
        ttk.Label(range_frame, text="X Range:", style='Dark.TLabel').grid(row=0, column=0, sticky='w', padx=5)
        x_min_spin = ttk.Spinbox(range_frame, from_=-100, to=100, textvariable=self.x_min,
                                 width=10, increment=1)
        x_min_spin.grid(row=0, column=1, padx=2)
        ttk.Label(range_frame, text="to", style='Dark.TLabel').grid(row=0, column=2)
        x_max_spin = ttk.Spinbox(range_frame, from_=-100, to=100, textvariable=self.x_max,
                                 width=10, increment=1)
        x_max_spin.grid(row=0, column=3, padx=2)
        
        # Y range
        ttk.Label(range_frame, text="Y Range:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', padx=5)
        y_min_spin = ttk.Spinbox(range_frame, from_=-100, to=100, textvariable=self.y_min,
                                 width=10, increment=1)
        y_min_spin.grid(row=1, column=1, padx=2)
        ttk.Label(range_frame, text="to", style='Dark.TLabel').grid(row=1, column=2)
        y_max_spin = ttk.Spinbox(range_frame, from_=-100, to=100, textvariable=self.y_max,
                                 width=10, increment=1)
        y_max_spin.grid(row=1, column=3, padx=2)
        
        # Points slider
        ttk.Label(range_frame, text="Points:", style='Dark.TLabel').grid(row=2, column=0, sticky='w', padx=5)
        points_scale = ttk.Scale(range_frame, from_=100, to=5000, variable=self.num_points,
                                orient='horizontal', style='Dark.Horizontal.TScale')
        points_scale.grid(row=2, column=1, columnspan=3, sticky='ew', padx=5)
        
        # Action buttons
        btn_frame = ttk.Frame(parent, style='Dark.TFrame')
        btn_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(btn_frame, text="🎯 Plot", command=self.plot_function,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="➕ Add", command=self.add_function,
                  style='Dark.TButton').pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="🗑️ Clear", command=self.clear_plot,
                  style='Dark.TButton').pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
    def create_style_controls(self, parent):
        """Create style customization controls"""
        # Color scheme
        color_frame = ttk.LabelFrame(parent, text="Color Schemes", style='Dark.TLabelframe')
        color_frame.pack(fill=tk.X, padx=5, pady=5)
        
        scheme_combo = ttk.Combobox(color_frame, values=list(self.color_schemes.keys()),
                                   state='readonly', style='Dark.TCombobox')
        scheme_combo.set(self.current_scheme)
        scheme_combo.pack(padx=5, pady=5, fill=tk.X)
        scheme_combo.bind('<<ComboboxSelected>>', self.change_color_scheme)
        
        # Line style
        line_frame = ttk.LabelFrame(parent, text="Line Style", style='Dark.TLabelframe')
        line_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(line_frame, text="Style:", style='Dark.TLabel').grid(row=0, column=0, sticky='w', padx=5)
        style_combo = ttk.Combobox(line_frame, textvariable=self.plot_style,
                                  values=['line', 'scatter', 'stem', 'step', 'bar'],
                                  state='readonly', style='Dark.TCombobox', width=15)
        style_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(line_frame, text="Width:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', padx=5)
        width_scale = ttk.Scale(line_frame, from_=0.5, to=5, variable=self.line_width,
                               orient='horizontal', style='Dark.Horizontal.TScale')
        width_scale.grid(row=1, column=1, sticky='ew', padx=5)
        
        ttk.Label(line_frame, text="Markers:", style='Dark.TLabel').grid(row=2, column=0, sticky='w', padx=5)
        marker_scale = ttk.Scale(line_frame, from_=1, to=20, variable=self.marker_size,
                                orient='horizontal', style='Dark.Horizontal.TScale')
        marker_scale.grid(row=2, column=1, sticky='ew', padx=5)
        
        # Grid options
        grid_frame = ttk.LabelFrame(parent, text="Grid Options", style='Dark.TLabelframe')
        grid_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Checkbutton(grid_frame, text="Show Grid", variable=self.show_grid,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5)
        ttk.Checkbutton(grid_frame, text="Show Minor Grid", variable=self.show_minor_grid,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5)
        ttk.Checkbutton(grid_frame, text="Show Legend", variable=self.show_legend,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5)
        ttk.Checkbutton(grid_frame, text="Show Axes", variable=self.show_axes,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5)
        
        ttk.Label(grid_frame, text="Grid Alpha:", style='Dark.TLabel').pack(anchor='w', padx=5)
        alpha_scale = ttk.Scale(grid_frame, from_=0, to=1, variable=self.grid_alpha,
                               orient='horizontal', style='Dark.Horizontal.TScale')
        alpha_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Theme toggle
        theme_frame = ttk.LabelFrame(parent, text="Theme", style='Dark.TLabelframe')
        theme_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Checkbutton(theme_frame, text="Dark Mode", variable=self.dark_mode,
                       style='Dark.TCheckbutton', command=self.toggle_theme).pack(padx=5, pady=5)
        
    def create_calculus_controls(self, parent):
        """Create calculus feature controls"""
        # Features
        calc_frame = ttk.LabelFrame(parent, text="Calculus Features", style='Dark.TLabelframe')
        calc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Checkbutton(calc_frame, text="Show Derivative", variable=self.show_derivatives,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5, pady=2)
        ttk.Checkbutton(calc_frame, text="Show Integral", variable=self.show_integrals,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5, pady=2)
        ttk.Checkbutton(calc_frame, text="Show Tangent Line", variable=self.show_tangent,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5, pady=2)
        ttk.Checkbutton(calc_frame, text="Show Area Under Curve", variable=self.show_area,
                       style='Dark.TCheckbutton').pack(anchor='w', padx=5, pady=2)
        
        # Tangent point
        tangent_frame = ttk.LabelFrame(parent, text="Tangent Point", style='Dark.TLabelframe')
        tangent_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.tangent_x = tk.DoubleVar(value=0)
        ttk.Label(tangent_frame, text="X value:", style='Dark.TLabel').pack(side=tk.LEFT, padx=5)
        tangent_scale = ttk.Scale(tangent_frame, from_=-10, to=10, variable=self.tangent_x,
                                 orient='horizontal', style='Dark.Horizontal.TScale')
        tangent_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Integration bounds
        int_frame = ttk.LabelFrame(parent, text="Integration Bounds", style='Dark.TLabelframe')
        int_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.int_lower = tk.DoubleVar(value=-2)
        self.int_upper = tk.DoubleVar(value=2)
        
        ttk.Label(int_frame, text="Lower:", style='Dark.TLabel').grid(row=0, column=0, padx=5)
        lower_spin = ttk.Spinbox(int_frame, from_=-100, to=100, textvariable=self.int_lower,
                                width=10, increment=0.5)
        lower_spin.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(int_frame, text="Upper:", style='Dark.TLabel').grid(row=1, column=0, padx=5)
        upper_spin = ttk.Spinbox(int_frame, from_=-100, to=100, textvariable=self.int_upper,
                                width=10, increment=0.5)
        upper_spin.grid(row=1, column=1, padx=5, pady=2)
        
        # Calculate button
        ttk.Button(int_frame, text="Calculate Area", command=self.calculate_area,
                  style='Dark.TButton').grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        
        # Results display
        results_frame = ttk.LabelFrame(parent, text="Results", style='Dark.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(results_frame, height=8, bg='#16213e', fg='white',
                                   font=('Courier', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_3d_controls(self, parent):
        """Create 3D plot controls"""
        # 3D equation
        eq_frame = ttk.LabelFrame(parent, text="3D Surface Equation z = f(x,y)", style='Dark.TLabelframe')
        eq_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.z_text = tk.Text(eq_frame, height=3, width=40, bg='#16213e',
                             fg='white', insertbackground='white',
                             font=('Courier', 11))
        self.z_text.pack(padx=5, pady=5)
        self.z_text.insert('1.0', self.z_equation.get())
        
        # Quick 3D functions
        quick_3d = ttk.LabelFrame(parent, text="Quick 3D Functions", style='Dark.TLabelframe')
        quick_3d.pack(fill=tk.X, padx=5, pady=5)
        
        functions_3d = [
            ("Ripple", "sin(sqrt(x**2 + y**2))"),
            ("Saddle", "x**2 - y**2"),
            ("Bowl", "x**2 + y**2"),
            ("Wave", "sin(x) * cos(y)"),
            ("Peaks", "3*(1-x)**2*exp(-(x**2)-(y+1)**2) - 10*(x/5-x**3-y**5)*exp(-x**2-y**2) - 1/3*exp(-(x+1)**2-y**2)"),
            ("Spiral", "sin(5*sqrt(x**2+y**2)) / sqrt(x**2+y**2+1)")
        ]
        
        for i, (label, func) in enumerate(functions_3d):
            btn = ttk.Button(quick_3d, text=label, style='Dark.TButton',
                           command=lambda f=func: self.set_3d_equation(f))
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky='ew')
        
        # View controls
        view_frame = ttk.LabelFrame(parent, text="View Angles", style='Dark.TLabelframe')
        view_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(view_frame, text="Elevation:", style='Dark.TLabel').pack(anchor='w', padx=5)
        elev_scale = ttk.Scale(view_frame, from_=-90, to=90, variable=self.elevation,
                              orient='horizontal', style='Dark.Horizontal.TScale')
        elev_scale.pack(fill=tk.X, padx=5)
        
        ttk.Label(view_frame, text="Azimuth:", style='Dark.TLabel').pack(anchor='w', padx=5)
        azim_scale = ttk.Scale(view_frame, from_=0, to=360, variable=self.azimuth,
                              orient='horizontal', style='Dark.Horizontal.TScale')
        azim_scale.pack(fill=tk.X, padx=5)
        
        # 3D style
        style_3d = ttk.LabelFrame(parent, text="3D Style", style='Dark.TLabelframe')
        style_3d.pack(fill=tk.X, padx=5, pady=5)
        
        self.surface_type = tk.StringVar(value="surface")
        ttk.Radiobutton(style_3d, text="Surface", variable=self.surface_type,
                       value="surface", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        ttk.Radiobutton(style_3d, text="Wireframe", variable=self.surface_type,
                       value="wireframe", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        ttk.Radiobutton(style_3d, text="Contour", variable=self.surface_type,
                       value="contour", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        
    def create_parametric_controls(self, parent):
        """Create parametric plot controls"""
        # Parametric equations
        param_frame = ttk.LabelFrame(parent, text="Parametric Equations", style='Dark.TLabelframe')
        param_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(param_frame, text="x(t) =", style='Dark.TLabel').grid(row=0, column=0, padx=5, pady=2)
        self.x_param_entry = tk.Entry(param_frame, textvariable=self.param_x,
                                      bg='#16213e', fg='white', insertbackground='white',
                                      font=('Courier', 10), width=30)
        self.x_param_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(param_frame, text="y(t) =", style='Dark.TLabel').grid(row=1, column=0, padx=5, pady=2)
        self.y_param_entry = tk.Entry(param_frame, textvariable=self.param_y,
                                      bg='#16213e', fg='white', insertbackground='white',
                                      font=('Courier', 10), width=30)
        self.y_param_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Parameter range
        t_frame = ttk.LabelFrame(parent, text="Parameter t Range", style='Dark.TLabelframe')
        t_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(t_frame, text="t min:", style='Dark.TLabel').grid(row=0, column=0, padx=5)
        t_min_spin = ttk.Spinbox(t_frame, from_=-100, to=100, textvariable=self.t_min,
                                width=10, increment=0.5)
        t_min_spin.grid(row=0, column=1, padx=5)
        
        ttk.Label(t_frame, text="t max:", style='Dark.TLabel').grid(row=1, column=0, padx=5)
        t_max_spin = ttk.Spinbox(t_frame, from_=-100, to=100, textvariable=self.t_max,
                                width=10, increment=0.5)
        t_max_spin.grid(row=1, column=1, padx=5)
        
        # Quick parametric curves
        curves_frame = ttk.LabelFrame(parent, text="Famous Curves", style='Dark.TLabelframe')
        curves_frame.pack(fill=tk.X, padx=5, pady=5)
        
        curves = [
            ("Circle", "cos(t)", "sin(t)", 0, 2*np.pi),
            ("Lissajous", "sin(3*t)", "sin(4*t)", 0, 2*np.pi),
            ("Rose", "cos(5*t)*cos(t)", "cos(5*t)*sin(t)", 0, 2*np.pi),
            ("Spiral", "t*cos(t)", "t*sin(t)", 0, 6*np.pi),
            ("Heart", "16*sin(t)**3", "13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)", 0, 2*np.pi),
            ("Butterfly", "sin(t)*(exp(cos(t))-2*cos(4*t)-sin(t/12)**5)", 
             "cos(t)*(exp(cos(t))-2*cos(4*t)-sin(t/12)**5)", 0, 12*np.pi)
        ]
        
        for i, curve in enumerate(curves):
            name = curve[0]
            btn = ttk.Button(curves_frame, text=name, style='Dark.TButton',
                           command=lambda c=curve: self.set_parametric_curve(c))
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky='ew')
            
    def create_animation_controls(self, parent):
        """Create animation controls"""
        # Animation settings
        anim_frame = ttk.LabelFrame(parent, text="Animation Settings", style='Dark.TLabelframe')
        anim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(anim_frame, text="Speed (ms):", style='Dark.TLabel').pack(anchor='w', padx=5)
        self.anim_speed = tk.IntVar(value=50)
        speed_scale = ttk.Scale(anim_frame, from_=10, to=500, variable=self.anim_speed,
                               orient='horizontal', style='Dark.Horizontal.TScale')
        speed_scale.pack(fill=tk.X, padx=5)
        
        # Animation types
        type_frame = ttk.LabelFrame(parent, text="Animation Type", style='Dark.TLabelframe')
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.anim_type = tk.StringVar(value="phase")
        ttk.Radiobutton(type_frame, text="Phase Shift", variable=self.anim_type,
                       value="phase", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        ttk.Radiobutton(type_frame, text="Amplitude", variable=self.anim_type,
                       value="amplitude", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        ttk.Radiobutton(type_frame, text="Frequency", variable=self.anim_type,
                       value="frequency", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        ttk.Radiobutton(type_frame, text="Growing", variable=self.anim_type,
                       value="growing", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        ttk.Radiobutton(type_frame, text="Rotating 3D", variable=self.anim_type,
                       value="rotate3d", style='Dark.TRadiobutton').pack(anchor='w', padx=5)
        
        # Control buttons
        btn_frame = ttk.Frame(parent, style='Dark.TFrame')
        btn_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="▶️ Start", command=self.start_animation,
                                   style='Accent.TButton')
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.stop_btn = ttk.Button(btn_frame, text="⏸️ Stop", command=self.stop_animation,
                                  style='Dark.TButton', state='disabled')
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Export controls
        export_frame = ttk.LabelFrame(parent, text="Export", style='Dark.TLabelframe')
        export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(export_frame, text="💾 Save Plot", command=self.save_plot,
                  style='Dark.TButton').pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(export_frame, text="📊 Export Data", command=self.export_data,
                  style='Dark.TButton').pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(export_frame, text="🎥 Save Animation", command=self.save_animation,
                  style='Dark.TButton').pack(fill=tk.X, padx=5, pady=2)
        
    def create_plot_area(self, parent):
        """Create the plot area with toolbar"""
        # Title
        title_frame = ttk.Frame(parent, style='Dark.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.plot_title = ttk.Label(title_frame, text="✨ Mathematical Visualization ✨",
                                   font=('Arial', 20, 'bold'), style='Dark.TLabel')
        self.plot_title.pack()
        
        # Create figure with dark style
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(10, 8), facecolor='#1a1a2e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#16213e')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        
        # Create toolbar frame
        toolbar_frame = ttk.Frame(parent, style='Dark.TFrame')
        toolbar_frame.pack(fill=tk.X)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
        # Pack canvas
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bind events for interactivity
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_hover)
        
    def set_equation(self, equation):
        """Set the equation in the text widget"""
        self.equation_text.delete('1.0', tk.END)
        self.equation_text.insert('1.0', equation)
        
    def set_3d_equation(self, equation):
        """Set the 3D equation"""
        self.z_text.delete('1.0', tk.END)
        self.z_text.insert('1.0', equation)
        
    def set_parametric_curve(self, curve):
        """Set parametric curve"""
        _, x_eq, y_eq, t_min, t_max = curve
        self.param_x.set(x_eq)
        self.param_y.set(y_eq)
        self.t_min.set(t_min)
        self.t_max.set(t_max)
        
    def switch_plot_mode(self):
        """Switch between 2D, 3D, and parametric modes"""
        mode = self.plot_mode.get()
        self.clear_plot()
        
        if mode == "3D":
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax = self.fig.add_subplot(111)
        
        self.ax.set_facecolor('#16213e' if self.dark_mode.get() else 'white')
        self.canvas.draw()
        
    def plot_function(self):
        """Main plotting function"""
        try:
            mode = self.plot_mode.get()
            
            if mode == "2D":
                self.plot_2d()
            elif mode == "3D":
                self.plot_3d()
            elif mode == "Parametric":
                self.plot_parametric()
                
        except Exception as e:
            messagebox.showerror("Error", f"Plotting error: {str(e)}")
            
    def plot_2d(self):
        """Plot 2D function"""
        # Get equation
        equation = self.equation_text.get('1.0', tk.END).strip()
        if not equation:
            return
            
        # Generate data
        x = np.linspace(self.x_min.get(), self.x_max.get(), self.num_points.get())
        
        try:
            # Parse and evaluate equation
            x_sym = sp.symbols('x')
            expr = sp.sympify(equation)
            func = sp.lambdify(x_sym, expr, modules=['numpy'])
            y = func(x)
            
            # Clear and setup axes
            self.ax.clear()
            
            # Get color from scheme
            colors = self.color_schemes[self.current_scheme]
            color = colors[len(self.current_functions) % len(colors)]
            
            # Plot based on style
            style = self.plot_style.get()
            if style == 'line':
                self.ax.plot(x, y, color=color, linewidth=self.line_width.get(),
                           label=f"y = {equation}")
            elif style == 'scatter':
                self.ax.scatter(x[::10], y[::10], color=color, s=self.marker_size.get()**2,
                              label=f"y = {equation}", alpha=0.6)
            elif style == 'stem':
                self.ax.stem(x[::20], y[::20], linefmt=color, markerfmt=f'{color}o',
                           label=f"y = {equation}")
            elif style == 'step':
                self.ax.step(x, y, color=color, linewidth=self.line_width.get(),
                           label=f"y = {equation}")
            elif style == 'bar':
                self.ax.bar(x[::50], y[::50], color=color, alpha=0.6,
                          label=f"y = {equation}")
            
            # Add calculus features if enabled
            if self.show_derivatives.get():
                self.plot_derivative(x, func, color)
                
            if self.show_tangent.get():
                self.plot_tangent_line(x, func, expr, x_sym, color)
                
            if self.show_area.get():
                self.plot_area_under_curve(x, y, color)
                
            # Styling
            self.apply_plot_styling()
            
            # Store function for history
            self.current_functions.append((equation, x, y))
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid equation: {str(e)}")
            
    def plot_3d(self):
        """Plot 3D surface"""
        equation = self.z_text.get('1.0', tk.END).strip()
        if not equation:
            return
            
        try:
            # Generate mesh
            x = np.linspace(self.x_min.get(), self.x_max.get(), 100)
            y = np.linspace(self.y_min.get(), self.y_max.get(), 100)
            X, Y = np.meshgrid(x, y)
            
            # Evaluate equation
            x_sym, y_sym = sp.symbols('x y')
            expr = sp.sympify(equation)
            func = sp.lambdify((x_sym, y_sym), expr, modules=['numpy'])
            Z = func(X, Y)
            
            # Clear axes
            self.ax.clear()
            
            # Plot based on surface type
            surface_type = self.surface_type.get()
            if surface_type == "surface":
                surf = self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8,
                                           edgecolor='none', antialiased=True)
                self.fig.colorbar(surf, ax=self.ax, shrink=0.5)
            elif surface_type == "wireframe":
                self.ax.plot_wireframe(X, Y, Z, color='cyan', alpha=0.5)
            elif surface_type == "contour":
                contour = self.ax.contour3D(X, Y, Z, 20, cmap='rainbow')
                self.fig.colorbar(contour, ax=self.ax, shrink=0.5)
                
            # Set labels and viewing angle
            self.ax.set_xlabel('X', fontsize=12)
            self.ax.set_ylabel('Y', fontsize=12)
            self.ax.set_zlabel('Z', fontsize=12)
            self.ax.view_init(elev=self.elevation.get(), azim=self.azimuth.get())
            
            self.ax.set_title(f"z = {equation}", fontsize=14, color='white')
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"3D plotting error: {str(e)}")
            
    def plot_parametric(self):
        """Plot parametric curve"""
        try:
            # Generate parameter values
            t = np.linspace(self.t_min.get(), self.t_max.get(), self.num_points.get())
            
            # Parse equations
            t_sym = sp.symbols('t')
            x_expr = sp.sympify(self.param_x.get())
            y_expr = sp.sympify(self.param_y.get())
            
            x_func = sp.lambdify(t_sym, x_expr, modules=['numpy'])
            y_func = sp.lambdify(t_sym, y_expr, modules=['numpy'])
            
            x = x_func(t)
            y = y_func(t)
            
            # Clear and plot
            self.ax.clear()
            
            # Create gradient color effect
            colors = plt.cm.rainbow(np.linspace(0, 1, len(t)))
            for i in range(len(t)-1):
                self.ax.plot(x[i:i+2], y[i:i+2], color=colors[i], linewidth=2)
                
            # Add direction arrows
            arrow_indices = np.linspace(0, len(t)-1, 10, dtype=int)
            for idx in arrow_indices[:-1]:
                dx = x[idx+5] - x[idx]
                dy = y[idx+5] - y[idx]
                self.ax.arrow(x[idx], y[idx], dx*0.1, dy*0.1,
                            head_width=0.05, head_length=0.05,
                            fc='yellow', ec='yellow', alpha=0.7)
                            
            self.ax.set_title(f"Parametric: x(t), y(t)", fontsize=14, color='white')
            self.ax.set_xlabel("x(t)", fontsize=12)
            self.ax.set_ylabel("y(t)", fontsize=12)
            
            self.apply_plot_styling()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Parametric plotting error: {str(e)}")
            
    def plot_derivative(self, x, func, color):
        """Plot the derivative of the function"""
        try:
            # Numerical derivative
            dx = x[1] - x[0]
            y = func(x)
            dy = np.gradient(y, dx)
            
            # Plot with modified color
            r, g, b = plt.colors.to_rgb(color)
            deriv_color = (min(1, r*1.3), min(1, g*0.7), min(1, b*0.7))
            
            self.ax.plot(x, dy, '--', color=deriv_color, linewidth=self.line_width.get()*0.7,
                        label="f'(x)", alpha=0.7)
                        
        except Exception:
            pass
            
    def plot_tangent_line(self, x, func, expr, x_sym, color):
        """Plot tangent line at specified point"""
        try:
            # Get tangent point
            x_t = self.tangent_x.get()
            
            # Calculate derivative symbolically
            deriv = sp.diff(expr, x_sym)
            deriv_func = sp.lambdify(x_sym, deriv, modules=['numpy'])
            
            # Calculate slope and point
            y_t = func(x_t)
            slope = deriv_func(x_t)
            
            # Generate tangent line
            x_range = np.array([self.x_min.get(), self.x_max.get()])
            y_tangent = slope * (x_range - x_t) + y_t
            
            # Plot tangent line and point
            self.ax.plot(x_range, y_tangent, 'r--', linewidth=2,
                        label=f"Tangent at x={x_t:.2f}")
            self.ax.plot(x_t, y_t, 'ro', markersize=8)
            
            # Add annotation
            self.ax.annotate(f"Slope: {slope:.2f}", 
                           xy=(x_t, y_t), xytext=(x_t+1, y_t+1),
                           arrowprops=dict(arrowstyle='->', color='red'),
                           fontsize=10, color='red')
                           
        except Exception:
            pass
            
    def plot_area_under_curve(self, x, y, color):
        """Shade area under curve"""
        try:
            # Get integration bounds
            lower = self.int_lower.get()
            upper = self.int_upper.get()
            
            # Find indices within bounds
            mask = (x >= lower) & (x <= upper)
            x_fill = x[mask]
            y_fill = y[mask]
            
            # Fill area
            self.ax.fill_between(x_fill, y_fill, alpha=0.3, color=color,
                               label=f"Area [{lower:.1f}, {upper:.1f}]")
                               
        except Exception:
            pass
            
    def calculate_area(self):
        """Calculate definite integral"""
        try:
            equation = self.equation_text.get('1.0', tk.END).strip()
            if not equation:
                return
                
            # Parse equation
            x_sym = sp.symbols('x')
            expr = sp.sympify(equation)
            
            # Calculate integral
            lower = self.int_lower.get()
            upper = self.int_upper.get()
            
            # Symbolic integration
            integral = sp.integrate(expr, (x_sym, lower, upper))
            
            # Numerical integration for comparison
            func = sp.lambdify(x_sym, expr, modules=['numpy'])
            numerical, _ = integrate.quad(func, lower, upper)
            
            # Display results
            result_text = f"Function: {equation}\n"
            result_text += f"Bounds: [{lower:.2f}, {upper:.2f}]\n"
            result_text += f"─" * 30 + "\n"
            result_text += f"Symbolic integral: {integral:.6f}\n"
            result_text += f"Numerical integral: {numerical:.6f}\n"
            
            # Calculate derivative at bounds
            deriv = sp.diff(expr, x_sym)
            deriv_func = sp.lambdify(x_sym, deriv, modules=['numpy'])
            
            result_text += f"─" * 30 + "\n"
            result_text += f"f'({lower:.2f}) = {deriv_func(lower):.4f}\n"
            result_text += f"f'({upper:.2f}) = {deriv_func(upper):.4f}\n"
            
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert('1.0', result_text)
            
            # Update plot to show area
            self.show_area.set(True)
            self.plot_function()
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            
    def add_function(self):
        """Add function to existing plot"""
        try:
            # Store current state
            current_funcs = self.current_functions.copy()
            
            # Plot new function
            self.plot_function()
            
            # Restore previous functions
            colors = self.color_schemes[self.current_scheme]
            for i, (eq, x, y) in enumerate(current_funcs):
                color = colors[i % len(colors)]
                self.ax.plot(x, y, color=color, linewidth=self.line_width.get(),
                           label=f"y = {eq}")
                           
            if self.show_legend.get():
                self.ax.legend(loc='best', framealpha=0.8)
                
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding function: {str(e)}")
            
    def apply_plot_styling(self):
        """Apply styling to the plot"""
        # Grid
        if self.show_grid.get():
            self.ax.grid(True, alpha=self.grid_alpha.get(), linestyle='-', linewidth=0.5)
            
        if self.show_minor_grid.get():
            self.ax.grid(True, which='minor', alpha=self.grid_alpha.get()*0.5,
                        linestyle=':', linewidth=0.3)
            self.ax.minorticks_on()
            
        # Axes
        if self.show_axes.get():
            self.ax.axhline(y=0, color='white', linewidth=0.5, alpha=0.5)
            self.ax.axvline(x=0, color='white', linewidth=0.5, alpha=0.5)
            
        # Legend
        if self.show_legend.get() and len(self.ax.lines) > 0:
            self.ax.legend(loc='best', framealpha=0.8)
            
        # Labels
        self.ax.set_xlabel('x', fontsize=12)
        self.ax.set_ylabel('y', fontsize=12)
        
        # Set limits
        self.ax.set_xlim(self.x_min.get(), self.x_max.get())
        self.ax.set_ylim(self.y_min.get(), self.y_max.get())
        
    def change_color_scheme(self, event=None):
        """Change the color scheme"""
        combo = event.widget
        self.current_scheme = combo.get()
        self.plot_function()
        
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.dark_mode.get():
            plt.style.use('dark_background')
            self.fig.patch.set_facecolor('#1a1a2e')
            self.ax.set_facecolor('#16213e')
        else:
            plt.style.use('default')
            self.fig.patch.set_facecolor('white')
            self.ax.set_facecolor('white')
            
        self.canvas.draw()
        
    def start_animation(self):
        """Start animation"""
        if self.is_animating:
            return
            
        self.is_animating = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        anim_type = self.anim_type.get()
        
        if anim_type == "phase":
            self.animate_phase()
        elif anim_type == "amplitude":
            self.animate_amplitude()
        elif anim_type == "frequency":
            self.animate_frequency()
        elif anim_type == "growing":
            self.animate_growing()
        elif anim_type == "rotate3d":
            self.animate_3d_rotation()
            
    def stop_animation(self):
        """Stop animation"""
        self.is_animating = False
        if self.animation_obj:
            self.animation_obj.event_source.stop()
            self.animation_obj = None
            
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
    def animate_phase(self):
        """Animate phase shift"""
        equation = self.equation_text.get('1.0', tk.END).strip()
        if not equation:
            return
            
        x = np.linspace(self.x_min.get(), self.x_max.get(), self.num_points.get())
        
        def update(frame):
            if not self.is_animating:
                return
                
            self.ax.clear()
            
            # Modify equation with phase
            phase = frame * 0.1
            modified_eq = equation.replace('x', f'(x - {phase})')
            
            try:
                x_sym = sp.symbols('x')
                expr = sp.sympify(modified_eq)
                func = sp.lambdify(x_sym, expr, modules=['numpy'])
                y = func(x)
                
                color = self.color_schemes[self.current_scheme][0]
                self.ax.plot(x, y, color=color, linewidth=self.line_width.get())
                self.ax.set_title(f"Phase Animation: {equation}", fontsize=14)
                self.apply_plot_styling()
                
            except:
                pass
                
        self.animation_obj = animation.FuncAnimation(
            self.fig, update, interval=self.anim_speed.get(), repeat=True
        )
        self.canvas.draw()
        
    def animate_amplitude(self):
        """Animate amplitude modulation"""
        equation = self.equation_text.get('1.0', tk.END).strip()
        if not equation:
            return
            
        x = np.linspace(self.x_min.get(), self.x_max.get(), self.num_points.get())
        
        def update(frame):
            if not self.is_animating:
                return
                
            self.ax.clear()
            
            # Calculate amplitude
            amp = 1 + 0.5 * np.sin(frame * 0.1)
            
            try:
                x_sym = sp.symbols('x')
                expr = sp.sympify(equation)
                func = sp.lambdify(x_sym, expr, modules=['numpy'])
                y = func(x) * amp
                
                color = self.color_schemes[self.current_scheme][1]
                self.ax.plot(x, y, color=color, linewidth=self.line_width.get())
                self.ax.set_title(f"Amplitude: {amp:.2f}", fontsize=14)
                self.apply_plot_styling()
                
            except:
                pass
                
        self.animation_obj = animation.FuncAnimation(
            self.fig, update, interval=self.anim_speed.get(), repeat=True
        )
        self.canvas.draw()
        
    def animate_frequency(self):
        """Animate frequency modulation"""
        base_equation = "sin(f * x)"
        x = np.linspace(self.x_min.get(), self.x_max.get(), self.num_points.get())
        
        def update(frame):
            if not self.is_animating:
                return
                
            self.ax.clear()
            
            # Vary frequency
            freq = 1 + 2 * np.sin(frame * 0.05)
            
            y = np.sin(freq * x)
            
            color = self.color_schemes[self.current_scheme][2]
            self.ax.plot(x, y, color=color, linewidth=self.line_width.get())
            self.ax.set_title(f"Frequency: {freq:.2f}", fontsize=14)
            self.apply_plot_styling()
            
        self.animation_obj = animation.FuncAnimation(
            self.fig, update, interval=self.anim_speed.get(), repeat=True
        )
        self.canvas.draw()
        
    def animate_growing(self):
        """Animate growing function"""
        equation = self.equation_text.get('1.0', tk.END).strip()
        if not equation:
            return
            
        x_full = np.linspace(self.x_min.get(), self.x_max.get(), self.num_points.get())
        
        try:
            x_sym = sp.symbols('x')
            expr = sp.sympify(equation)
            func = sp.lambdify(x_sym, expr, modules=['numpy'])
            y_full = func(x_full)
        except:
            return
            
        def update(frame):
            if not self.is_animating:
                return
                
            self.ax.clear()
            
            # Grow from left to right
            progress = (frame % 100) / 100
            end_idx = int(len(x_full) * progress)
            
            if end_idx > 0:
                x = x_full[:end_idx]
                y = y_full[:end_idx]
                
                # Rainbow color effect
                colors = plt.cm.rainbow(np.linspace(0, 1, len(x)))
                for i in range(len(x)-1):
                    self.ax.plot(x[i:i+2], y[i:i+2], color=colors[i], linewidth=2)
                    
            self.ax.set_title(f"Growing: {progress*100:.0f}%", fontsize=14)
            self.apply_plot_styling()
            
        self.animation_obj = animation.FuncAnimation(
            self.fig, update, interval=self.anim_speed.get(), repeat=True
        )
        self.canvas.draw()
        
    def animate_3d_rotation(self):
        """Animate 3D plot rotation"""
        if self.plot_mode.get() != "3D":
            messagebox.showinfo("Info", "Switch to 3D mode first!")
            self.stop_animation()
            return
            
        def update(frame):
            if not self.is_animating:
                return
                
            self.ax.view_init(elev=30, azim=frame*2)
            
        self.animation_obj = animation.FuncAnimation(
            self.fig, update, interval=self.anim_speed.get(), repeat=True
        )
        self.canvas.draw()
        
    def on_click(self, event):
        """Handle mouse clicks on plot"""
        if event.inaxes != self.ax:
            return
            
        # Add point marker
        self.ax.plot(event.xdata, event.ydata, 'yo', markersize=10, 
                    markeredgecolor='red', markeredgewidth=2)
        
        # Show coordinates
        self.ax.annotate(f"({event.xdata:.2f}, {event.ydata:.2f})",
                        xy=(event.xdata, event.ydata),
                        xytext=(event.xdata+0.5, event.ydata+0.5),
                        arrowprops=dict(arrowstyle='->', color='yellow'),
                        fontsize=10, color='yellow',
                        bbox=dict(boxstyle='round,pad=0.3', fc='black', alpha=0.7))
                        
        self.canvas.draw()
        
    def on_hover(self, event):
        """Handle mouse hover over plot"""
        if event.inaxes != self.ax:
            return
            
        # Update toolbar with coordinates
        if event.xdata is not None and event.ydata is not None:
            self.toolbar.set_message(f"x={event.xdata:.3f}, y={event.ydata:.3f}")
            
    def clear_plot(self):
        """Clear the plot"""
        self.ax.clear()
        self.current_functions = []
        self.apply_plot_styling()
        self.canvas.draw()
        
    def save_plot(self):
        """Save plot to file"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
                ("All files", "*.*")
            ]
        )
        
        if filepath:
            self.fig.savefig(filepath, dpi=150, bbox_inches='tight',
                           facecolor=self.fig.get_facecolor())
            messagebox.showinfo("Success", f"Plot saved to {filepath}")
            
    def export_data(self):
        """Export plot data to CSV"""
        if not self.current_functions:
            messagebox.showwarning("Warning", "No data to export!")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filepath:
            with open(filepath, 'w') as f:
                for eq, x, y in self.current_functions:
                    f.write(f"# Equation: {eq}\n")
                    f.write("x,y\n")
                    for xi, yi in zip(x[::10], y[::10]):  # Sample every 10th point
                        f.write(f"{xi:.6f},{yi:.6f}\n")
                    f.write("\n")
                    
            messagebox.showinfo("Success", f"Data exported to {filepath}")
            
    def save_animation(self):
        """Save animation as GIF"""
        if not self.is_animating:
            messagebox.showwarning("Warning", "Start an animation first!")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        
        if filepath:
            # Note: This requires pillow or imagemagick
            try:
                writer = animation.PillowWriter(fps=30)
                self.animation_obj.save(filepath, writer=writer)
                messagebox.showinfo("Success", f"Animation saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save animation: {str(e)}")
                
    def reset_and_demo(self):
        """Reset and show demo"""
        self.clear_plot()
        
        # Set a nice demo function
        demo_eq = "sin(x) * exp(-abs(x)/10) * cos(3*x)"
        self.set_equation(demo_eq)
        
        # Set nice range
        self.x_min.set(-10)
        self.x_max.set(10)
        self.y_min.set(-1.5)
        self.y_max.set(1.5)
        
        # Plot it
        self.plot_function()
        
        # Add welcome message
        self.ax.text(0.5, 1.05, "Welcome to Super Math Visualization Studio!",
                    transform=self.ax.transAxes, fontsize=16,
                    ha='center', color='cyan', weight='bold')
        
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = SuperMathGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()