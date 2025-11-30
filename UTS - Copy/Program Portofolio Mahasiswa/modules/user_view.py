import sqlite3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_mahasiswa_data(id_pengguna):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.NIM, m.nama_mahasiswa, p.id_portofolio
        FROM Mahasiswa m
        JOIN Portofolio p ON m.NIM = p.NIM
        WHERE m.id_pengguna = ?
    ''', (id_pengguna,))
    data = cursor.fetchone()
    conn.close()
    return data 

def lihat_portfolio_saya(id_portofolio, nim, nama):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT judul, deskripsi FROM Portofolio WHERE id_portofolio = ?", (id_portofolio,))
    portfolio = cursor.fetchone()

    clear_screen()
    print(f"--- Portofolio Milik: {nama} ({nim}) ---")
    print(f"Judul: {portfolio[0]}")
    print(f"Deskripsi: {portfolio[1]}")
    
    print("\n[ Pengalaman Saya ]")
    cursor.execute("SELECT id_pengalaman, nama_kegiatan, peran, durasi FROM Pengalaman WHERE id_portofolio = ?", (id_portofolio,))
    pengalaman_list = cursor.fetchall()
    if pengalaman_list:
        for p in pengalaman_list: print(f"  ID: {p[0]} | {p[1]} sebagai {p[2]} ({p[3]})")
    else: print("  (Belum ada pengalaman ditambahkan)")
        
    print("\n[ Sertifikat Saya ]")
    cursor.execute("SELECT id_sertifikat, nama_sertifikat, penerbit FROM Sertifikat WHERE id_portofolio = ?", (id_portofolio,))
    sertifikat_list = cursor.fetchall()
    if sertifikat_list:
        for s in sertifikat_list: print(f"  ID: {s[0]} | {s[1]}, oleh {s[2]}")
    else: print("  (Belum ada sertifikat ditambahkan)")
    conn.close()

def tambah_pengalaman(id_portofolio):
    print("\n-- Menambah Pengalaman Baru --")
    nama_kegiatan = input("Nama Kegiatan: ")
    peran = input("Peran/Jabatan: ")
    durasi = input("Durasi: ")
    
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Pengalaman (nama_kegiatan, peran, durasi, id_portofolio) VALUES (?, ?, ?, ?)", (nama_kegiatan, peran, durasi, id_portofolio))
    conn.commit()
    conn.close()
    print("Pengalaman baru berhasil ditambahkan!")

def tambah_sertifikat(id_portofolio):
    print("\n-- Menambah Sertifikat Baru --")
    nama_sertifikat = input("Nama Sertifikat: ")
    penerbit = input("Diterbitkan oleh: ")
    
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Sertifikat (nama_sertifikat, penerbit, id_portofolio) VALUES (?, ?, ?)", (nama_sertifikat, penerbit, id_portofolio))
    conn.commit()
    conn.close()
    print("Sertifikat baru berhasil ditambahkan!")

def menu_hapus_data(id_portofolio, nim, nama):
    while True:
        lihat_portfolio_saya(id_portofolio, nim, nama) 
        
        print("\n--- MENU HAPUS DATA ---")
        print("1. Hapus Pengalaman")
        print("2. Hapus Sertifikat")
        print("3. Kembali ke Dasbor")
        
        choice = input("Pilih yang mau dihapus: ")
        
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        if choice == '1':
            try:
                id_hapus = int(input("Masukkan ID Pengalaman yang akan dihapus: "))
                cursor.execute("DELETE FROM Pengalaman WHERE id_pengalaman = ? AND id_portofolio = ?", (id_hapus, id_portofolio))
                if cursor.rowcount > 0:
                    print("Pengalaman berhasil dihapus!")
                else:
                    print("ID tidak ditemukan atau bukan milik Anda.")
            except ValueError:
                print("Input harus angka.")
            conn.commit()
            input("Tekan Enter...")

        elif choice == '2':
            try:
                id_hapus = int(input("Masukkan ID Sertifikat yang akan dihapus: "))
                cursor.execute("DELETE FROM Sertifikat WHERE id_sertifikat = ? AND id_portofolio = ?", (id_hapus, id_portofolio))
                if cursor.rowcount > 0:
                    print("Sertifikat berhasil dihapus!")
                else:
                    print("ID tidak ditemukan atau bukan milik Anda.")
            except ValueError:
                print("Input harus angka.")
            conn.commit()
            input("Tekan Enter...")

        elif choice == '3':
            conn.close()
            break
        else:
            print("Pilihan tidak valid.")
            conn.close()

def mahasiswa_menu(user_data):
    nim, nama_mahasiswa, id_portofolio = get_mahasiswa_data(user_data['id_pengguna'])
    
    while True:
        clear_screen()
        print(f"Selamat datang, {nama_mahasiswa}!")
        print("--- Dasbor Portofolio Anda ---")
        print("1. Lihat Portofolio Saya")
        print("2. Tambah Pengalaman")
        print("3. Tambah Sertifikat")
        print("4. Hapus Data (Pengalaman/Sertifikat)") 
        print("5. Lihat Daftar Portofolio Mahasiswa Lain")
        print("6. Logout")
        
        choice = input("Pilih menu: ")

        if choice == '1':
            lihat_portfolio_saya(id_portofolio, nim, nama_mahasiswa)
            input("\nTekan Enter...")
        elif choice == '2':
            tambah_pengalaman(id_portofolio)
            input("\nTekan Enter...")
        elif choice == '3':
            tambah_sertifikat(id_portofolio)
            input("\nTekan Enter...")
        elif choice == '4':
            menu_hapus_data(id_portofolio, nim, nama_mahasiswa) 
        elif choice == '5':
            from modules.admin_view import view_all_portfolios_admin
            view_all_portfolios_admin()
            input("\nTekan Enter...")
        elif choice == '6':
            print("Anda telah logout."); break
        else:

            print("Pilihan tidak valid.")
