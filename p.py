from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Set ukuran window simulasi HP
Window.size = (360, 640)

# --- LAYAR 1: MENU ---
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        
        # 1. Buat Layout container
        layout = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            adaptive_height=True # Tips: Agar layout menyesuaikan konten di tengah
        )

        # 2. Buat Widget
        label = MDLabel(
            text="Halaman Menu Utama",
            halign="center",
            font_style="Headline",
            role="medium" # Style baru di KivyMD 2.0
        )
        
        # PERBAIKAN DI SINI:
        # MDButton membungkus MDButtonText
        btn_go = MDButton(
            MDButtonText(
                text="Lihat Data Science",
            ),
            style="filled", # "filled" memberi warna background otomatis
            pos_hint={"center_x": 0.5},
        )
        
        btn_go.bind(on_release=self.pindah_layar)

        # 3. Susun Widget
        layout.add_widget(label)
        layout.add_widget(btn_go)
        self.add_widget(layout)

    def pindah_layar(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'data_screen'


# --- LAYAR 2: DATA ---
class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)
        
        layout = MDBoxLayout(
            orientation='vertical', 
            padding=20, 
            spacing=20,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            adaptive_height=True
        )
        
        label = MDLabel(
            text="Visualisasi Data",
            halign="center",
            theme_text_color="Custom",
            text_color="red"
        )
        
        # PERBAIKAN DI SINI JUGA:
        btn_back = MDButton(
            MDButtonText(
                text="Kembali"
            ),
            style="outlined", # "outlined" memberi border tanpa warna isi
            pos_hint={"center_x": 0.5}
        )
        btn_back.bind(on_release=self.kembali_ke_menu)

        layout.add_widget(label)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def kembali_ke_menu(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_screen'


# --- APLIKASI UTAMA ---
class DataApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue" # Mengatur tema warna aplikasi
        
        sm = ScreenManager()
        screen_menu = MenuScreen(name='menu_screen')
        screen_data = DataScreen(name='data_screen')
        
        sm.add_widget(screen_menu)
        sm.add_widget(screen_data)
        
        return sm

if __name__ == '__main__':
    DataApp().run()