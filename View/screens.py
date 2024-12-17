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

from View.constants import NAME_APP_MAIN_SCREEN, NAME_EDIT_EXTRA_DECK_SCREEN, \
    NAME_EDIT_BANISHED_ZONE_SCREEN, NAME_TUTORIAL_SCREEN

screens = {
    NAME_APP_MAIN_SCREEN: {
        "model": AppMainScreenModel,
        "controller": AppMainScreenController,
    },

    NAME_EDIT_EXTRA_DECK_SCREEN: {
        "model": EditInputScreenModel,
        "controller": EditInputScreenController,
    },

    NAME_EDIT_BANISHED_ZONE_SCREEN: {
        "model": EditInputScreenModel,
        "controller": EditInputScreenController,
    },
    NAME_TUTORIAL_SCREEN: {
        "model": TutorialScreenModel,
        "controller": TutorialScreenController,
    },
}
