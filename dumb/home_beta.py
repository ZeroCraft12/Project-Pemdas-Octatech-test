import sqlite3
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore

# --- TAMBAHAN PENTING: Import Komponen UI agar dikenali ---
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

KV = '''
ScreenManager:
    id: screen_manager
    LoginScreen:
        name: 'login_screen'
    MainScreen:
        name: 'main_screen'

<LoginScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        adaptive_height: True

        MDLabel:
            text: "SISTEM LOGIN"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: user_field
            hint_text: "Username"
            mode: "rectangle"
        
        MDTextField:
            id: pass_field
            hint_text: "Password"
            password: True
            mode: "rectangle"

        MDRaisedButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            on_release: app.proses_login(user_field.text, pass_field.text)
        
        MDFlatButton:
            text: "Buat Akun Demo (Irfan/123)"
            pos_hint: {"center_x": .5}
            on_release: app.buat_akun_demo()

<MainScreen>:
    MDBoxLayout:
        orientation: "vertical"
        pos_hint: {"center_x": .5, "center_y": .5}
        adaptive_height: True
        spacing: "20dp"
        
        MDLabel:
            id: welcome_label
            text: "Berhasil Masuk!"
            halign: "center"
            font_style: "H4"
        
        MDRaisedButton:
            text: "LOGOUT"
            md_bg_color: "red"
            pos_hint: {"center_x": .5}
            on_release: app.proses_logout()
'''

class LoginScreen(MDScreen):
    pass

class MainScreen(MDScreen):
    pass

class AplikasiLengkap(MDApp):
    def build(self):
        # Warna tema agar terlihat lebih jelas
        self.theme_cls.primary_palette = "Blue"
        
        # 1. Siapkan JsonStore (Session)
        self.store = JsonStore('session.json')
        
        # 2. Siapkan SQLite (Database Utama)
        self.koneksi_db() 
        
        return Builder.load_string(KV)

    def koneksi_db(self):
        # Membuat/Menghubungkan ke database
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        
        # Membuat tabel jika belum ada
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        """)
        self.conn.commit()

    def on_start(self):
        # --- LOGIKA PERSISTENT LOGIN (Cek JsonStore) ---
        # Cek apakah file session.json ada DAN kuncinya ada
        if self.store.exists('session'):
            user = self.store.get('session')['username']
            print(f"Session ditemukan untuk: {user}")
            self.root.ids.screen_manager.current = 'main_screen'
            self.root.ids.screen_manager.get_screen('main_screen').ids.welcome_label.text = f"Halo, {user}"

    def buat_akun_demo(self):
        # Fungsi bantuan untuk mengisi database
        try:
            self.cursor.execute("INSERT INTO users VALUES (?, ?)", ('Irfan', '123'))
            self.conn.commit()
            print("Akun demo berhasil dibuat: Irfan / 123")
        except sqlite3.IntegrityError:
            print("Akun Irfan sudah ada di database.")

    def proses_login(self, username, password):
        # --- LOGIKA UTAMA (Cek SQLite) ---
        
        # Query: Cari user dengan nama DAN password yang cocok
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone() # Ambil satu hasil

        if result:
            print("Login Berhasil! Data ditemukan di SQLite.")
            
            # SIMPAN SESI KE JSONSTORE
            self.store.put('session', username=username, logged_in=True)
            
            # Pindah Layar
            self.root.ids.screen_manager.current = 'main_screen'
            self.root.ids.screen_manager.get_screen('main_screen').ids.welcome_label.text = f"Halo, {username}"
            
            # Bersihkan inputan password
            self.root.ids.screen_manager.get_screen('login_screen').ids.pass_field.text = ""
            
        else:
            print("Gagal. Username atau Password salah.")

    def proses_logout(self):
        # Hapus sesi dari JsonStore
        if self.store.exists('session'):
            self.store.delete('session')
            print("Sesi dihapus.")
        
        self.root.ids.screen_manager.current = 'login_screen'

    def on_stop(self):
        # Tutup koneksi database saat aplikasi ditutup
        self.conn.close()

if __name__ == '__main__':
    AplikasiLengkap().run()