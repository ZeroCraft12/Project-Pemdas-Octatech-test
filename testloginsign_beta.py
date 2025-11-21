import sqlite3
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivymd.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivy.uix.image import Image

Window.size = (1000, 600)

# --- DATABASE HELPER ---
def get_db_connection():
    conn = sqlite3.connect("octatech.db")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- HALAMAN 1: LOGIN SCREEN ---
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (1, 1, 1, 1)
        self.build_ui()

    def build_ui(self):
        # ... (Kode UI Login kamu saya rapikan disini) ...
        main_layout = MDBoxLayout(orientation='horizontal')
        
        # BAGIAN KIRI (Gambar)
        left_layout = MDFloatLayout(size_hint_x=0.6)
        # Ganti path sesuai komputer kamu
        bg_image = FitImage(source=r"D:\Project Pemdas Octatech test\Assets\loginpage\Latarbelakang.jpg")
        left_layout.add_widget(bg_image)
        left_layout.add_widget(MDBoxLayout(md_bg_color=(0, 0.5, 1, 0.1))) # Overlay
        
        # BAGIAN KANAN (Form)
        right_layout = MDFloatLayout(size_hint_x=0.4, md_bg_color=(11/255, 20/255, 54/255, 1))
        
        form_box = MDBoxLayout(
            orientation='vertical', adaptive_height=True,
            pos_hint={"center_x": .5, "center_y": .5},
            padding=dp(40), spacing=dp(20)
        )
        
        # Judul
        form_box.add_widget(MDLabel(text="Login", font_style="Headline", role="medium", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1)))
        form_box.add_widget(MDLabel(text="Masuk ke akun OctaTech", theme_text_color="Custom", text_color=(0.7, 0.7, 0.8, 1), font_style="Body", role="small"))

        # Input Username
        self.username_field = MDTextField(mode="filled", theme_bg_color="Custom", fill_color_normal=(1, 1, 1, 1), radius=[10])
        self.username_field.add_widget(MDTextFieldHintText(text="Username"))
        form_box.add_widget(self.username_field)

        # Input Password
        self.password_field = MDTextField(mode="filled", theme_bg_color="Custom", fill_color_normal=(1, 1, 1, 1), radius=[10], password=True, password_mask="•")
        self.password_field.add_widget(MDTextFieldHintText(text="Password"))
        form_box.add_widget(self.password_field)

        # Tombol Sign In
        btn_signin = MDButton(style="filled", theme_bg_color="Custom", md_bg_color=(0, 0.47, 0.8, 1), size_hint_x=1, radius=[dp(10)])
        btn_signin.add_widget(MDButtonText(text="Sign In", theme_text_color="Custom", text_color=(1,1,1,1), pos_hint={"center_x": .5, "center_y": .5}))
        btn_signin.bind(on_release=self.do_login) # Aksi Login
        form_box.add_widget(btn_signin)

        # Link ke Sign Up
        footer_box = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing=dp(5), pos_hint={'center_x': .5})
        footer_box.add_widget(MDLabel(text="Belum punya akun?", theme_text_color="Custom", text_color=(0.7, 0.7, 0.8, 1), halign="right"))
        
        btn_signup = MDButton(style="text")
        btn_signup.add_widget(MDButtonText(text="Sign Up", theme_text_color="Custom", text_color=(1, 0.8, 0, 1), bold=True))
        btn_signup.bind(on_release=self.go_to_signup) # Aksi Pindah Layar
        footer_box.add_widget(btn_signup)
        
        form_box.add_widget(footer_box)
        right_layout.add_widget(form_box)
        
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        self.add_widget(main_layout)

    def do_login(self, instance):
        user = self.username_field.text
        pwd = self.password_field.text
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
        result = cursor.fetchone()
        conn.close()

        if result:
            print(f"LOGIN SUKSES: Halo {user}!")
            # Nanti pindah ke Dashboard disini
        else:
            print("LOGIN GAGAL: Cek username/password.")

    def go_to_signup(self, instance):
        # Fungsi untuk pindah layar
        self.manager.current = "signup_screen"
        self.manager.transition.direction = "left"


# --- HALAMAN 2: SIGN UP SCREEN ---
class SignupScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (11/255, 20/255, 54/255, 1) # Background Navy
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(50), spacing=dp(20), pos_hint={"center_x": .5, "center_y": .5}, size_hint=(None, None), width=dp(400), adaptive_height=True)
        
        layout.add_widget(MDLabel(text="Buat Akun Baru", font_style="Headline", role="medium", halign="center", theme_text_color="Custom", text_color=(1,1,1,1), bold=True))
        
        # Input Baru
        self.new_user = MDTextField(mode="filled", theme_bg_color="Custom", fill_color_normal=(1, 1, 1, 1), radius=[10])
        self.new_user.add_widget(MDTextFieldHintText(text="Username Baru"))
        layout.add_widget(self.new_user)

        self.new_pass = MDTextField(mode="filled", theme_bg_color="Custom", fill_color_normal=(1, 1, 1, 1), radius=[10], password=True)
        self.new_pass.add_widget(MDTextFieldHintText(text="Password Baru"))
        layout.add_widget(self.new_pass)

        # Tombol Daftar
        btn_register = MDButton(style="filled", theme_bg_color="Custom", md_bg_color=(0, 0.8, 0.4, 1), size_hint_x=1, radius=[dp(10)])
        btn_register.add_widget(MDButtonText(text="Daftar Sekarang", pos_hint={"center_x": .5, "center_y": .5}, theme_text_color="Custom", text_color=(1,1,1,1)))
        btn_register.bind(on_release=self.do_register)
        layout.add_widget(btn_register)

        # Tombol Kembali
        btn_back = MDButton(style="text", pos_hint={"center_x": .5})
        btn_back.add_widget(MDButtonText(text="Kembali ke Login", theme_text_color="Custom", text_color=(1,1,1,0.7)))
        btn_back.bind(on_release=self.back_to_login)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def do_register(self, instance):
        user = self.new_user.text
        pwd = self.new_pass.text

        if user == "" or pwd == "":
            print("Isi semua data!")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users VALUES (?, ?)", (user, pwd))
            conn.commit()
            print("REGISTRASI BERHASIL! Silakan login.")
            self.back_to_login(None) # Otomatis balik ke login
        except sqlite3.IntegrityError:
            print("Username sudah terpakai!")
        finally:
            conn.close()

    def back_to_login(self, instance):
        self.manager.current = "login_screen"
        self.manager.transition.direction = "right"


# --- CLASS UTAMA APP ---
class OctaTechApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        init_db() # Pastikan DB siap

        # SCREEN MANAGER: Pengatur lalu lintas halaman
        sm = MDScreenManager()
        
        # Tambahkan layar-layar ke manager
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(SignupScreen(name="signup_screen"))
        
        return sm

if __name__ == "__main__":
    OctaTechApp().run()