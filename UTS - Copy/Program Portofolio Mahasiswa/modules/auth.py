import sqlite3
import hashlib
from getpass import getpass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    """
    Menangani proses login dan mengembalikan data pengguna jika berhasil.
    """
    print("--- HALAMAN LOGIN ---")
    username = input("Username: ")
    password = getpass("Password: ") # getpass menyembunyikan input password
    
    hashed_password = hash_password(password)

    conn = sqlite3.connect('portfolio.db')
    conn.row_factory = sqlite3.Row # Mengakses kolom dengan nama
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Pengguna WHERE username = ? AND password = ?",
        (username, hashed_password)
    )
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return dict(user) # Mengembalikan data user sebagai dictionary
    else:
        return None