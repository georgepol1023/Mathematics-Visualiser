import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkfont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

class MathPlotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Math Visualization GUI")
        self.root.geometry("1200x800")

        # Set a larger font for all widgets
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=14)
        text_font = ("Helvetica", 14)
        btn_font = ("Helvetica", 14)
        # Much larger font for the function listbox
        listbox_font = ("Helvetica", 20, "bold")

        # Variables for controls
        self.x_min = tk.DoubleVar(value=0.1)  # min > 0 for ln(x)
        self.x_max = tk.DoubleVar(value=10)
        self.show_grid = tk.BooleanVar(value=True)
        self.show_legend = tk.BooleanVar(value=True)
        self.plot_style = tk.StringVar(value="line")

        # Available functions
        self.func_names = [
            "y = x^2",
            "y = sin(x)",
            "y = cos(x)",
            "y = ln(x)",
            "y = e^x",
            "y = sinh(x)",
            "y = cosh(x)",
            "y = tanh(x)",
            "Custom polynomial"
        ]

        # Figure setup
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Controls frame
        control_frame = ttk.Frame(root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Plot range sliders
        ttk.Label(control_frame, text="X min:", font=text_font).grid(row=0, column=0, sticky='w')
        self.x_min_scale = ttk.Scale(control_frame, from_=0.01, to=20, variable=self.x_min, orient='horizontal')
        self.x_min_scale.grid(row=0, column=1, sticky='ew')

        ttk.Label(control_frame, text="X max:", font=text_font).grid(row=1, column=0, sticky='w')
        self.x_max_scale = ttk.Scale(control_frame, from_=0.1, to=50, variable=self.x_max, orient='horizontal')
        self.x_max_scale.grid(row=1, column=1, sticky='ew')

        # Plot style selector
        ttk.Label(control_frame, text="Plot style:", font=text_font).grid(row=2, column=0, sticky='w')
        style_combo = ttk.Combobox(control_frame, textvariable=self.plot_style,
                                   values=["line", "scatter"], state="readonly", font=text_font)
        style_combo.grid(row=2, column=1, sticky='ew')

        # Large multi-select Listbox for functions with big letters and size
        func_frame = ttk.LabelFrame(control_frame,
                                    text="Select functions (Ctrl+Click to select multiple)",
                                    labelanchor='n', padding=8, style='My.TLabelframe')
        func_frame.grid(row=0, column=2, rowspan=4, padx=10, sticky='nsew')

        self.func_listbox = tk.Listbox(func_frame, selectmode=tk.MULTIPLE,
                                      height=20, width=40,
                                      exportselection=False,
                                      font=listbox_font)
        for func in self.func_names:
            self.func_listbox.insert(tk.END, func)
        self.func_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(func_frame, orient="vertical", command=self.func_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.func_listbox.config(yscrollcommand=scrollbar.set)

        # Custom polynomial entry
        self.custom_entry = ttk.Entry(control_frame, width=40, font=text_font)
        self.custom_entry.insert(0, "2*x**3 - 5*x + 1")
        self.custom_entry.grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)
        self.custom_entry.grid_remove()
        self.custom_entry.bind("<KeyRelease>", lambda event: self.plot_function())

        # Buttons frame
        button_frame = ttk.Frame(root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="Plot", command=self.plot_function, width=10, style='My.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_plot, width=10, style='My.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_controls, width=10, style='My.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Plot", command=self.save_plot, width=10, style='My.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset Zoom", command=self.reset_zoom, width=12, style='My.TButton').pack(side='left', padx=5)

        # Style for label frame and buttons to enlarge fonts nicely
        style = ttk.Style()
        style.configure('My.TLabelframe.Label', font=("Helvetica", 16, "bold"))
        style.configure('My.TButton', font=btn_font)

        # Increase matplotlib fonts
        plt.rcParams.update({
            'axes.titlesize': 20,
            'axes.labelsize': 18,
            'xtick.labelsize': 16,
            'ytick.labelsize': 16,
            'legend.fontsize': 17,
            'figure.titlesize': 22
        })

        self.reset_controls()
        self.canvas.draw()

    def parse_custom_poly(self, expr, x_vals):
        try:
            x = sp.symbols('x')
            parsed_expr = sp.sympify(expr)
            f = sp.lambdify(x, parsed_expr, "numpy")
            return f(x_vals)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid polynomial expression:\n{e}")
            return None

    def plot_function(self):
        xmin = self.x_min.get()
        xmax = self.x_max.get()
        if xmin >= xmax:
            messagebox.showerror("Error", "X min must be less than X max")
            return

        selected_indices = self.func_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Select at least one function to plot.")
            return

        x_vals = np.linspace(xmin, xmax, 500)
        self.ax.clear()

        for i in selected_indices:
            func_name = self.func_names[i]
            if func_name == "y = x^2":
                y_vals = x_vals**2
            elif func_name == "y = sin(x)":
                y_vals = np.sin(x_vals)
            elif func_name == "y = cos(x)":
                y_vals = np.cos(x_vals)
            elif func_name == "y = ln(x)":
                # domain check for ln(x) > 0
                x_vals_pos = x_vals[x_vals > 0]
                y_vals = np.log(x_vals_pos)
                if self.plot_style.get() == "line":
                    self.ax.plot(x_vals_pos, y_vals, label=func_name)
                else:
                    self.ax.scatter(x_vals_pos, y_vals, label=func_name, s=15)
                continue
            elif func_name == "y = e^x":
                y_vals = np.exp(x_vals)
            elif func_name == "y = sinh(x)":
                y_vals = np.sinh(x_vals)
            elif func_name == "y = cosh(x)":
                y_vals = np.cosh(x_vals)
            elif func_name == "y = tanh(x)":
                y_vals = np.tanh(x_vals)
            elif func_name == "Custom polynomial":
                y_vals = self.parse_custom_poly(self.custom_entry.get(), x_vals)
                if y_vals is None:
                    continue

            if self.plot_style.get() == "line":
                self.ax.plot(x_vals, y_vals, label=func_name)
            else:
                self.ax.scatter(x_vals, y_vals, label=func_name, s=15)

        if self.show_grid.get():
            self.ax.grid(True, linestyle='--', alpha=0.6)
        if self.show_legend.get():
            self.ax.legend()

        self.ax.set_title("Enhanced Math Visualization", fontsize=20)
        self.ax.set_xlabel("x", fontsize=18)
        self.ax.set_ylabel("y", fontsize=18)

        # Friendly guy annotation
        xmin_plot, xmax_plot = self.ax.get_xlim()
        ymin_plot, ymax_plot = self.ax.get_ylim()
        xg = xmin_plot + (xmax_plot - xmin_plot) * 0.75
        yg_min, yg_max = ymin_plot, ymax_plot
        yg = yg_min + (yg_max - yg_min) * 0.4
        yg_top = yg_min + (yg_max - yg_min) * 0.6

        self.ax.annotate(
            "Hi! Here's your math plot!",
            xy=(xg, yg),
            xytext=(xg * 1.05, yg_top),
            arrowprops=dict(arrowstyle="->", color='green', lw=2),
            fontsize=18,
            color='darkgreen',
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="green", lw=2)
        )

        stick_x = [xg * 0.98, xg * 0.98, xg * 0.95, xg * 1.01, xg * 0.98]
        stick_y = [yg * 0.9, yg_top * 0.97, yg_top * 0.93, yg_top * 0.93, yg * 0.9]
        self.ax.plot(stick_x[:2], stick_y[:2], color='darkgreen', lw=3)
        self.ax.plot(stick_x[2:4], stick_y[2:4], color='darkgreen', lw=3)
        self.ax.scatter([xg * 0.98], [yg_top * 0.98], s=120, color='darkgreen', edgecolors='black', linewidths=1)

        self.canvas.draw()

    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()

    def reset_controls(self):
        self.x_min.set(0.1)
        self.x_max.set(10)
        self.show_grid.set(True)
        self.show_legend.set(True)
        self.plot_style.set("line")
        self.func_listbox.selection_clear(0, tk.END)
        self.func_listbox.selection_set(0, 1)  # select y=x² and sin(x) by default
        self.custom_entry.grid_remove()
        self.canvas.draw()

    def save_plot(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filepath:
            self.fig.savefig(filepath)
            messagebox.showinfo("Saved", f"Plot image saved to {filepath}")

    def reset_zoom(self):
        self.ax.autoscale(enable=True)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = MathPlotGUI(root)
    root.mainloop()
