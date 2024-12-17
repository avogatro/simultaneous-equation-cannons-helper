"""
Binder of all model view controller

The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""
import os
import sys

from kivy.resources import resource_add_path, resource_find
from kivy import Config
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from PIL import ImageGrab

# crucial hidden import for pyinstaller
# pylint: disable=W0611
import kivymd.icon_definitions

from Controller.base_controller import BaseController
from View.EditInputScreen.edit_input_screen_view import InputMode
from View.screens import screens, NAME_APP_MAIN_SCREEN, NAME_EDIT_EXTRA_DECK_SCREEN
from View.screens import NAME_EDIT_BANISHED_ZONE_SCREEN, NAME_TUTORIAL_SCREEN


resolution = ImageGrab.grab().size

# Change the values of the application window size as you need
Config.set("graphics", "height", "800")
Config.set("graphics", "width", "700")
Config.set('kivy','window_icon','icon_p1.ico')

# Place the application window on the right side of the computer screen

Window.top = 5
Window.left = resolution[0] - Window.width
Window.icon = "icon_p1.ico"
Window.size = (700, 800)
KV = '''

<BaseMDNavigationItem@MDNavigationItem>
    text: ""
    icon: ""
    MDNavigationItemIcon:
        icon: root.icon
    MDNavigationItemLabel:
        text: root.text
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationBar:
        on_switch_tabs: app.on_switch_tabs(*args)
        BaseMDNavigationItem
            icon: "calculator-variant-outline"
            text: "Main"
            active: True

        BaseMDNavigationItem
            icon: "selection"
            text: "Extra Deck"
            
        BaseMDNavigationItem
            icon: "selection-remove"
            text: "Banished Zone"
            
        BaseMDNavigationItem
            icon: "help"
            text: "Tutorial"
'''


class SimultaneousEquationCannonsHelper(MDApp):
    """
    main app
    generate UI and bind model view controller
    """
    controllers: dict[BaseController]
    screen_name_dict = {'Main': NAME_APP_MAIN_SCREEN, 'Extra Deck': NAME_EDIT_EXTRA_DECK_SCREEN,
                        'Banished Zone': NAME_EDIT_BANISHED_ZONE_SCREEN, 'Tutorial': NAME_TUTORIAL_SCREEN}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.manager_screens = MDScreenManager(id="screen_manager")
        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "Orange"
        self.theme_cls.dynamic_color = True
        self.controllers = {}
        self.icon = resource_find("assets/icons/icon.png")
        self.title = 'Simultaneous Equation Cannons Helper'

    def build(self) -> MDScreenManager:
        self.generate_application_screens()
        self.manager_screens.current = NAME_APP_MAIN_SCREEN
        self.root = Builder.load_string(KV)
        self.root.add_widget(self.manager_screens)
        return self.root

    def generate_application_screens(self) -> None:
        """
        binder function

        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """

        for name_screen, screen_mvc_group in screens.items():
            model = screen_mvc_group["model"]()
            controller = screen_mvc_group["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)
            self.controllers[name_screen] = controller

    def on_switch_tabs(
        # pylint: disable=W0613
        self, nav_bar: MDNavigationBar, nav_item: MDNavigationItem, nav_item_icon: str, item_text: str):
        """
        navigationbar: on_switch_tabs save stats of current tab, prepare new tab view
        """
        if self.screen_name_dict[item_text] == self.manager_screens.current:
            return
        # save stats
        if self.manager_screens.current == NAME_EDIT_BANISHED_ZONE_SCREEN:
            view = self.controllers[NAME_EDIT_BANISHED_ZONE_SCREEN].get_view()
            self.controllers[NAME_APP_MAIN_SCREEN].set_banish_zone_monster_level(
                    view.fusion_levels, view.xyz_ranks)
        elif self.manager_screens.current == NAME_EDIT_EXTRA_DECK_SCREEN:
            view = self.controllers[NAME_EDIT_EXTRA_DECK_SCREEN].get_view()
            self.controllers[NAME_APP_MAIN_SCREEN].set_extra_deck_monster_level(
                    view.fusion_levels, view.xyz_ranks)
        # prepare next view
        config = self.controllers[NAME_APP_MAIN_SCREEN].get_simultaneous_equation_cannons_config()
        if self.screen_name_dict[item_text] == NAME_EDIT_EXTRA_DECK_SCREEN:
            self.controllers[NAME_EDIT_EXTRA_DECK_SCREEN].update_extra_deck_monsters(
                    config.fusion_levels, config.xyz_ranks, InputMode.EXTRA_DECK)

        elif self.screen_name_dict[item_text] == NAME_EDIT_BANISHED_ZONE_SCREEN:
            self.controllers[NAME_EDIT_BANISHED_ZONE_SCREEN].update_extra_deck_monsters(
                    config.banished_fusion_levels, config.banished_xyz_ranks, InputMode.BANISHED_ZONE)

        self.manager_screens.current = self.screen_name_dict[item_text]


if __name__ == '__main__':
    # for pyinstaller
    if hasattr(sys, '_MEIPASS'):
        # pylint: disable=W0212
        resource_add_path(os.path.join(sys._MEIPASS))
    SimultaneousEquationCannonsHelper().run()
