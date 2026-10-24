import math
import tkinter as tk
from tkinter import messagebox

# SymPy
try:
    import sympy as sp
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Main Code 
class MultiModeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("480x660")
        self.root.resizable(False, False)

        self.first_num = None
        self.operator = None
        self.new_input = True

        self.container = tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.init_menu_screen()
        self.init_calc_screen()
        self.init_algebra_screen()
        self.init_graph_screen()

        self.show_screen("Menu")

    def show_screen(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def init_menu_screen(self):
        frame = tk.Frame(self.container, bg="#1e1e2e")
        self.frames["Menu"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        title = tk.Label(
            frame,
            text="Change Mode",
            font=("Arial", 22, "bold"),
            fg="#cdd6f4",
            bg="#1e1e2e"
        )
        title.pack(pady=(60, 40))

        btn_style = {
            "font": ("Arial", 14, "bold"),
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#b4befe"
        }

        calc_btn = tk.Button(
            frame,
            text="Scientific Calculator",
            bg="#89b4fa",
            fg="#11111b",
            command=lambda: self.show_screen("Calculator"),
            **btn_style
        )
        calc_btn.pack(fill=tk.X, padx=40, pady=15)

        algebra_btn = tk.Button(
            frame,
            text="Algebra Solver",
            bg="#a6e3a1",
            fg="#11111b",
            command=lambda: self.show_screen("Algebra Solver"),
            **btn_style
        )
        algebra_btn.pack(fill=tk.X, padx=40, pady=15)

        graph_btn = tk.Button(
            frame,
            text="2D Function Grapher",
            bg="#f9e2af",
            fg="#11111b",
            command=lambda: self.show_screen("Grapher"),
            **btn_style
        )
        graph_btn.pack(fill=tk.X, padx=40, pady=15)

    # Scientific Calculator Screen
    def init_calc_screen(self):
        frame = tk.Frame(self.container)
        self.frames["Calculator"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        top_bar = tk.Frame(frame, bg="#e0e0e0")
        top_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        tk.Button(
            top_bar, text="☰ Switch Modes", font=("Arial", 10, "bold"),
            bg="#2196F3", fg="white", command=lambda: self.show_screen("Menu")
        ).pack(side=tk.LEFT, padx=5, pady=5)

        # Display
        disp_frame = tk.Frame(frame, bd=2, relief=tk.SUNKEN, bg="#f0f0f0")
        disp_frame.pack(fill=tk.X, padx=10, pady=10)

        self.calc_sub = tk.Label(disp_frame, font=("Arial", 12), anchor="e", fg="#555555", bg="#f0f0f0", height=1)
        self.calc_sub.pack(fill=tk.X, padx=10, pady=(5, 0))

        self.calc_main = tk.Entry(disp_frame, font=("Arial", 20, "bold"), justify="right", bd=0, bg="#f0f0f0")
        self.calc_main.insert(0, "0")
        self.calc_main.config(state="readonly")
        self.calc_main.pack(fill=tk.X, ipadx=8, ipady=8, padx=5, pady=(0, 5))

        # Keypad
        grid_frame = tk.Frame(frame)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        buttons = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('log', 0, 3), ('ln', 0, 4),
            ('√', 1, 0), ('x²', 1, 1), ('^', 1, 2), ('π', 1, 3), ('e', 1, 4), 
            ('C', 2, 0), ('⌫', 2, 1), ('n!', 2, 2), ('/', 2, 3), ('*', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('-', 3, 3), ('+', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('0', 4, 3), ('.', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('=', 5, 3, 1, 2)
        ]
        for i in range(6): grid_frame.rowconfigure(i, weight=1)
        for i in range(5): grid_frame.columnconfigure(i, weight=1)

        for btn in buttons:
            text, r, c = btn[0], btn[1], btn[2]
            r_span, c_span = btn[3] if len(btn) > 3 else 1, btn[4] if len(btn) > 4 else 1 
            tk.Button(
                grid_frame, text=text, font=("Arial", 12),
                command=lambda t=text: self.handle_calc(t)
            ).grid(row=r, column=c, rowspan=r_span, columnspan=c_span, sticky="nsew", padx=2, pady=2)

    def handle_calc(self, text):
        curr = self.calc_main.get()

        def set_main(val):
            self.calc_main.config(state="normal")
            self.calc_main.delete(0, tk.END)
            self.calc_main.insert(0, val)
            self.calc_main.config(state="readonly")

        if text.isdigit():
            if self.new_input or curr in ("0", "Error"):
                set_main(text)
                self.new_input = False
            else: 
                set_main(curr + text)
        elif text == ".":
            if self.new_input or curr == "Error":
                set_main("0.")
                self.new_input = False
            elif '.' not in curr:
                set_main(curr + ".")
        elif text in ('π', 'e'):
            set_main(str(math.pi if text == 'π' else math.e))
            self.new_input = False
        elif text in ('+', '-', '*', '/', '^'):
            try:
                self.first_num = float(curr)
                self.operator = text
                f_num = int(self.first_num) if self.first_num.is_integer() else self.first_num
                self.calc_sub.config(text=f"{f_num} {text}")
                self.new_input = True
            except ValueError:
                set_main("Error")
        elif text in ('sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'n!'): 
            try:
                val = float(curr)
                f_val = int(val) if val.is_integer() else val
                if text == 'sin': res, expr = math.sin(math.radians(val)), f"sin({f_val}°)"
                elif text == 'cos': res, expr = math.cos(math.radians(val)), f"cos({f_val}°)"
                elif text == 'tan': res, expr = math.tan(math.radians(val)), f"tan({f_val}°)"
                elif text == 'log': res, expr = math.log10(val), f"log({f_val})"
                elif text == 'ln': res, expr = math.log(val), f"ln({f_val})"
                elif text == '√': res, expr = math.sqrt(val), f"√({f_val})"
                elif text == 'x²': res, expr = val ** 2, f"sqr({f_val})"
                elif text == 'n!': res, expr = math.factorial(int(val)), f"{int(val)}!"

                if isinstance(res, float) and res.is_integer(): res = int(res)
                set_main(str(res))
                self.calc_sub.config(text=f"{expr} =")
                self.new_input = True 
            except Exception:
                set_main("Error")
        elif text == '=':
            if self.operator and self.first_num is not None:
                try:
                    second = float(curr)
                    f_1 = int(self.first_num) if self.first_num.is_integer() else self.first_num
                    f_2 = int(second) if second.is_integer() else second
                    self.calc_sub.config(text=f"{f_1} {self.operator} {f_2} =")

                    ops = {'+': lambda a, b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b,
                           '/': lambda a,b: "Error" if b==0 else a/b, '^': lambda a,b: a**b}
                    res = ops[self.operator](self.first_num, second)
                    if isinstance(res, float) and res.is_integer(): res = int(res)
                    set_main(str(res))
                    self.first_num = self.operator = None
                    self.new_input = True
                except ValueError:
                    set_main("Error")
        elif text == '⌫':
            if not self.new_input and curr not in ("0", "Error"):
                new_t = curr[:-1]
                set_main("0" if new_t in ("", "-") else new_t)
        elif text == 'C':
            set_main("0")
            self.calc_sub.config(text="")
            self.first_num = self.operator = None
            self.new_input = True

    # Algebra Mode
    def init_algebra_screen(self):
        frame = tk.Frame(self.container)
        self.frames["Algebra Solver"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        top_bar = tk.Frame(frame, bg="#e0e0e0")
        top_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        tk.Button(
            top_bar, text="☰ Change Modes", font=("Arial", 10, "bold"),
            bg="#2196F3", fg='white', command=lambda: self.show_screen("Menu")
        ).pack(side=tk.LEFT, padx=5, pady=5)

        disp_frame = tk.Frame(frame, bd=2, relief=tk.SUNKEN, bg="#f0f0f0")
        disp_frame.pack(fill=tk.X, padx=10, pady=(5, 0))

        self.algebra_sub = tk.Label(disp_frame, text='Enter an Equation', font=("Arial", 10), anchor="e", fg="#555555", bg="#f0f0f0", height=1)
        self.algebra_sub.pack(fill=tk.X, padx=10, pady=(5, 0))

        self.algebra_main = tk.Entry(disp_frame, font=("Arial", 18, "bold"), justify='right', bd=0, bg="#f0f0f0")
        self.algebra_main.pack(fill=tk.X, ipadx=8, ipady=8, padx=5, pady=(0, 5))

        grid_frame = tk.Frame(frame)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        buttons = [
            ('x', 0, 0), ('y', 0, 1), ('=', 0, 2), ('^', 0, 3), ('(', 0, 4),
            ('d/dx', 1, 0), ('∫', 1, 1), ('Σ', 1, 2), ('/', 1, 3), (')', 1, 4),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3), ('C', 2, 4), 
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3), ('⌫', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3), ('.', 4, 4),
            ('0', 5, 0, 1, 2), ('SOLVE', 5, 2, 1, 3)
        ]

        for i in range(6): grid_frame.rowconfigure(i, weight=1)
        for i in range(5): grid_frame.columnconfigure(i, weight=1)

        for btn in buttons:
            text, r, c = btn[0], btn[1], btn[2]
            r_span, c_span = btn[3] if len(btn) > 3 else 1, btn[4] if len(btn) > 4 else 1
            tk.Button(
                grid_frame, text=text, font=("Arial", 12, "bold" if text == "SOLVE" else "normal"),
                bg="#a6e3a1" if text == "SOLVE" else "#f0f0f0",
                command=lambda t=text: self.handle_algebra(t)
            ).grid(row=r, column=c, rowspan=r_span, columnspan=c_span, sticky="nsew", padx=2, pady=2)

    def handle_algebra(self, text):
        curr = self.algebra_main.get()

        if text == 'SOLVE':
            self.algebra_expression(curr)
        elif text == 'C':
            self.algebra_main.delete(0, tk.END)
        elif text == '⌫':
            self.algebra_main.delete(0, tk.END)
            self.algebra_main.insert(0, curr[:-1])
        elif text == 'd/dx': self.algebra_main.insert(tk.END, "d/dx(")
        elif text == '∫': self.algebra_main.insert(tk.END, "∫(")
        elif text == 'Σ': self.algebra_main.insert(tk.END, "Σ(x, x, 1, 10)")
        else: self.algebra_main.insert(tk.END, text)

    def algebra_expression(self, expr_str):
        if not HAS_SYMPY:
            self.algebra_sub.config(text="Install SymPy: 'pip install sympy'")
            return

        if not expr_str.strip(): return

        try:
            x, y = sp.symbols('x y')
            clean_str = expr_str.replace('^', '**')

            if clean_str.startswith("d/dx("):
                inner = clean_str[5:-1] if clean_str.endswith(")") else clean_str[5:]
                res = sp.diff(sp.sympify(inner), x)
                self.algebra_sub.config(text=f"d/dx ({inner})")
                self.algebra_main.delete(0, tk.END); self.algebra_main.insert(0, str(res))
            elif clean_str.startswith("∫("):
                inner = clean_str[2:-1] if clean_str.endswith(")") else clean_str[2:]
                res = sp.integrate(sp.sympify(inner), x)
                self.algebra_sub.config(text=f"∫ ({inner}) dx")
                self.algebra_main.delete(0, tk.END); self.algebra_main.insert(0, f"{res} + C")
            elif clean_str.startswith("Σ("):
                inner = clean_str[2:-1] if clean_str.endswith(")") else clean_str[2:]
                parts = [p.strip() for p in inner.split(',')]
                res = sp.summation(sp.sympify(parts[0]), (sp.Symbol(parts[1]), sp.sympify(parts[2]), sp.sympify(parts[3])))
                self.algebra_sub.config(text=f"Σ: {expr_str}")
                self.algebra_main.delete(0, tk.END); self.algebra_main.insert(0, str(str(res)))
            elif '=' in clean_str:
                left, right = clean_str.split('=', 1)
                eq = sp.Eq(sp.sympify(left), sp.sympify(right))
                syms = list(eq.free_symbols) or [x]
                sol = sp.solve(eq, syms)
                self.algebra_sub.config(text=f"Solved: {expr_str}")
                self.algebra_main.delete(0, tk.END); self.algebra_main.insert(0, str(sol))
            else:
                simplified = sp.simplify(sp.sympify(clean_str))
                self.algebra_sub.config(text=f"Simplified: {expr_str}")
                self.algebra_main.delete(0, tk.END); self.algebra_main.insert(0, str(simplified))
        except Exception:
            self.algebra_sub.config(text="Syntax Error")

    # 2D Graphing Function
    def init_graph_screen(self):
        frame = tk.Frame(self.container)
        self.frames["Grapher"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        top_bar = tk.Frame(frame, bg='#e0e0e0')
        top_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        tk.Button(
            top_bar, text="☰ Switch Modes", font=("Arial", 10, "bold"),
            bg="#2196F3", fg='white', command=lambda: self.show_screen('Menu')
        ).pack(side=tk.LEFT, padx=5, pady=5)

        input_frame = tk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(input_frame, text="y =", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=(0,5))

        self.graph_entry = tk.Entry(input_frame, font=("Arial", 14))
        self.graph_entry.insert(0, "x^2 - 4")
        self.graph_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            input_frame, text="PLOT", font=("Arial", 11,"bold"),
            bg="#a6e3a1", fg="#11111b", command=self.plot_graph
        ).pack(side=tk.RIGHT, padx=5)

        self.plot_container = tk.Frame(frame, bg='#ffffff', bd=2, relief=tk.SUNKEN)
        self.plot_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        if HAS_MATPLOTLIB:
            self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_container)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.plot_graph()
        else:
            tk.Label(
                self.plot_container,
                text="Install matplotlib and numpy",
                font=("Arial", 12), fg="red", bg="white"
            ).pack(expand=True)

    def plot_graph(self):
        if not HAS_MATPLOTLIB:
            return

        expr_str = self.graph_entry.get().strip()
        if not expr_str:
            return

        try:
            self.ax.clear()
            x = np.linspace(-10, 10, 500)

            clean_expr = expr_str.replace('^', "**")
            allowed_context = {
                "x": x,
                "np": np,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "log": np.log10,
                "ln": np.log,
                "sqrt": np.sqrt,
                "pi": np.pi,
                "e": np.e
            }

            y = eval(clean_expr, {"__builtins__": None}, allowed_context)

            if isinstance(y, (int, float)):
                y = np.full_like(x, float(y))

            self.ax.plot(x, y, color="#2196F3", linewidth=2, label=f"y = {expr_str}")
            self.ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
            self.ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
            self.ax.grid(True, alpha=0.3)
            self.ax.set_ylim(-10, 10)
            self.ax.legend(loc="upper right")

            self.canvas.draw()
        except Exception:
            messagebox.showerror("Graph Error", "Invalid Equation")

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiModeCalculator(root)
    root.mainloop()
