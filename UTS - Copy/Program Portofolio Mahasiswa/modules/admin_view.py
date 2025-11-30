import sqlite3
import os
import hashlib
from getpass import getpass

KODE_RAHASIA = '123'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_new_admin():
    clear_screen()
    print("--- Tambah Admin Baru ---")
    if getpass("Masukkan Kode Rahasia: ") != KODE_RAHASIA:
        print("Kode salah.")
        return

    try:
        u = input("Username Admin Baru: ").strip()
        p = getpass("Password: ")
        if not u or not p:
            print("Username/Password tidak boleh kosong.")
            return

        conn = sqlite3.connect('portfolio.db')
        conn.execute("INSERT INTO Pengguna (username, password, role) VALUES (?, ?, ?)", 
                     (u, hashlib.sha256(p.encode()).hexdigest(), 'admin'))
        conn.commit()
        conn.close()
        print(f"Admin '{u}' berhasil dibuat.")
    except Exception as e:
        print(f"Gagal: {e}")

def view_all_portfolios_admin():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id_portofolio, p.judul, m.nama_mahasiswa, m.NIM 
        FROM Portofolio p 
        JOIN Mahasiswa m ON p.NIM = m.NIM
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    print("\n--- DAFTAR SEMUA PORTOFOLIO ---")
    if not rows: print("Belum ada data.")
    for r in rows: print(f"ID Porto: {r[0]} | {r[1]} | Oleh: {r[2]} ({r[3]})")
    return True

def get_full_portfolio_details(portfolio_id):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT judul FROM Portofolio WHERE id_portofolio = ?", (portfolio_id,))
    if not cursor.fetchone():
        print("Portofolio tidak ditemukan.")
        conn.close()
        return

    print(f"\n--- DETAIL PORTOFOLIO (ID: {portfolio_id}) ---")
    
    print("\n[ Pengalaman ]")
    cursor.execute("SELECT id_pengalaman, nama_kegiatan, peran FROM Pengalaman WHERE id_portofolio = ?", (portfolio_id,))
    rows = cursor.fetchall()
    if rows:
        for r in rows: print(f"  ID Item: {r[0]} | {r[1]} ({r[2]})")
    else:
        print("  (Kosong)")

    print("\n[ Sertifikat ]")
    cursor.execute("SELECT id_sertifikat, nama_sertifikat, penerbit FROM Sertifikat WHERE id_portofolio = ?", (portfolio_id,))
    rows = cursor.fetchall()
    if rows:
        for r in rows: print(f"  ID Item: {r[0]} | {r[1]} ({r[2]})")
    else:
        print("  (Kosong)")
    
    conn.close()
    print("-" * 30)
def delete_specific_item():
    clear_screen()
    print("--- HAPUS ITEM (SERTIFIKAT/PENGALAMAN) ---")
    view_all_portfolios_admin()
    try:
        p_id = int(input("\nMasukkan ID Portofolio target untuk melihat isinya: "))
        get_full_portfolio_details(p_id)
        
        print("\nApa yang mau dihapus dari mahasiswa ini?")
        print("1. Hapus Pengalaman")
        print("2. Hapus Sertifikat")
        print("3. Batal")
        choice = input("Pilih: ")
        
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        if choice == '1':
            item_id = int(input("Masukkan ID ITEM Pengalaman: "))
            cursor.execute("DELETE FROM Pengalaman WHERE id_pengalaman = ?", (item_id,))
            if cursor.rowcount > 0: print("Pengalaman berhasil dihapus paksa.")
            else: print("ID Item tidak ditemukan.")
            
        elif choice == '2':
            item_id = int(input("Masukkan ID ITEM Sertifikat: "))
            cursor.execute("DELETE FROM Sertifikat WHERE id_sertifikat = ?", (item_id,))
            if cursor.rowcount > 0: print("Sertifikat berhasil dihapus paksa.")
            else: print("ID Item tidak ditemukan.")
            
        conn.commit()
        conn.close()
        
    except ValueError:
        print("Input harus angka.")

def delete_student_total():
    clear_screen()
    print("--- HAPUS MAHASISWA (TOTAL) ---")
    view_all_portfolios_admin()
    
    try:
        p_id = input("\nMasukkan ID Portofolio mahasiswa yg mau di-BAN: ")
        if input("Yakin hapus akun, biodata, & porto dia? (y/n): ").lower() == 'y':
            conn = sqlite3.connect('portfolio.db')
            cursor = conn.cursor()
            cursor.execute('SELECT m.id_pengguna FROM Portofolio p JOIN Mahasiswa m ON p.NIM=m.NIM WHERE p.id_portofolio=?', (p_id,))
            res = cursor.fetchone()
            
            if res:
                cursor.execute("DELETE FROM Pengguna WHERE id_pengguna=?", (res[0],))
                conn.commit()
                print("Mahasiswa dihapus permanen.")
            else:
                print("ID tidak valid.")
            conn.close()
    except: print("Error.")

def admin_menu(admin_data):
    while True:
        clear_screen()
        print(f"=== ADMIN PANEL ({admin_data['username']}) ===")
        print("1. Lihat Detail Portofolio")
        print("2. Tambah Admin Baru")
        print("3. Hapus Portofolio (Sertifikat/Pengalaman)") 
        print("4. Hapus Mahasiswa (Banned)")
        print("5. Logout")

        c = input("Pilih menu: ")
        
        if c == '1':
            view_all_portfolios_admin()
            try:
                if i := input("\nMasukan ID Porto untuk detail (Enter utk batal): "):
                    get_full_portfolio_details(int(i))
            except: print("ID salah.")
            input("\nEnter...")
        elif c == '2':
            add_new_admin()
            input("\nEnter...")
        elif c == '3':
            delete_specific_item() 
            input("\nEnter...")
        elif c == '4':
            delete_student_total()
            input("\nEnter...")
        elif c == '5':

            break
