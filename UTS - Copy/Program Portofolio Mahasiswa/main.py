import os
from modules import auth, admin_view, user_view, register
from modules import guest_view 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        print("==========================================")
        print("   SELAMAT DATANG DI APLIKASI PORTOFOLIO MAHASISWA  ")
        print("==========================================")
        print("\n--- MENU UTAMA ---")
        print("1. Lihat Portofolio (Mode Tamu)") 
        print("2. Login sebagai Mahasiswa")
        print("3. Login sebagai Admin")
        print("4. Register Akun Mahasiswa")
        print("5. Keluar")

        choice = input("Pilih opsi: ")
        
        if choice == '1': 
            guest_view.guest_menu()

        elif choice == '2':
            user_data = auth.login()
            if user_data and user_data.get('role') == 'mahasiswa':
                user_view.mahasiswa_menu(user_data)
            else:
                print("\nLogin gagal: Username/password salah atau bukan akun mahasiswa.")
                input("Tekan Enter untuk melanjutkan...")

        elif choice == '3':
            user_data = auth.login()
            if user_data and user_data.get('role') == 'admin':
                admin_view.admin_menu(user_data)
            else:
                print("\nLogin gagal: Username/password salah atau bukan akun admin.")
                input("Tekan Enter untuk melanjutkan...")

        elif choice == '4':
            register.register_new_student()
            input("\nTekan Enter untuk kembali...")

        elif choice == '5':
            print("Terima kasih telah menggunakan aplikasi."); break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk melanjutkan...")

if __name__ == '__main__':
    if not os.path.exists('portfolio.db'):
        print("Database 'portfolio.db' tidak ditemukan.")
        print("Silakan jalankan 'python database/setup.py' terlebih dahulu.")
    else:
        main()