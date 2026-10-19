import tkinter as tk

# --- Original Core Logic ---
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

# --- Tkinter GUI Integration ---
class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Calculator")
        self.root.geometry("300x440")
        self.root.resizable(False, False)

        self.first_num = None
        self.operator = None
        self.new_input = True

        self.init_ui()

    def init_ui(self):
        # Display Container Box
        display_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN, bg="#f0f0f0")
        display_frame.pack(fill=tk.X, padx=10, pady=10)

        # Secondary Top Display (Small expression history)
        self.sub_display = tk.Label(
            display_frame,
            font=("Arial", 11),
            anchor="e",
            fg="#666666",
            bg="#f0f0f0",
            height=1
        )
        self.sub_display.pack(fill=tk.X, padx=5, pady=(5, 0))

        # Main Bottom Display (Current active input/result)
        self.display = tk.Entry(
            display_frame,
            font=("Arial", 20, "bold"),
            justify="right",
            bd=0,
            relief=tk.FLAT,
            bg="#FEFEFE"
        )
        self.display.insert(0, "0")
        self.display.config(state="readonly")
        self.display.pack(fill=tk.X, ipadx=8, ipady=8, padx=5, pady=(0, 5))

        # Button Grid Frame
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Full button layout.
        buttons = [
            ('C', 0, 0, 1, 1), ('⌫', 0, 1, 1, 1), ('/', 0, 2, 1, 1), ('*', 0, 3, 1, 1),
            ('7', 1, 0, 1, 1), ('8', 1, 1, 1, 1), ('9', 1, 2, 1, 1), ('-', 1, 3, 1, 1),
            ('4', 2, 0, 1, 1), ('5', 2, 1, 1, 1), ('6', 2, 2, 1, 1), ('+', 2, 3, 1, 1),
            ('1', 3, 0, 1, 1), ('2', 3, 1, 1, 1), ('3', 3, 2, 1, 1), ('=', 3, 3, 2, 1),
            ('0', 4, 0, 1, 3),
        ]

        for i in range(5):
            frame.rowconfigure(i, weight=1)
        for i in range(4):
            frame.columnconfigure(i, weight=1)

        for text, row, col, r_span, c_span in buttons:
            btn = tk.Button(
                frame,
                text=text,
                font=("Arial", 16),
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
            if self.new_input or current_text in ("0", "Error: Division by zero", "Error"):
                self.set_display(text)
                self.new_input = False
            else:
                self.set_display(current_text + text)

        elif text in ('+', '-', '*', '/'):
            try:
                self.first_num = float(current_text)
                self.operator = text
                
                # Format clean display string
                formatted_num = int(self.first_num) if self.first_num.is_integer() else self.first_num
                self.set_sub_display(f"{formatted_num} {self.operator}")
                
                self.new_input = True
            except ValueError:
                self.set_display("Error")

        elif text == '=':
            if self.operator and self.first_num is not None:
                try:
                    second_num = float(current_text)
                    formatted_first = int(self.first_num) if self.first_num.is_integer() else self.first_num
                    formatted_second = int(second_num) if second_num.is_integer() else second_num

                    # Push full equation to secondary display
                    self.set_sub_display(f"{formatted_first} {self.operator} {formatted_second} =")

                    operations = {
                        '+': add,
                        '-': subtract,
                        '*': multiply,
                        '/': divide
                    }

                    calc_func = operations[self.operator]
                    result = calc_func(self.first_num, second_num)

                    if isinstance(result, float) and result.is_integer():
                        result = int(result)

                    self.set_display(str(result))
                    self.first_num = None 
                    self.operator = None
                    self.new_input = True
                except ValueError:
                    self.set_display("Error")

        elif text == '⌫':
            if not self.new_input and current_text not in ("0", "Error: Division by zero", "Error"):
                new_text = current_text[:-1]
                if new_text in ("", "-"):
                    self.set_display("0")
                    self.new_input = True
                else:
                    self.set_display(new_text)

        elif text == 'C':
            self.set_display("0")
            self.set_sub_display("")
            self.first_num = None
            self.operator = None
            self.new_input = True

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()