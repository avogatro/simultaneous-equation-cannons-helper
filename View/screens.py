""" 
The screens dictionary contains the objects of the models and controllers
of the screens of the application.
"""


from Model.app_main_screen import AppMainScreenModel
from Model.edit_input_screen import EditInputScreenModel
from Model.tutorial_screen import TutorialScreenModel
from Controller.app_main_screen_controller import AppMainScreenController
from Controller.edit_input_screen_controller import EditInputScreenController
from Controller.tutorial_screen_controller import TutorialScreenController

screens = {
    "app_main_screen": {
        "model": AppMainScreenModel,
        "controller": AppMainScreenController,
    },

    "edit_input_screen": {
        "model": EditInputScreenModel,
        "controller": EditInputScreenController,
    },

    "tutorial_screen": {
        "model": TutorialScreenModel,
        "controller": TutorialScreenController,
    },
}
