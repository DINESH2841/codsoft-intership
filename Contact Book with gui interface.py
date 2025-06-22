import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.contacts = load_contacts()
        self.selected_index = None

        # Center window
        self.center_window(500, 350)

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f4f8')
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TLabel', background='#f0f4f8', font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), background='#4f8cff', foreground='white')

        # Main Frame
        self.frame = ttk.Frame(root, padding=15)
        self.frame.pack(fill='both', expand=True)

        # Title
        ttk.Label(self.frame, text="Contact Book", style='Header.TLabel', anchor='center').grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky='ew')

        # Contact List with Scrollbar
        list_frame = ttk.Frame(self.frame)
        list_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky='ew')
        self.listbox = tk.Listbox(list_frame, width=40, height=10, font=('Segoe UI', 10), relief='flat', highlightthickness=1, bd=1)
        self.listbox.pack(side='left', fill='y')
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Buttons
        ttk.Button(self.frame, text="Add Contact", command=self.add_contact).grid(row=2, column=0, pady=8, padx=2)
        ttk.Button(self.frame, text="View Details", command=self.view_contact).grid(row=2, column=1, pady=8, padx=2)
        ttk.Button(self.frame, text="Update Contact", command=self.update_contact).grid(row=2, column=2, pady=8, padx=2)
        ttk.Button(self.frame, text="Delete Contact", command=self.delete_contact).grid(row=2, column=3, pady=8, padx=2)

        # Search
        ttk.Label(self.frame, text="Search:").grid(row=3, column=0, sticky='e', pady=10)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.frame, textvariable=self.search_var, width=25)
        self.search_entry.grid(row=3, column=1, columnspan=2, sticky='w', pady=10)
        ttk.Button(self.frame, text="Search", command=self.search_contact).grid(row=3, column=3, padx=2, pady=10)

        self.refresh_list()

    def center_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def refresh_list(self, contacts=None):
        self.listbox.delete(0, tk.END)
        if contacts is None:
            contacts = self.contacts
        for idx, contact in enumerate(contacts):
            display = f"{contact['name']} - {contact['phone']}"
            self.listbox.insert(tk.END, display)

    def add_contact(self):
        ContactForm(self.root, self, "Add Contact")

    def view_contact(self):
        idx = self.get_selected_index()
        if idx is not None:
            contact = self.contacts[idx]
            info = (
                f"Name: {contact['name']}\n"
                f"Phone: {contact['phone']}\n"
                f"Email: {contact['email']}\n"
                f"Address: {contact['address']}"
            )
            messagebox.showinfo("Contact Details", info)
        else:
            messagebox.showwarning("No Selection", "Please select a contact to view.")

    def update_contact(self):
        idx = self.get_selected_index()
        if idx is not None:
            ContactForm(self.root, self, "Update Contact", idx)
        else:
            messagebox.showwarning("No Selection", "Please select a contact to update.")

    def delete_contact(self):
        idx = self.get_selected_index()
        if idx is not None:
            confirm = messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?")
            if confirm:
                del self.contacts[idx]
                save_contacts(self.contacts)
                self.refresh_list()
        else:
            messagebox.showwarning("No Selection", "Please select a contact to delete.")

    def search_contact(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self.refresh_list()
            return
        filtered = [
            c for c in self.contacts
            if query in c['name'].lower() or query in c['phone']
        ]
        self.refresh_list(filtered)

    def on_select(self, event):
        try:
            self.selected_index = self.listbox.curselection()[0]
        except IndexError:
            self.selected_index = None

    def get_selected_index(self):
        try:
            return self.listbox.curselection()[0]
        except IndexError:
            return None

    def add_contact_data(self, contact):
        self.contacts.append(contact)
        save_contacts(self.contacts)
        self.refresh_list()

    def update_contact_data(self, idx, contact):
        self.contacts[idx] = contact
        save_contacts(self.contacts)
        self.refresh_list()

class ContactForm(tk.Toplevel):
    def __init__(self, parent, app, title, idx=None):
        super().__init__(parent)
        self.app = app
        self.idx = idx
        self.title(title)
        self.resizable(False, False)
        self.configure(bg='#eaf1fb')

        # Center window
        self.update_idletasks()
        w, h = 320, 220
        x = self.winfo_screenwidth() // 2 - w // 2
        y = self.winfo_screenheight() // 2 - h // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Fields
        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky='e', padx=8, pady=8)
        ttk.Label(self, text="Phone:").grid(row=1, column=0, sticky='e', padx=8, pady=8)
        ttk.Label(self, text="Email:").grid(row=2, column=0, sticky='e', padx=8, pady=8)
        ttk.Label(self, text="Address:").grid(row=3, column=0, sticky='e', padx=8, pady=8)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        ttk.Entry(self, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=8, pady=8)
        ttk.Entry(self, textvariable=self.phone_var, width=30).grid(row=1, column=1, padx=8, pady=8)
        ttk.Entry(self, textvariable=self.email_var, width=30).grid(row=2, column=1, padx=8, pady=8)
        ttk.Entry(self, textvariable=self.address_var, width=30).grid(row=3, column=1, padx=8, pady=8)

        if idx is not None:
            contact = self.app.contacts[idx]
            self.name_var.set(contact['name'])
            self.phone_var.set(contact['phone'])
            self.email_var.set(contact['email'])
            self.address_var.set(contact['address'])

        ttk.Button(self, text="Save", command=self.save_contact).grid(row=4, column=0, columnspan=2, pady=15)

    def save_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showerror("Input Error", "Name and Phone are required.")
            return

        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }

        if self.idx is None:
            self.app.add_contact_data(contact)
        else:
            self.app.update_contact_data(self.idx, contact)
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()