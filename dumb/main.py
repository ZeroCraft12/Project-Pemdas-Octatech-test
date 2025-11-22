from kivy.properties import StringProperty
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemIcon,
    MDNavigationItemLabel,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.builds)

    def builds(self, *args):
        self.add_widget(
            MDNavigationItemIcon(
                icon=self.icon
            )
        )
        self.add_widget(
            MDNavigationItemLabel(
                text=self.text
            )
        )


class BaseScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.builds)

    def builds(self, *args):
        self.add_widget(
            MDLabel(
                text=self.name,
                halign="center",
            )
        )


class Example(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.get_ids().screen_manager.current = item_text

    def build(self):
        return (
            MDBoxLayout(
                MDScreenManager(
                    BaseScreen(
                        name="Screen 1"
                    ),
                    BaseScreen(
                        name="Screen 2"
                    ),
                    id="screen_manager"
                ),
                MDNavigationBar(
                    BaseMDNavigationItem(
                        icon="gmail",
                        text="Screen 1",
                        active=True,
                    ),
                    BaseMDNavigationItem(
                        icon="twitter",
                        text="Screen 2",
                    ),
                    on_switch_tabs=lambda *args: self.on_switch_tabs(*args)
                ),
                orientation="vertical",
                md_bg_color=self.theme_cls.backgroundColor,
            )
        )


Example().run()