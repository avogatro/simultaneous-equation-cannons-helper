"""
controller for edit input screen, 
edit extra deck monster levels
"""
from typing import List
from Controller.base_controller import BaseController
from View.EditInputScreen.edit_input_screen_view import EditInputScreenView, InputMode


class EditInputScreenController(BaseController):
    """
    The `EditInputScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.edit_input_screen.EditInputScreenModel
        self.view = EditInputScreenView(controller=self, model=self.model)

    def update_extra_deck_monsters(self, fusion_levels: List[int], xyz_ranks:List[int], input_mode:InputMode):
        """update extra deck monster level selection in view"""
        self.view.update_extra_deck_monsters(fusion_levels, xyz_ranks, input_mode)
