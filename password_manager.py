import json
import os
import base64
import getpass
from cryptography.fernet import Fernet
from hashlib import sha256

DATA_FILE = "vault.json"
KEY_FILE = "key.key"

# =========================
# KEY GENERATION
# =========================
def generate_key(master_password):
    return base64.urlsafe_b64encode(sha256(master_password.encode()).digest())

# =========================
# LOAD / SAVE DATA
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# =========================
# ENCRYPT / DECRYPT
# =========================
def encrypt_data(data, fernet):
    return fernet.encrypt(json.dumps(data).encode()).decode()

def decrypt_data(data, fernet):
    return json.loads(fernet.decrypt(data.encode()).decode())

# =========================
# INITIAL SETUP
# =========================
def setup():
    if not os.path.exists(KEY_FILE):
        print("\n🔐 First Time Setup")
        master = getpass.getpass("Set Master Password: ")
        key = generate_key(master)

        with open(KEY_FILE, "wb") as f:
            f.write(key)

        fernet = Fernet(key)
        encrypted = encrypt_data({}, fernet)
        save_data({"data": encrypted})

        print("✅ Setup Complete!\n")

# =========================
# LOGIN
# =========================
def login():
    master = getpass.getpass("Enter Master Password: ")
    key = generate_key(master)

    try:
        with open(KEY_FILE, "rb") as f:
            stored_key = f.read()

        if key != stored_key:
            print("❌ Wrong Password!")
            return None

        return Fernet(key)

    except:
        print("Error loading key!")
        return None

# =========================
# FEATURES
# =========================
def add_entry(data):
    site = input("Site: ")
    user = input("Username: ")
    pwd = getpass.getpass("Password: ")

    data[site] = {"username": user, "password": pwd}
    print("✅ Saved!")

def view_entries(data):
    for site, creds in data.items():
        print(f"\n🌐 {site}")
        print(f"👤 {creds['username']}")
        print(f"🔑 {creds['password']}")

def delete_entry(data):
    site = input("Enter site to delete: ")
    if site in data:
        del data[site]
        print("🗑 Deleted!")
    else:
        print("❌ Not found")

def search_entry(data):
    keyword = input("Search: ")
    for site in data:
        if keyword.lower() in site.lower():
            print(f"🔍 Found: {site}")

# =========================
# MAIN MENU
# =========================
def main():
    setup()
    fernet = login()

    if not fernet:
        return

    raw = load_data()
    data = decrypt_data(raw["data"], fernet)

    while True:
        print("\n===== PASSWORD MANAGER =====")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Delete Password")
        print("4. Search")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_entry(data)

        elif choice == "2":
            view_entries(data)

        elif choice == "3":
            delete_entry(data)

        elif choice == "4":
            search_entry(data)

        elif choice == "5":
            encrypted = encrypt_data(data, fernet)
            save_data({"data": encrypted})
            print("💾 Saved & Exiting...")
            break

        else:
            print("Invalid option!")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
