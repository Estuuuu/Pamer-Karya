import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    print("Menjalankan setup database dengan struktur final...")
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pengguna (
        id_pengguna INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'mahasiswa'))
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mahasiswa (
        NIM TEXT PRIMARY KEY,
        nama_mahasiswa TEXT NOT NULL,
        tanggal_lahir TEXT,
        fakultas TEXT,
        prodi TEXT,
        tahun_angkatan INTEGER,
        email TEXT UNIQUE,
        id_pengguna INTEGER UNIQUE,
        FOREIGN KEY (id_pengguna) REFERENCES Pengguna(id_pengguna) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Portofolio (
        id_portofolio INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        deskripsi TEXT,
        NIM TEXT UNIQUE,
        FOREIGN KEY (NIM) REFERENCES Mahasiswa(NIM) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sertifikat (
        id_sertifikat INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_sertifikat TEXT NOT NULL,
        penerbit TEXT,
        id_portofolio INTEGER,
        FOREIGN KEY (id_portofolio) REFERENCES Portofolio(id_portofolio) ON DELETE CASCADE
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pengalaman (
        id_pengalaman INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_kegiatan TEXT NOT NULL,
        peran TEXT,
        durasi TEXT,
        id_portofolio INTEGER,
        FOREIGN KEY (id_portofolio) REFERENCES Portofolio(id_portofolio) ON DELETE CASCADE
    )
    ''')

    cursor.execute("SELECT username FROM Pengguna WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO Pengguna (username, password, role) VALUES (?, ?, ?)",
            ('admin', hash_password('admin123'), 'admin')
        )
        print("Admin default 'admin' berhasil dibuat.")

    conn.commit()
    conn.close()
    print("Setup database selesai dan siap digunakan.")

if __name__ == '__main__':

    setup_database()
