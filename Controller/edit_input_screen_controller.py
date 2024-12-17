"""
controller for edit input screen, 
edit extra deck monster levels
"""
from typing import List
from View.EditInputScreen.edit_input_screen_view import EditInputScreenView


class EditInputScreenController:
    """
    The `EditInputScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.edit_input_screen.EditInputScreenModel
        self.view = EditInputScreenView(controller=self, model=self.model)

    def get_view(self) -> EditInputScreenView:
        """generated get view function for MVC"""
        return self.view

    def update_extra_deck(self,fusion_levels: List[int], xyz_ranks:List[int]):
        """update extra deck monster level selection in view"""
        self.view.change_all_levels(fusion_levels,xyz_ranks)
