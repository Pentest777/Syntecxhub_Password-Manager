🔐 Project 2: Password Manager

A secure CLI-based Password Manager built in Python that stores user credentials in an encrypted format using strong cryptographic techniques.

🚀 Features
🔒 AES-based Encryption (Fernet)
🔑 Master Password Protection
📁 Secure Local Storage (Encrypted JSON)
➕ Add new credentials (site, username, password)
👀 View saved passwords
🗑 Delete stored credentials
🔍 Search entries by keyword
💾 Automatic save on exit
🛠️ Technologies Used
Python 3
cryptography library (Fernet encryption)
JSON for storage
SHA-256 for key generation
📂 Project Structure
password-manager/
│
├── project2.py        # Main application file
├── vault.json         # Encrypted password storage
├── key.key            # Master key (generated on first run)
└── README.md
🔐 How It Works
On first run:
User sets a Master Password
A key is generated using SHA-256
Empty vault is encrypted and stored
On login:
User enters master password
Key is regenerated and matched
Data Security:
All credentials are stored in encrypted format
Uses Fernet (symmetric encryption)
▶️ How to Run
1. Install dependencies
pip install cryptography
2. Run the program
python project2.py
📌 Usage
===== PASSWORD MANAGER =====
1. Add Password
2. View Passwords
3. Delete Password
4. Search
5. Exit
