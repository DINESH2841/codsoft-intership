import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showerror("Error", "Password length should be at least 4.")
            return

        chars = ""
        if var_upper.get():
            chars += string.ascii_uppercase
        if var_lower.get():
            chars += string.ascii_lowercase
        if var_digits.get():
            chars += string.digits
        if var_symbols.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("Error", "Select at least one character type.")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        password_var.set(password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

# GUI setup
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")

tk.Label(root, text="Enter password length:").pack(pady=5)
length_entry = tk.Entry(root)
length_entry.pack()

# Complexity options
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase (A-Z)", variable=var_upper).pack(anchor='w')
tk.Checkbutton(root, text="Include Lowercase (a-z)", variable=var_lower).pack(anchor='w')
tk.Checkbutton(root, text="Include Digits (0-9)", variable=var_digits).pack(anchor='w')
tk.Checkbutton(root, text="Include Symbols (!@#...)", variable=var_symbols).pack(anchor='w')

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, width=40, state='readonly').pack(pady=10)

root.mainloop()