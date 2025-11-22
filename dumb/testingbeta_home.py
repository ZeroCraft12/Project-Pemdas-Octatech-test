from kivy.properties import StringProperty
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemIcon,
    MDNavigationItemLabel,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
# Import khusus KivyMD 2.0
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.scrollview import MDScrollView

class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clock schedule dihapus untuk simplifikasi di v2.0, 
        # tapi jika tetap dipakai tidak masalah, namun kita isi manual di bawah
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))


class SavingsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        layout = MDBoxLayout(
            orientation="vertical", 
            padding=20, 
            spacing=20, 
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            adaptive_height=True
        )

        # 1. Input Target (Format Baru KivyMD 2.0)
        self.target_input = MDTextField(
            MDTextFieldHintText(text="Harga Laptop Impian (Rp)"),
            mode="outlined",
        )
        # Filter input angka manual nanti di logika, karena input_filter properti berbeda di v2

        # 2. Input Tabungan (Format Baru KivyMD 2.0)
        self.current_savings = MDTextField(
            MDTextFieldHintText(text="Tabungan Saat Ini (Rp)"),
            mode="outlined",
        )

        # 3. Label Hasil
        self.result_label = MDLabel(
            text="Masukkan angka untuk menghitung",
            halign="center",
            theme_text_color="Primary"
        )

        # 4. Tombol Hitung (Format Baru KivyMD 2.0)
        # Perhatikan: MDButtonText ada DI DALAM MDButton
        calc_btn = MDButton(
            MDButtonText(
                text="Hitung Sisa Target",
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            ),
            style="elevated",
            pos_hint={"center_x": 0.5},
            on_release=self.calculate 
        )

        layout.add_widget(self.target_input)
        layout.add_widget(self.current_savings)
        layout.add_widget(calc_btn)
        layout.add_widget(self.result_label)

        self.add_widget(layout)

    def calculate(self, instance):
        try:
            # Mengambil text di KivyMD v2 sama saja
            target = int(self.target_input.text)
            current = int(self.current_savings.text)
            gap = target - current

            if gap <= 0:
                self.result_label.text = "Selamat! Uang Anda sudah cukup!"
                self.result_label.text_color = "green"
            else:
                self.result_label.text = f"Anda butuh Rp {gap:,} lagi."
                self.result_label.text_color = "red"
        except ValueError:
            self.result_label.text = "Mohon masukkan angka yang valid."


class WishlistScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        scroll = MDScrollView()
        list_container = MDList()

        laptops = [
            ("MacBook Air M2", "Rp 18.000.000 - Chip Apple Silicon efisien"),
            ("Asus ROG Zephyrus", "Rp 25.000.000 - Powerhouse untuk Gaming/ML"),
            ("Lenovo Legion 5", "Rp 20.000.000 - Pendinginan mantap"),
            ("Acer Swift X", "Rp 12.000.000 - Ringan untuk Data Analyst"),
        ]

        for name, desc in laptops:
            item = MDListItem(
                MDListItemHeadlineText(text=name),
                MDListItemSupportingText(text=desc),
            )
            list_container.add_widget(item)

        scroll.add_widget(list_container)
        self.add_widget(scroll)


class Example(MDApp):
    def on_switch_tabs(self, bar, item, item_icon, item_text):
        self.root.get_ids().screen_manager.current = item_text

    def build(self):
        return (
            MDBoxLayout(
                MDScreenManager(
                    SavingsScreen(name="Tabungan"),
                    WishlistScreen(name="Wishlist"),
                    id="screen_manager"
                ),
                MDNavigationBar(
                    BaseMDNavigationItem(
                        icon="calculator",
                        text="Tabungan",
                        active=True,
                    ),
                    BaseMDNavigationItem(
                        icon="laptop",
                        text="Wishlist",
                    ),
                    on_switch_tabs=lambda *args: self.on_switch_tabs(*args)
                ),
                orientation="vertical",
                md_bg_color=self.theme_cls.backgroundColor,
            )
        )

Example().run()