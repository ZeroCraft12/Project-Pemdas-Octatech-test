from kivy.lang import Builder
from kivymd.app import MDApp

# Perubahan dilakukan pada baris 14 dan 20: 
# primary_color -> primaryColor
# accent_color -> accentColor

KV = '''
MDScreen:

    # MDNavigationRail diletakkan di sisi kiri layar (default)
    MDNavigationRail:
        id: navigation_rail
        anchor_point: "center"
        padding: "12dp", "12dp", "12dp", "12dp"
        
        # BARIS INI DIPERBAIKI: primary_color -> primaryColor
        md_bg_color: self.theme_cls.primaryColor 
        
        text_color: 0.9, 0.9, 0.9, 1
        
        # BARIS INI DIPERBAIKI: accent_color -> accentColor
        selected_color: self.theme_cls.accentColor 

        MDNavigationRailItem:
            text: "Beranda"
            icon: "home"
            on_release: app.on_nav_rail_item_click(self.text)
            
        MDNavigationRailItem:
            text: "Pesan"
            icon: "message-processing"
            on_release: app.on_nav_rail_item_click(self.text)

        MDNavigationRailItem:
            text: "Pengaturan"
            icon: "cog"
            on_release: app.on_nav_rail_item_click(self.text)
'''

class NavigationRailApp(MDApp):
    def on_nav_rail_item_click(self, item_text):
        print(f"Item terpilih: {item_text}")
        
    def build(self):
        # Perhatikan: Pada kode Python, penamaan properti tema biasanya menggunakan snake_case 
        # (seperti yang sudah benar di sini).
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue" 
        
        return Builder.load_string(KV)

if __name__ == '__main__':
    NavigationRailApp().run()