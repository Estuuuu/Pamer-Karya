import sqlite3
import hashlib
from getpass import getpass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    print("--- HALAMAN LOGIN ---")
    username = input("Username: ")
    password = getpass("Password: ") 
    
    hashed_password = hash_password(password)

    conn = sqlite3.connect('portfolio.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Pengguna WHERE username = ? AND password = ?",
        (username, hashed_password)
    )
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return dict(user) 
    else:

        return None
