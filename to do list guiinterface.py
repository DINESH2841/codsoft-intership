import customtkinter as ctk
import json
import os
import tkinter as tk

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def add_task():
    global tasks
    if task_entry is not None:
        task = task_entry.get()
    else:
        task = ""
    if task:
        tasks.append({"task": task, "done": False})
        save_tasks(tasks)
        task_entry.delete(0, ctk.END)
        update_task_list()

def update_task_list():
    task_list.delete(0, tk.END)
    for index, task in enumerate(tasks):
        status = "Done" if task["done"] else "Not Done"
        task_list.insert(tk.END, f"{index + 1}. {task['task']} - {status}")
def mark_task_done():
    global tasks
    selected = task_list.curselection()
    if selected:
        idx = selected[0]
        tasks[idx]["done"] = True
        save_tasks(tasks)
        update_task_list()
def mark_task_not_done():
    global tasks
    selected = task_list.curselection()
    if selected:
        idx = selected[0]
        tasks[idx]["done"] = False
        save_tasks(tasks)
        update_task_list()
def delete_task():
    global tasks
    selected = task_list.curselection()
    if selected:
        idx = selected[0]
        tasks.pop(idx)
        save_tasks(tasks)
        update_task_list()
def sort_tasks():
    global tasks
    sort_type = sort_var.get()
    if sort_type == "Number Ascending":
        # Original order (by insertion)
        pass  # Do nothing, already in order
    elif sort_type == "Number Descending":
        tasks.reverse()
    elif sort_type == "Alphabet Ascending":
        tasks.sort(key=lambda x: x["task"].lower())
    elif sort_type == "Alphabet Descending":
        tasks.sort(key=lambda x: x["task"].lower(), reverse=True)
    save_tasks(tasks)
    update_task_list()

# Create the main application window
app = ctk.CTk()
app.title("To-Do List")

# Create the task entry field
task_entry = ctk.CTkEntry(app, placeholder_text="Write your Task here", width=200)
task_entry.pack(pady=10)
add_button = ctk.CTkButton(app, text="Add Task", command=add_task)
add_button.pack(pady=5)

task_list = tk.Listbox(app, width=50, height=15)
task_list.pack(pady=10)
mark_done_button = ctk.CTkButton(app, text="Mark Task as Done", command=mark_task_done)
mark_done_button.pack(pady=5)
mark_not_done_button = ctk.CTkButton(app, text="Mark as Not Done", command=mark_task_not_done)
mark_not_done_button.pack(pady=5)
delete_button = ctk.CTkButton(app, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

# Sort options
sort_var = tk.StringVar(value="Number Ascending")
sort_options = ["Number Ascending", "Number Descending", "Alphabet Ascending", "Alphabet Descending"]
sort_menu = ctk.CTkOptionMenu(app, variable=sort_var, values=sort_options)
sort_menu.pack(pady=5)
sort_button = ctk.CTkButton(app, text="Sort Tasks", command=sort_tasks)
sort_button.pack(pady=5)

tasks = load_tasks()
update_task_list()

def main():
    app.mainloop()

if __name__ == "__main__":
    main()
