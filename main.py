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

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy import Config
from kivy.core.window import Window
from PIL import ImageGrab

from View.screens import screens

resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", "800")
Config.set("graphics", "width", "1280")


# Place the application window on the right side of the computer screen.
Window.top = 5
Window.left = resolution[0] - Window.width


class SimultaneousEquationCannonsHelper(MDApp):
    """
    main app
    generate UI and bind model view controller
    """
    main_controller = None
    edit_input_screen_controller = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.manager_screens = MDScreenManager(id="screen_manager")
        self.theme_cls.theme_style = "Dark"

    def build(self) -> MDScreenManager:
        self.generate_application_screens()
        self.manager_screens.current = "app_main_screen"

        Window.size = (800, 1280)

        return self.manager_screens

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
            if name_screen == "app_main_screen":
                self.main_controller = controller
            elif name_screen == "edit_input_screen":
                self.edit_input_screen_controller = controller


SimultaneousEquationCannonsHelper().run()
