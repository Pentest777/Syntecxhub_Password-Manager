import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from cryptography.fernet import Fernet
import base64
import hashlib

DATA_FILE = "vault.dat"
KEY_FILE = "key.key"

# Generate key from master password
def generate_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

# Save data encrypted
def save_data(data, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)

# Load data
def load_data(key):
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "rb") as f:
        encrypted = f.read()

    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except:
        messagebox.showerror("Error", "Wrong Master Password!")
        exit()

# Main App
class PasswordManager:
    def __init__(self, root, key):
        self.root = root
        self.key = key
        self.data = load_data(key)

        root.title("🔐 Password Manager")
        root.geometry("500x400")

        tk.Label(root, text="Website").pack()
        self.site = tk.Entry(root)
        self.site.pack()

        tk.Label(root, text="Username").pack()
        self.user = tk.Entry(root)
        self.user.pack()

        tk.Label(root, text="Password").pack()
        self.passw = tk.Entry(root, show="*")
        self.passw.pack()

        tk.Button(root, text="Add", command=self.add).pack(pady=5)
        tk.Button(root, text="View All", command=self.view).pack(pady=5)
        tk.Button(root, text="Delete", command=self.delete).pack(pady=5)
        tk.Button(root, text="Search", command=self.search).pack(pady=5)

        self.output = tk.Text(root, height=10)
        self.output.pack()

    def add(self):
        site = self.site.get()
        user = self.user.get()
        pwd = self.passw.get()

        if not site or not user or not pwd:
            messagebox.showerror("Error", "Fill all fields")
            return

        self.data[site] = {"username": user, "password": pwd}
        save_data(self.data, self.key)
        messagebox.showinfo("Success", "Saved!")

    def view(self):
        self.output.delete(1.0, tk.END)
        for site, creds in self.data.items():
            self.output.insert(tk.END, f"{site} | {creds['username']} | {creds['password']}\n")

    def delete(self):
        site = self.site.get()
        if site in self.data:
            del self.data[site]
            save_data(self.data, self.key)
            messagebox.showinfo("Deleted", "Entry removed")
        else:
            messagebox.showerror("Error", "Not found")

    def search(self):
        site = self.site.get()
        self.output.delete(1.0, tk.END)

        if site in self.data:
            creds = self.data[site]
            self.output.insert(tk.END, f"{site} | {creds['username']} | {creds['password']}")
        else:
            self.output.insert(tk.END, "Not found")


# Master Password Prompt
root = tk.Tk()
root.withdraw()

master_password = simpledialog.askstring("Master Key", "Enter Master Password:", show="*")

if not master_password:
    exit()

key = generate_key(master_password)

root.deiconify()
app = PasswordManager(root, key)
root.mainloop()