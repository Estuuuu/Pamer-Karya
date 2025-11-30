import sqlite3
import os
from modules.admin_view import get_full_portfolio_details 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cari_portfolio(filter_by, keyword):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    query = f'''
        SELECT p.id_portofolio, p.judul, m.nama_mahasiswa, m.fakultas, m.prodi
        FROM Portofolio p
        JOIN Mahasiswa m ON p.NIM = m.NIM
        WHERE m.{filter_by} LIKE ? 
    '''
    
    cursor.execute(query, ('%' + keyword + '%',))
    results = cursor.fetchall()
    conn.close()
    
    clear_screen()
    if not results:
        print(f"Tidak ditemukan portofolio dengan {filter_by} mengandung '{keyword}'.")
        return

    print(f"--- Hasil Pencarian untuk '{keyword}' di {filter_by} ---")
    for row in results:
        print(f"ID: {row[0]} | Judul: {row[1]} | Pemilik: {row[2]} ({row[3]} - {row[4]})")

def guest_menu():
    """Menu utama untuk mode tamu."""
    while True:
        clear_screen()
        print("--- Mode Tamu: Jelajahi Portofolio Mahasiswa ---")
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id_portofolio, p.judul, m.nama_mahasiswa, m.fakultas, m.prodi
            FROM Portofolio p
            JOIN Mahasiswa m ON p.NIM = m.NIM
        ''')
        portfolios = cursor.fetchall()
        conn.close()

        if not portfolios:
            print("\nBelum ada portofolio yang bisa ditampilkan.")
        else:
            print("\n[ Daftar Semua Portofolio ]")
            for p in portfolios:
                print(f"ID: {p[0]} | Judul: {p[1]} | Pemilik: {p[2]} ({p[3]} - {p[4]})")
        
        print("\n--- Opsi ---")
        print("1. Cari Berdasarkan Fakultas")
        print("2. Cari Berdasarkan Prodi")
        print("3. Lihat Detail Portofolio (Masukkan ID)")
        print("4. Kembali ke Menu Utama")

        choice = input("Pilihan Anda: ")

        if choice == '1':
            keyword = input("Masukkan nama Fakultas: ").strip()
            cari_portfolio('fakultas', keyword)
        elif choice == '2':
            keyword = input("Masukkan nama Prodi: ").strip()
            cari_portfolio('prodi', keyword)
        elif choice == '3':
            try:
                p_id = int(input("Masukkan ID Portofolio: "))
                get_full_portfolio_details(p_id)
            except ValueError:
                print("Input ID tidak valid.")
        elif choice == '4':
            break
        else:
            print("Pilihan tidak valid.")
        

        input("\nTekan Enter untuk melanjutkan...")
