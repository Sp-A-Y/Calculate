"""
Windows Style Calculator - Python Tkinter
Требует только стандартную библиотеку Python (tkinter встроен)
Запуск: python calculator.py
"""
import tkinter as tk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("320x450")
        self.root.resizable(False, False)
        
        # Настройки
        self.mode = "standard"
        self.expression = ""
        self.memory = 0
        
        # Цвета (стиль Windows)
        self.bg_main = "#f3f3f3"
        self.bg_display = "#1e1e1e"
        self.bg_display_text = "#ffffff"
        self.bg_button = "#f0f0f0"
        self.bg_function = "#a5a5a5"
        self.bg_operator = "#3a3a3a"
        self.bg_operator_text = "#ffffff"
        
        self.root.configure(bg=self.bg_main)
        
        self.create_display()
        self.create_buttons()
        
    def create_display(self):
        display_frame = tk.Frame(self.root, bg=self.bg_display)
        display_frame.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        self.display = tk.Label(
            display_frame,
            text="0",
            bg=self.bg_display,
            fg=self.bg_display_text,
            font=("Segoe UI", 24, "bold"),
            anchor="e",
            padx=10,
            pady=5
        )
        self.display.pack(fill=tk.BOTH)
        
        self.sub_display = tk.Label(
            display_frame,
            text="",
            bg=self.bg_display,
            fg="#888888",
            font=("Segoe UI", 10),
            anchor="e",
            padx=10
        )
        self.sub_display.pack(fill=tk.BOTH)
        
    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg=self.bg_main)
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for widget in btn_frame.winfo_children():
            widget.destroy()
            
        if self.mode == "standard":
            self.create_standard_buttons(btn_frame)
        else:
            self.create_scientific_buttons(btn_frame)
            
    def create_standard_buttons(self, frame):
        buttons = [
            ["MC", "MR", "M+", "M-", "C"],
            ["CE", "←", "%", "÷", "×"],
            ["7", "8", "9", "±", "1/x"],
            ["4", "5", "6", "-", "+"],
            ["1", "2", "3", "=", "√"],
            ["0", ".", "", "", ""]
        ]
        
        for r, row in enumerate(buttons):
            for c, btn in enumerate(row):
                if btn == "":
                    continue
                    
                if btn in ["C", "CE"]:
                    bg = self.bg_function
                elif btn in ["÷", "×", "-", "+", "="]:
                    bg = self.bg_operator
                    fg = self.bg_operator_text
                else:
                    bg = self.bg_button
                    fg = "black"
                    
                cmd = self.get_command(btn)
                    
                tk.Button(
                    frame,
                    text=btn,
                    font=("Segoe UI", 14),
                    bg=bg,
                    fg=fg,
                    relief=tk.FLAT,
                    command=cmd
                ).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                
        tk.Button(
            frame,
            text="★ Scientific",
            font=("Segoe UI", 10),
            bg=self.bg_function,
            fg="black",
            relief=tk.FLAT,
            command=self.toggle_mode
        ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
                
    def create_scientific_buttons(self, frame):
        buttons = [
            ["deg", "sin", "cos", "tan", "C"],
            ["π", "e", "x²", "xʸ", "CE"],
            ["x³", "√x", "n!", "log", "ln"],
            ["(", ")", "%", "÷", "×"],
            ["7", "8", "9", "±", "1/x"],
            ["4", "5", "6", "-", "+"],
            ["1", "2", "3", "=", "√"],
            ["0", ".", "", "", ""]
        ]
        
        for r, row in enumerate(buttons):
            for c, btn in enumerate(row):
                if btn == "":
                    continue
                    
                if btn in ["C", "CE"]:
                    bg = self.bg_function
                elif btn in ["÷", "×", "-", "+", "=", "sin", "cos", "tan", "log", "ln", "√x", "x²", "xʸ", "x³", "n!", "√", "π", "e", "deg"]:
                    bg = self.bg_operator
                    fg = self.bg_operator_text
                else:
                    bg = self.bg_button
                    fg = "black"
                    
                command = lambda b=btn: self.scientific_button(b)
                    
                tk.Button(
                    frame,
                    text=btn,
                    font=("Segoe UI", 12),
                    bg=bg,
                    fg=fg,
                    relief=tk.FLAT,
                    command=command
                ).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                
        tk.Button(
            frame,
            text="◀ Standard",
            font=("Segoe UI", 10),
            bg=self.bg_function,
            fg="black",
            relief=tk.FLAT,
            command=self.toggle_mode
        ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        
    def get_command(self, btn):
        commands = {
            "=": self.calculate,
            "C": self.clear_all,
            "CE": self.clear_entry,
            "←": self.backspace,
            "±": self.toggle_sign,
            "1/x": self.reciprocal,
            "√": self.sqrt,
            "%": lambda: self.append_operator("%"),
            "MC": lambda: self.memory_op("MC"),
            "MR": lambda: self.memory_op("MR"),
            "M+": lambda: self.memory_op("M+"),
            "M-": lambda: self.memory_op("M-"),
        }
        if btn in commands:
            return commands[btn]
        if btn in ["÷", "×", "-", "+"]:
            return lambda b=btn: self.append_operator(b)
        return lambda b=btn: self.append_number(b)
    
    def scientific_button(self, btn):
        funcs = {
            "C": self.clear_all, "CE": self.clear_entry, "←": self.backspace,
            "±": self.toggle_sign, "1/x": self.reciprocal, "√": self.sqrt,
            "π": lambda: self.append_number("3.14159265359"),
            "e": lambda: self.append_number("2.71828182846"),
            "x²": lambda: self.append_operator("**2"),
            "xʸ": lambda: self.append_operator("**"),
            "x³": lambda: self.append_operator("**3"),
            "√x": lambda: self.append_operator("**0.5"),
            "n!": self.factorial,
            "log": self.append_log10,
            "ln": self.append_ln,
            "sin": lambda: self.append_func("sin"),
            "cos": lambda: self.append_func("cos"),
            "tan": lambda: self.append_func("tan"),
            "deg": self.to_degrees,
        }
        if btn in funcs:
            funcs[btn]()
        elif btn in ["÷", "×", "-", "+", "%"]:
            self.append_operator(btn)
        elif btn == "=":
            self.calculate()
        else:
            self.append_number(btn)
            
    def factorial(self):
        try:
            n = int(float(self.expression))
            self.expression = str(math.factorial(n))
            self.update_display()
        except:
            self.display.config(text="Error")
            self.expression = ""
            
    def append_log10(self):
        self.expression += "log10("
        self.update_display()
        
    def append_ln(self):
        self.expression += "log("
        self.update_display()
        
    def append_func(self, func):
        self.expression += func + "("
        self.update_display()
        
    def to_degrees(self):
        try:
            val = eval(self.expression) if self.expression else 0
            self.expression = str(math.degrees(val))
            self.update_display()
        except:
            self.display.config(text="Error")
            self.expression = ""
            
    def toggle_mode(self):
        self.expression = ""
        self.display.config(text="0")
        self.sub_display.config(text="")
        self.create_buttons()
        
    def append_number(self, num):
        if self.display.cget("text") == "0" and num != ".":
            self.expression = num
        else:
            self.expression += num
        self.update_display()
        
    def append_operator(self, op):
        op_map = {"÷": "/", "×": "*", "√": "**0.5"}
        op = op_map.get(op, op)
        if self.expression and self.expression[-1] in "+-*/%.":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op
        self.update_display()
        
    def calculate(self):
        try:
            expr = self.expression.replace("÷", "/").replace("×", "*").replace("√", "**0.5")
            expr = expr.replace("log10", "math.log10").replace("log", "math.log")
            expr = expr.replace("sin", "math.sin").replace("cos", "math.cos").replace("tan", "math.tan")
            result = eval(expr)
            if isinstance(result, float):
                result = int(result) if result.is_integer() else round(result, 10)
            self.expression = str(result)
            self.update_display()
        except:
            self.display.config(text="Error")
            self.expression = ""
            
    def clear_all(self):
        self.expression = ""
        self.display.config(text="0")
        self.sub_display.config(text="")
        
    def clear_entry(self):
        self.expression = ""
        self.display.config(text="0")
        
    def backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
            self.display.config(text=self.expression if self.expression else "0")
            
    def toggle_sign(self):
        if self.expression:
            self.expression = "-" + self.expression if not self.expression.startswith("-") else self.expression[1:]
            self.update_display()
            
    def reciprocal(self):
        if self.expression:
            try:
                val = eval(self.expression)
                self.expression = str(1 / val)
                self.update_display()
            except:
                self.display.config(text="Error")
                self.expression = ""
                
    def sqrt(self):
        if self.expression:
            try:
                val = eval(self.expression)
                result = math.sqrt(val)
                self.expression = str(int(result) if result.is_integer() else round(result, 10))
                self.update_display()
            except:
                self.display.config(text="Error")
                self.expression = ""
                
    def memory_op(self, op):
        try:
            current = float(self.expression) if self.expression else 0
            if op == "M+": self.memory += current
            elif op == "M-": self.memory -= current
            elif op == "MR": self.expression = str(int(self.memory) if self.memory.is_integer() else self.memory); self.update_display()
            elif op == "MC": self.memory = 0
            mem_val = int(self.memory) if self.memory.is_integer() else self.memory
            self.sub_display.config(text=f"M: {mem_val}")
        except: pass
            
    def update_display(self):
        self.display.config(text=self.expression[:20] if self.expression else "0")

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()