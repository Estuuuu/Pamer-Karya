# file: modules/register.py

import sqlite3
import hashlib
from getpass import getpass
import os

# --- KATA KUNCI PENDAFTARAN ---
KODE_AKSES_MAHASISWA = "212"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def register_new_student():
    """
    Fungsi untuk user mendaftarkan diri sendiri sebagai mahasiswa.
    """
    clear_screen()
    print("--- Registrasi Akun Mahasiswa Baru ---")
    
    kode_input = getpass("Masukkan Kode Akses Pendaftaran Mahasiswa: ")
    
    if kode_input != KODE_AKSES_MAHASISWA:
        print("\n[GAGAL] Kode Akses salah. Anda tidak bisa mendaftar sebagai mahasiswa.")
        return 

    print("\nKode Akses valid. Silakan lanjutkan pendaftaran.")
    
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    try:
        print("\n-- Langkah 1: Isi Biodata Diri --")
        nim = input("NIM: ").strip()
        nama = input("Nama Lengkap: ").strip()
        tgl_lahir = input("Tanggal Lahir (YYYY-MM-DD): ").strip()
        fakultas = input("Fakultas: ").strip()
        prodi = input("Program Studi: ").strip()
        angkatan = int(input("Tahun Angkatan: "))
        email = input("Email: ").strip()

        print("\n-- Langkah 2: Buat Akun Login Anda --")
        username = input(f"Buat Username (rekomendasi: {nim}): ") or nim
        password = getpass("Buat Password: ")
        password_confirm = getpass("Konfirmasi Password: ")

        if not all([nim, nama, prodi, angkatan, email, username, password]):
            print("\n[GAGAL] Semua field wajib diisi.")
            conn.close()
            return
        
        if password != password_confirm:
            print("\n[GAGAL] Password tidak cocok.")
            conn.close()
            return

        #menyimpan data ke databasn
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Buat akun login di tabel Pengguna
        cursor.execute(
            "INSERT INTO Pengguna (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, 'mahasiswa')
        )
        id_pengguna_baru = cursor.lastrowid

        # Simpan biodata di tabel Mahasiswa
        cursor.execute(
            "INSERT INTO Mahasiswa (NIM, nama_mahasiswa, tanggal_lahir, fakultas, prodi, tahun_angkatan, email, id_pengguna) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (nim, nama, tgl_lahir, fakultas, prodi, angkatan, email, id_pengguna_baru)
        )
        
        # C. Buat "wadah" portofolio kosong
        judul_default = f"Portofolio {nama}"
        deskripsi_default = f"Kumpulan karya dan pencapaian oleh {nama}."
        cursor.execute(
            "INSERT INTO Portofolio (judul, deskripsi, NIM) VALUES (?, ?, ?)",
            (judul_default, deskripsi_default, nim)
        )

        conn.commit()
        print(f"\n[SUKSES] Registrasi berhasil! Selamat datang, {nama}.")
        print(f"Silakan login menggunakan username '{username}'.")

    except sqlite3.IntegrityError as e:
        print(f"\n[GAGAL] Registrasi gagal. NIM, Email, atau Username mungkin sudah terdaftar.")
        conn.rollback()
    except ValueError:
        print("\n[GAGAL] Tahun angkatan harus berupa angka.")
        conn.rollback()
    except Exception as e:
        print(f"\nTerjadi error: {e}")
        conn.rollback()
    finally:
        conn.close()