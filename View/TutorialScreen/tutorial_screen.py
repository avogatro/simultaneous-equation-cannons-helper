"""
view for tutorial screen
"""
import webbrowser
from View.base_screen import BaseScreenView
class TutorialScreenView(BaseScreenView):
    """
    view for tutorial screen
    """
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
    def open_browser(self):
        """
        open webbrowser
        """
        webbrowser.open("https://www.youtube.com/watch?v=GODdZ4Vz-WM")
        