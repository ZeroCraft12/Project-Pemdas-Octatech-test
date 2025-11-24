from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
# PERBAIKAN: Import komponen icon dan label untuk NavigationBar
from kivymd.uix.navigationbar import (
    MDNavigationBar, 
    MDNavigationItem, 
    MDNavigationItemIcon, 
    MDNavigationItemLabel
)

# --- 1. SCREEN LOGIN ---
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login_screen"
        self.md_bg_color = self.theme_cls.backgroundColor

        layout = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp",
            adaptive_height=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        title = MDLabel(
            text="Data Science App",
            halign="center",
            font_style="Display",
            role="small",
            theme_text_color="Primary",
        )

        self.user_field = MDTextField(mode="outlined")
        self.user_field.add_widget(MDTextFieldHintText(text="Username"))

        self.pass_field = MDTextField(mode="outlined")
        self.pass_field.add_widget(MDTextFieldHintText(text="Password"))

        btn_login = MDButton(
            style="filled",
            pos_hint={"center_x": 0.5}
        )
        btn_login.add_widget(MDButtonText(text="Masuk (Dummy)"))
        btn_login.bind(on_release=self.go_home)

        layout.add_widget(title)
        layout.add_widget(self.user_field)
        layout.add_widget(self.pass_field)
        layout.add_widget(btn_login)

        self.add_widget(layout)

    def go_home(self, instance):
        self.manager.current = "home_screen"


# --- 2. SCREEN HOME (Dashboard) ---
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home_screen"
        self.md_bg_color = self.theme_cls.backgroundColor

        self.main_layout = MDBoxLayout(orientation="vertical")

        # A. MANAGER KONTEN
        self.content_manager = ScreenManager()

        screen_dash = MDScreen(name="dashboard_tab")
        screen_dash.add_widget(MDLabel(text="Halaman Dashboard (Data Viz)", halign="center"))
        
        screen_profile = MDScreen(name="profile_tab")
        screen_profile.add_widget(MDLabel(text="Halaman Profil User", halign="center"))

        self.content_manager.add_widget(screen_dash)
        self.content_manager.add_widget(screen_profile)

        # B. NAVIGATION BAR (PERBAIKAN DI SINI)
        self.nav_bar = MDNavigationBar()
        self.nav_bar.bind(on_switch_tabs=self.switch_tabs)

        # -- Item 1: Dashboard --
        # Kita buat container Item dulu
        item_dash = MDNavigationItem(active=True)
        # Kita set atribut name secara manual (Python standard attribute)
        item_dash.name = "dashboard_tab"
        
        # Masukkan Icon
        item_dash.add_widget(MDNavigationItemIcon(icon="chart-bar"))
        # Masukkan Label (Teks)
        item_dash.add_widget(MDNavigationItemLabel(text="Dashboard"))
        
        # -- Item 2: Profile --
        item_profile = MDNavigationItem()
        item_profile.name = "profile_tab"
        
        item_profile.add_widget(MDNavigationItemIcon(icon="account"))
        item_profile.add_widget(MDNavigationItemLabel(text="Profile"))

        # Tambahkan item yang sudah lengkap ke navbar
        self.nav_bar.add_widget(item_dash)
        self.nav_bar.add_widget(item_profile)

        self.main_layout.add_widget(self.content_manager)
        self.main_layout.add_widget(self.nav_bar)

        self.add_widget(self.main_layout)

    def switch_tabs(self, bar, item, item_icon, item_text):
        # KivyMD akan mengirim item (objek tombol)
        # Kita akses .name yang tadi kita set manual
        if hasattr(item, 'name'):
            self.content_manager.current = item.name


# --- 3. APP ---
class DataScienceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.root_sm = ScreenManager(transition=FadeTransition())
        self.root_sm.add_widget(LoginScreen())
        self.root_sm.add_widget(HomeScreen())
        self.root_sm.current = "login_screen"
        
        return self.root_sm

if __name__ == "__main__":
    DataScienceApp().run()