"""
declare BaseController class for classification
"""
from View.base_screen import BaseScreenView

class BaseController:
    """
    class for classification
    """
    view: BaseScreenView
    def get_view(self) -> BaseScreenView:
        """
        controller return view
        """
        return self.view
