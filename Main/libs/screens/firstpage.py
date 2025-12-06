import os
import sys
from kivy.core.text import LabelBase
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp

# --- SETUP PATH ---
current_file_path = os.path.abspath(__file__)
screens_dir = os.path.dirname(current_file_path)
libs_dir = os.path.dirname(screens_dir)
MAIN_DIR = os.path.dirname(libs_dir)

ASSETS_DIR = os.path.join(MAIN_DIR, "assets")
IMG_DIR = os.path.join(ASSETS_DIR, "Images")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")

# --- LOAD FONT ---
font_montserrat = "Roboto"
font_poppins = "Roboto"

try:
    LabelBase.register(name="Montserrat-Bold", fn_regular=os.path.join(FONT_DIR, "Montserrat-Bold.ttf"))
    LabelBase.register(name="Poppins-Medium", fn_regular=os.path.join(FONT_DIR, "Poppins-Medium.ttf"))
    font_montserrat = "Montserrat-Bold"
    font_poppins = "Poppins-Medium"
except Exception as e:
    print(f"Font Error: {e}")

# --- WARNA ---
COLOR_WHITE = get_color_from_hex("#FFFFFF")
COLOR_PRIMARY = get_color_from_hex("#008AC5")

# =========================================
# TEAM SCREEN
# =========================================
class TeamScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "team_screen"

    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        # 1. Background
        root_layout = MDFloatLayout()
        bg_path = os.path.join(IMG_DIR, "welcome page.jpg")
        if os.path.exists(bg_path):
            bg = FitImage(source=bg_path)
        else:
            bg = MDBoxLayout(md_bg_color=COLOR_PRIMARY)
        root_layout.add_widget(bg)

        # 2. Konten Utama
        content_box = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(40)],
            spacing=dp(20),
            pos_hint={"center_x": .5, "center_y": .5}
        )

        # JUDUL
        lbl_team = MDLabel(
            text="Pembuat Projek",
            halign="center",
            font_style="Headline",
            role="medium",
            font_name=font_montserrat,
            theme_text_color="Custom",
            text_color=COLOR_WHITE,
            size_hint_y=None,
            height=dp(80),
            bold=True
        )
        content_box.add_widget(lbl_team)

        # CONTAINER FOTO
        members_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(25),         # Spacing diperlebar dikit
            size_hint_y=None,
            height=dp(400),         # Tinggi container diperbesar untuk muat foto baru
            adaptive_width=True,
            pos_hint={'center_x': 0.5}
        )

        members = [
            ("furry_lover.jpg", "Furry Lover"),
            ("wowo_subianto.png", "Wowo Subianto"),
            ("zaidan_alfaisi.png", "M. Zaidan Alfaisi")
        ]

        # --- UKURAN FOTO TIM (DIPERBESAR) ---
        # Rasio 3:4 -> Lebar 200 : Tinggi 266
        card_width = dp(200) 
        card_height = dp(266)

        for img_name, name in members:
            # Wrapper (Foto + Teks)
            card = MDBoxLayout(
                orientation="vertical",
                spacing=dp(15),
                size_hint=(None, None),
                width=card_width,
                height=dp(350) # Tinggi total wrapper diperbesar
            )

            # Frame Foto
            card_img_box = MDCard(
                size_hint=(None, None),
                size=(card_width, card_height), # UKURAN FIX BARU
                radius=[15, 15, 15, 15],
                elevation=3,
                md_bg_color=[1, 1, 1, 1]
            )

            full_path = os.path.join(IMG_DIR, img_name)
            photo = FitImage(
                source=full_path if os.path.exists(full_path) else "",
                radius=[15, 15, 15, 15],
            )
            card_img_box.add_widget(photo)

            # Nama
            lbl_name = MDLabel(
                text=name,
                halign="center",
                font_style="Title",
                role="medium",
                font_name=font_poppins,
                theme_text_color="Custom",
                text_color=COLOR_WHITE,
                adaptive_height=True,
                bold=True
            )

            card.add_widget(card_img_box)
            card.add_widget(lbl_name)
            members_box.add_widget(card)

        content_box.add_widget(members_box)
        content_box.add_widget(MDBoxLayout())

        # Footer
        lbl_dosen = MDLabel(
            text="Dosen pengampu: Dr. Atik Wintarti, M.Kom.",
            halign="center",
            font_style="Title",
            role="small",
            theme_text_color="Custom",
            text_color=COLOR_WHITE,
            font_name=font_poppins,
            adaptive_height=True
        )
        content_box.add_widget(lbl_dosen)

        root_layout.add_widget(content_box)
        self.add_widget(root_layout)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.manager:
                self.manager.transition = FadeTransition(duration=0.5)
                self.manager.current = "hero_screen"
            return True
        return super().on_touch_down(touch)


# =========================================
# HERO SCREEN
# =========================================
class HeroScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "hero_screen"

    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        root_layout = MDFloatLayout()
        bg_path = os.path.join(IMG_DIR, "welcome page.jpg")
        if os.path.exists(bg_path):
            bg = FitImage(source=bg_path)
        else:
            bg = MDBoxLayout(md_bg_color=COLOR_PRIMARY)
        root_layout.add_widget(bg)

        content_layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(40), dp(40), dp(40), dp(40)],
            spacing=dp(15)
        )

        title = MDLabel(
            text="Cari gadget\nterbaik untukmu!",
            font_style="Display",
            role="small",
            font_name=font_montserrat,
            halign="left",
            theme_text_color="Custom",
            text_color=COLOR_WHITE,
            adaptive_height=True,
            bold=True,
            line_height=1.2
        )

        subtitle = MDLabel(
            text="Memberikan rekomendasi gadget terbaik untuk menunjang dunia perkuliahanmu. Mudah, Cepat, dan Menyenangkan",
            font_style="Title",
            role="large",
            font_name=font_poppins,
            theme_text_color="Custom",
            text_color=(0.9, 0.9, 0.9, 1),
            adaptive_height=True,
        )

        content_layout.add_widget(title)
        content_layout.add_widget(subtitle)

        # --- COLLAGE FOTO HERO (DIPERPANJANG KE BAWAH) ---
        collage_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(15),
            size_hint_y=None, 
            height=dp(450),  # <-- DIUBAH: Dari 300 jadi 450 (Lebih panjang ke bawah)
        )

        hero_images = ["hero1.png", "hero2.png", "hero3.png"]

        for img in hero_images:
            card = MDCard(
                radius=[15, 15, 15, 15],
                elevation=2,
                size_hint=(1, 1),
                md_bg_color=[1, 1, 1, 0.2]
            )

            full_path = os.path.join(IMG_DIR, img)
            if os.path.exists(full_path):
                hero_img = FitImage(source=full_path, radius=[15, 15, 15, 15])
                card.add_widget(hero_img)

            collage_box.add_widget(card)

        content_layout.add_widget(collage_box)
        content_layout.add_widget(MDBoxLayout())

        # TOMBOL
        btn_wrapper = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(80))
        btn_wrapper.add_widget(MDBoxLayout())

        btn_next = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=COLOR_WHITE,
            theme_width="Custom",
            height=dp(54),
            size_hint_x=None,
            width=dp(200),
        )
        btn_next.bind(on_release=self.go_to_login)

        btn_icon = MDButtonIcon(
            icon="chevron-double-right",
            theme_icon_color="Custom",
            icon_color=COLOR_PRIMARY,
            pos_hint={'center_y': 0.5}
        )
        btn_text = MDButtonText(
            text="Selanjutnya",
            font_name=font_montserrat,
            bold=True,
            theme_text_color="Custom",
            text_color=COLOR_PRIMARY,
            pos_hint={'center_y': 0.5},
        )

        btn_next.add_widget(btn_icon)
        btn_next.add_widget(btn_text)

        btn_wrapper.add_widget(btn_next)
        content_layout.add_widget(btn_wrapper)

        root_layout.add_widget(content_layout)
        self.add_widget(root_layout)

    def go_to_login(self, instance):
        if self.manager.has_screen("login_screen"):
            self.manager.current = "login_screen"
            self.manager.transition.direction = "left"
        else:
            print("Error: Screen 'login_screen' belum terdaftar!")