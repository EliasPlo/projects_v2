import sqlite3
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog

# Luo salausavain ja tallenna se tiedostoon (tehdään kerran)
def generate_key():
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as key_file:
        key_file.write(key)

# Lataa salausavain tiedostosta
def load_key():
    with open("encryption.key", "rb") as key_file:
        return key_file.read()

# Salaa data
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Pura salattu data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# Luo tietokanta ja taulu, jos niitä ei ole
def initialize_database():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        encrypted_password TEXT NOT NULL,
                        notes TEXT
                      )''')
    conn.commit()
    conn.close()

def initialize_user_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        encrypted_password TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

# Lisää uusi käyttäjä
def add_user(username, password, key):
    encrypted_password = encrypt_data(password, key)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, encrypted_password) VALUES (?, ?)", (username, encrypted_password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Virhe", "Käyttäjänimi on jo käytössä.")
    finally:
        conn.close()

# Tarkista käyttäjän kirjautumistiedot
def authenticate_user(username, password, key):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and decrypt_data(result[0], key) == password:
        return True
    return False

# Lisää salasana tietokantaan
def add_password(username, password, notes, key):
    encrypted_password = encrypt_data(password, key)
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (username, encrypted_password, notes) VALUES (?, ?, ?)",
                   (username, encrypted_password, notes))
    conn.commit()
    conn.close()

# Hakee salasanat käyttäjätunnukselle
def get_passwords(username, key):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_password, notes FROM passwords WHERE username = ?", (username,))
    results = cursor.fetchall()
    conn.close()
    return [(decrypt_data(row[0], key), row[1]) for row in results]

# Poistaa tietyn käyttäjän kaikki salasanat
def delete_passwords(username):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE username = ?", (username,))
    conn.commit()
    conn.close()

# Graafinen käyttöliittymä
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Salasanahallinta")
        
        self.key = load_key()
        self.logged_in_user = None
        
        tk.Label(root, text="Käyttäjätunnus:").grid(row=0, column=0)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Salasana:").grid(row=1, column=0)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(root, text="Kirjaudu sisään", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="Luo käyttäjä", command=self.create_user).grid(row=3, column=0, columnspan=2)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            add_user(username, password, self.key)
            messagebox.showinfo("Onnistui", "Käyttäjä luotu!")
        else:
            messagebox.showwarning("Virhe", "Käyttäjätunnus ja salasana vaaditaan.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            if authenticate_user(username, password, self.key):
                self.logged_in_user = username
                self.show_main_interface()
            else:
                messagebox.showerror("Virhe", "Väärä käyttäjätunnus tai salasana.")
        else:
            messagebox.showwarning("Virhe", "Käyttäjätunnus ja salasana vaaditaan.")

    def show_main_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=f"Tervetuloa, {self.logged_in_user}!").grid(row=0, column=0, columnspan=2)
        
        tk.Label(self.root, text="Salasana:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)
        
        tk.Label(self.root, text="Muistiinpanot:").grid(row=2, column=0)
        self.notes_entry = tk.Entry(self.root)
        self.notes_entry.grid(row=2, column=1)
        
        tk.Button(self.root, text="Lisää salasana", command=self.add_password).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text="Näytä salasanat", command=self.get_passwords).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Kirjaudu ulos", command=self.logout).grid(row=5, column=0, columnspan=2)

    def add_password(self):
        password = self.password_entry.get()
        notes = self.notes_entry.get()
        if password:
            add_password(self.logged_in_user, password, notes, self.key)
            messagebox.showinfo("Onnistui", "Salasana lisätty!")
        else:
            messagebox.showwarning("Virhe", "Salasana vaaditaan.")

    def get_passwords(self):
        results = get_passwords(self.logged_in_user, self.key)
        if results:
            result_text = "\n".join([f"Salasana: {res[0]}, Muistiinpanot: {res[1]}" for res in results])
            messagebox.showinfo("Salasanat", result_text)
        else:
            messagebox.showinfo("Ei löydy", "Ei salasanoja.")

    def logout(self):
        self.logged_in_user = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

if __name__ == "__main__":
    # Luo avain vain, jos sitä ei ole jo olemassa
    try:
        open("encryption.key", "rb")
    except FileNotFoundError:
        generate_key()

    initialize_database()
    initialize_user_database()

    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()