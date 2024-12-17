
from View.TutorialScreen.tutorial_screen import TutorialScreenView


class TutorialScreenController:
    """
    The `TutorialScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.tutorial_screen.TutorialScreenModel
        self.view = TutorialScreenView(controller=self, model=self.model)

    def get_view(self) -> TutorialScreenView:
        return self.view