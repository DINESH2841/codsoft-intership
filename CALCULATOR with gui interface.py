import tkinter as tk
from tkinter import ttk

def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            expr = entry_var.get()
            expr = expr.replace('%', '/100')
            result = str(eval(expr))
            result_var.set(result)
        except Exception:
            result_var.set("Error")
    elif text == "C":
        entry_var.set("")
        result_var.set("")
    elif text == "⌫":
        entry_var.set(entry_var.get()[:-1])
    else:
        entry_var.set(entry_var.get() + text)
        result_var.set("")

def keypress(event):
    key = event.char
    if key in "0123456789.+-*/()%":
        entry_var.set(entry_var.get() + key)
        result_var.set("")
    elif key == "\r":
        click(type("Event", (), {"widget": type("Widget", (), {"cget": lambda self, x: "="})()})())
    elif key == "\x08":
        entry_var.set(entry_var.get()[:-1])
    elif key.lower() == "c":
        entry_var.set("")
        result_var.set("")

def on_enter(e):
    e.widget['style'] = 'Hover.TButton'

def on_leave(e):
    e.widget['style'] = 'Calc.TButton'

root = tk.Tk()
root.title("Advanced Calculator")
root.geometry("400x550")
root.configure(bg="#222831")

style = ttk.Style(root)
style.theme_use('clam')
style.configure('TFrame', background='#222831')
style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), background='#222831', foreground='#FFD369')
style.configure('Display.TEntry', font=('Segoe UI', 22), fieldbackground='#393E46', foreground='#FFD369', borderwidth=0)
style.configure('Result.TEntry', font=('Segoe UI', 16), fieldbackground='#393E46', foreground='#EEEEEE', borderwidth=0)
style.configure('Calc.TButton', font=('Segoe UI', 18), background='#393E46', foreground='#FFD369', borderwidth=0, focusthickness=3, focuscolor='#FFD369')
style.map('Calc.TButton', background=[('active', '#FFD369')], foreground=[('active', '#222831')])
style.configure('Hover.TButton', background='#FFD369', foreground='#222831')

main_frame = ttk.Frame(root, padding=20, style='TFrame')
main_frame.pack(expand=True, fill='both')

title = ttk.Label(main_frame, text="Calculator", style='Title.TLabel', anchor='center')
title.grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky='ew')

entry_var = tk.StringVar()
result_var = tk.StringVar()

entry = ttk.Entry(main_frame, textvariable=entry_var, style='Display.TEntry', justify="right")
entry.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=2, pady=2, ipady=10)
result = ttk.Entry(main_frame, textvariable=result_var, style='Result.TEntry', justify="right", state="readonly")
result.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=2, pady=(0,8), ipady=6)

buttons = [
    "7", "8", "9", "/", "C",
    "4", "5", "6", "*", "⌫",
    "1", "2", "3", "-", "(",
    "0", ".", "%", "+", ")",
    "", "", "=", "", ""
]

row, col = 3, 0
for btn_text in buttons:
    if btn_text:
        btn = ttk.Button(main_frame, text=btn_text, style='Calc.TButton')
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3, ipadx=5, ipady=10)
        btn.bind("<Button-1>", click)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    col += 1
    if col > 4:
        col = 0
        row += 1

for i in range(5):
    main_frame.columnconfigure(i, weight=1)
for i in range(row+1):
    main_frame.rowconfigure(i, weight=1)

root.bind("<Key>", keypress)
root.mainloop()
