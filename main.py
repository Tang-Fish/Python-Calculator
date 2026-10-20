import math
import tkinter as tk 

# Core Functions
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by Zero"
    return a / b

def power(a, b):
    return a ** b

# Scientific Functions
class CalculatorGUI:
    def __init__(self, root):
        self.root = root 
        self.root.title("Scientific Calculator")
        self.root.geometry("400x520")
        self.root.resizable(False, False)

        self.first_num = None 
        self.operator = None
        self.new_input = True 

        self.init_ui()
    def init_ui(self):
        display_frame = tk.Frame(self.root, bd = 2, relief = tk.SUNKEN, bg = "white")
        display_frame.pack(fill=tk.X, padx=10, pady=10)

        self.sub_display = tk.Label(
            display_frame,
            font=("Arial", 11),
            anchor="e",
            fg="grey",
            bg="white",
            height = 1
        )
        self.sub_display.pack(fill=tk.X, padx=5, pady=(5, 0))

        self.display = tk.Entry(
            display_frame,
            font=("Arial", 22, "bold"),
            justify="right",
            bd=0,
            relief=tk.FLAT,
            bg="white"
        )
        self.display.insert(0, "0")
        self.display.config(state="readonly")
        self.display.pack(fill=tk.X, ipadx=8, ipady=8, padx=5, pady=(0, 5))

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        buttons = [
            # Scientific Functions
            ('sin', 0, 0, 1, 1), ('cos', 0, 1, 1, 1), ('tan', 0, 2, 1, 1), ('log', 0, 3, 1, 1), ('ln', 0, 4, 1, 1),
            ('√', 1, 0, 1, 1), ('x²', 1, 1, 1, 1), ('x³', 1, 2, 1, 1), ('xʸ', 1, 3, 1, 1), ('π', 1, 4, 1, 1),
            # Controls and Operations
            ('C', 2, 0, 1, 1), ('⌫', 2, 1, 1, 1), ('n!', 2, 2, 1, 1), ('/', 2, 3, 1, 1), ('*', 2, 4, 1, 1),
            # NumPad
            ('7', 3, 0, 1, 1), ('8', 3, 1, 1, 1), ('9', 3, 2, 1, 1), ('-', 3, 3, 1, 1), ('+', 3, 4, 1, 1),
            ('4', 4, 0, 1, 1), ('5', 4, 1, 1, 1), ('6', 4, 2, 1, 1), ('0', 4, 3, 1, 1), ('.', 4, 4, 1, 1),
            ('1', 5, 0, 1, 1), ('2', 5, 1, 1, 1), ('3', 5, 2, 1, 1), ('=', 5, 3, 1, 2)
        ]

        for i in range(6):
            frame.rowconfigure(i, weight=1)
        for i in range(5):
            frame.columnconfigure(i, weight=1)

        for text, row, col, r_span, c_span, in buttons:
            btn = tk.Button(
                frame,
                text=text,
                font=("Arial", 14),
                command=lambda t=text: self.handle_button(t)
            )
            btn.grid(row=row, column=col, rowspan=r_span, columnspan=c_span, sticky="nsew", padx=2, pady=2)

        def set_display(self, text):
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, text)
            self.display.config(state="readonly")

        def set_sub_display(self, text):
            self.sub_display.config(text=text)

        def handle_button(self, text):
            current_text = self.display.get()

            if text.isdigit():
                if self.new_input or current_text in ("0", "Error: Division by Zero", "Error"):
                    self.set_display(text)
                    self.new_input = False
                else:
                    self.set_display(current_text + text)

            elif text ==".":
                if self.new_input or current_text in ("Error", "Error: Division by Zero"):
                    self.set_display("0.")
                    self.new_input = False
                elif "." not in current_text:
                    self.set_display(current_text + ".")

            elif text in ('π', 'e'):
                val = math.pi if text == 'π' else math.e
                self.set_display(str(val))
                self.new_input = False

            elif text in ('+', '-', '*', '/', '^'):
                try:
                    self.first_num = float(current_text)
                    self.operator = text

                    formatted_num = int(self.first_num) if self.first_num.is_integer() else self.first_num
                    self.set_sub_display(f"{formatted_num} {self.operator}")

                    self.new_input = True
                except ValueError:
                    self.set_display("Error")

            elif text in ('sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'n!'):
                try:
                    val = float(current_text)
                    formatted_val = int(val) if val.is_integer() else val

                    if text == 'sin':
                        res = math.sin(math.radians(val))
                        expr = f"sin({formatted_val}°)"
                    elif text == 'cos':
                        res = math.cos(math.radians(val))
                        expr = f"cos({formatted_val}°)"
                    elif text == 'tan':
                        res = math.tan(math.radians(val))
                        expr = f"tan({formatted_val}°)"
                    elif text == 'log':
                        if val <= 0:
                            raise ValueError("Logarithm undefined for non-positive values")
                        res = math.log10(val)
                        expr = f"log({formatted_val})"
                    elif text == 'ln':
                       if val <= 0:
                        res = math.log(val)
                        expr = f"ln({formatted_val})"
                    elif text == '√':
                        if val < 0: raise ValueError
                        res = math.sqrt
                        expr = f"√({formatted_val})"
                    elif text == 'x²':
                        res = val ** 2
                        expr = f"({formatted_val})²"
                    elif text == 'n!':
                        if val < 0 or not val.is_integer():
                            res = int(res)

                        self.set_sub_display(f"{expr} =") 
                        self.set_display(str(res))
                        self.new_input = True
                except Exception:
                    self.set_display("Error")

            elif text == '=':
                if self.operator and self.first_num is not None:
                    try:
                        second_num = float(current_text)
                        formatted_first = int(self.first_num) if self.first_num.is_integer() else self.first_num
                        formatted_second = int(second_num) if second_num.is_integer() else second_num

                        self.set_sub_display(f"{formatted_first} {self.operator} {formatted_second} =")

                        operations = {
                            '+': add,
                            '-': subtract,
                            '*': multiply,
                            '/': divide,
                            '^': power
                        }

                        calc_func = operations[self.operator]
                        result = calc_func(self.first_num, second_num)

                        if isinstance(result, float) and result.is_integer():
                            result = int(result)

                        self.set_display(str(result))
                        self.first_num = None
                        self.operator = None
                    except ValueError:
                        self.set_display("Error")

            elif text == '⌫':
                if not self.new_input and current_text not in ("0", "Error: Division by Zero", "Error"):
                    new_text = current_text[:-1]
                    if new_text in ("", "-"):
                        self.set_display("0")
                        self.new_input = True



# Run
if __name__ == "__main__":
    root = tk.Tk()
    calculator = CalculatorGUI(root)
    root.mainloop()
