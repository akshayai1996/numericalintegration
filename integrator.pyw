import tkinter as tk
from tkinter import messagebox
import math
import json
import tempfile
import os

# Create a temporary file for history
history_file = os.path.join(tempfile.gettempdir(), "history.json")

# List to store history
history = []

def load_history():
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            global history
            history = json.load(file)

def save_history():
    with open(history_file, "w") as file:
        json.dump(history, file)

def update_history(question, answer):
    if len(history) >= 10:
        history.pop(0)
    history.append((question, answer))
    save_history()

def show_history():
    history_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in history])
    messagebox.showinfo("History", history_text)

def trapezoidal_integration(func, a, b, n=50):
    try:
        h = (b - a) / n
        integral = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            integral += func(a + i * h)
        integral *= h
        return round(integral, 6)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def simpson_integration(func, a, b, n=50):
    try:
        if n % 2 != 0:
            raise ValueError("Number of intervals must be even for Simpson's rule.")
        
        h = (b - a) / n
        integral = func(a) + func(b)
        
        for i in range(1, n):
            if i % 2 == 0:
                integral += 2 * func(a + i * h)
            else:
                integral += 4 * func(a + i * h)
        
        integral *= h / 3
        return round(integral, 6)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def evaluate_function(func_str, x):
    try:
        return eval(func_str)
    except Exception as e:
        raise ValueError(f"Invalid function: {e}")

def convert_to_float(value):
    try:
        if "pi" in value.lower():
            value = value.replace("pi", str(math.pi))
        return eval(value)
    except Exception as e:
        raise ValueError("Invalid input for limits of integration.")

def calculate_trapezoidal():
    func_str = entry_function.get()
    try:
        a = convert_to_float(entry_a.get())
        b = convert_to_float(entry_b.get())
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
    def func(x):
        return evaluate_function(func_str, x)
    
    result = trapezoidal_integration(func, a, b)
    if result is not None:
        label_result.config(text=f"Trapezoidal Integration result: {result}")
        update_history(f"Trapezoidal Integration of {func_str} from {a} to {b}", result)

def calculate_simpson():
    func_str = entry_function.get()
    try:
        a = convert_to_float(entry_a.get())
        b = convert_to_float(entry_b.get())
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
    def func(x):
        return evaluate_function(func_str, x)
    
    result = simpson_integration(func, a, b)
    if result is not None:
        label_result.config(text=f"Simpson Integration result: {result}")
        update_history(f"Simpson Integration of {func_str} from {a} to {b}", result)

def insert_function(func):
    current_text = entry_function.get()
    entry_function.delete(0, tk.END)
    entry_function.insert(0, current_text + func)

# Create the main window
root = tk.Tk()
root.title("Numerical Integrator Calculator")

# Set minimum width for the window
root.minsize(360, 300)

# Load history when the application starts
load_history()

# Configure grid weights to make widgets resize proportionally
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create and place the widgets
tk.Label(root, text="Function f(x):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_function = tk.Entry(root, width=30)
entry_function.grid(row=0, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Lower limit a:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_a = tk.Entry(root, width=30)
entry_a.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Upper limit b:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_b = tk.Entry(root, width=30)
entry_b.grid(row=2, column=1, padx=10, pady=10, sticky="w")

button_trapezoidal = tk.Button(root, text="Calculate Trapezoidal Integration", command=calculate_trapezoidal)
button_trapezoidal.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

button_simpson = tk.Button(root, text="Calculate Simpson Integration", command=calculate_simpson)
button_simpson.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

label_result = tk.Label(root, text="Integration result:")
label_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Create a frame for the function buttons
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Configure grid weights for the frame to ensure buttons resize proportionally
frame_buttons.grid_columnconfigure(0, weight=1)
frame_buttons.grid_columnconfigure(1, weight=1)
frame_buttons.grid_columnconfigure(2, weight=1)
frame_buttons.grid_columnconfigure(3, weight=1)
frame_buttons.grid_columnconfigure(4, weight=1)

# Add buttons for trigonometric functions, logarithmic functions, and power function in one line with uniform spacing
button_sin = tk.Button(frame_buttons, text="sin(x)", command=lambda: insert_function("math.sin(x)"))
button_sin.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

button_cos = tk.Button(frame_buttons, text="cos(x)", command=lambda: insert_function("math.cos(x)"))
button_cos.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

button_tan = tk.Button(frame_buttons, text="tan(x)", command=lambda: insert_function("math.tan(x)"))
button_tan.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

button_log = tk.Button(frame_buttons, text="log(x)", command=lambda: insert_function("math.log(x)"))
button_log.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

button_pow = tk.Button(frame_buttons, text="x^n", command=lambda: insert_function("x**"))
button_pow.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

# Add a button to show history
button_history = tk.Button(root, text="Show History", command=show_history, width=15)
button_history.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Save history when the application is closed
root.protocol("WM_DELETE_WINDOW", lambda: [save_history(), root.destroy()])

# Run the main loop
root.mainloop()