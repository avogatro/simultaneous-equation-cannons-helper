"""
main screen view
"""

from kivy.graphics import Color, PopMatrix, PushMatrix, Scale
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import BackgroundColorBehavior, DeclarativeBehavior

from View.EditInputScreen.edit_input_screen_view import InputMode
from View.base_screen import BaseScreenView

from Model.simultaneous_equation_cannons_state import SimultaneousEquationCannonsSolution
from Model.hct_color_finder import HctColorFinder
class CardNumberSelectionButton(MDCard):
    """
    button for displaying each value of (monster level and total cards) 
    for data from Simultaneous Equation Cannons value_table
    """
    monster_level: int = 0
    total_cards: int = 0

    def on_press(self, *args):
        self.style = "outlined"
        self.parent.parent.parent.parent.parent.find_solution(self.monster_level, self.total_cards)


class CustomScrollView(DeclarativeBehavior, BackgroundColorBehavior, ScrollView):
    """
    enable both x and y axis scrolling, by recreate MDScrollView but with no MD animation
    compare with MDScrollView to see more
    """
    _internal_scale = None

    def __init__(self, *args, **kwargs):
        #self.effect_cls = StretchOverScrollStencil
        super().__init__(*args, **kwargs)
        with self.canvas.before:
            Color(rgba=self.md_bg_color)
            PushMatrix()
            self._internal_scale = Scale()
        with self.canvas.after:
            PopMatrix()
        self.effect_y.scale_axis = "y"
        self.effect_x.scale_axis = "x"

    def on_touch_down(self, touch):
        self.effect_x.last_touch_pos = touch.pos
        self.effect_y.last_touch_pos = touch.pos
        super().on_touch_down(touch)

class CustomGridLayout(MDGridLayout):
    """placeholder class to seperate styling from code """

class AppMainScreenView(BaseScreenView):
    """
    main screen view
    """
    to_remove = []
    hct_color_finder = HctColorFinder(80)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def update_view_with_sec_solution(self, solution: SimultaneousEquationCannonsSolution):
        """
        called by controller to update view after search for sec solution
        """
        if not solution.solution_exist:
            self.ids[['"label_solution"']].text = "No Solution found"
        else:
            self.ids['"label_solution"'].text = f"Xyz Rank: {solution.xyz_rank} Fusion lvl: {solution.fusion_level }"

    def find_solution(self, monster_level: int, total_cards: int):
        """
        called by UI to trigger controller to find solution by using model SEC
        and update ui
        """
        for widget in self.to_remove:
            if isinstance(widget, CardNumberSelectionButton):
                if widget.total_cards != total_cards or widget.monster_level != monster_level:
                    widget.style = "filled"
                    widget.selected = False
                else:
                    widget.style = "outlined"
                    widget.selected = True
        self.controller.find_solution(monster_level, total_cards)

    def _remove_old_widgets(self):
        for w in self.to_remove:
            self.ids.boxed_content.remove_widget(w)
        self.to_remove = []

    def _find_range(self, value_table):
        keys = sorted(value_table.keys())
        min_total = 1000
        max_total = 0
        for level in keys:
            for total_cards in value_table[level]:
                min_total = min(total_cards,min_total)
                max_total = max(total_cards,max_total)
        steps = max_total - min_total + 1
        colors = self.hct_color_finder.find_colors(steps)
        res= {}
        for step in range(steps):
            res[min_total+step] = colors[step]
        return res

    def update_view_after_sec_update(self, value_table):
        """
        dynamically create UI to display values from model
        can be used by controller or in constructor
        """
        self._remove_old_widgets()
        max_col = 0
        keys = sorted(value_table.keys())
        heatmap_colors = self._find_range(value_table)
        for level in keys:
            max_col = max(max_col, len(value_table[level]))

        for level in keys:
            # create a section
            grid_layout = CustomGridLayout(cols=max_col)
            for total_cards in value_table[level]:
                color_hex = heatmap_colors[total_cards]
                card_number_button = CardNumberSelectionButton(
                    MDLabel(text=f"Lvl {level}: Total {total_cards}",
                            halign = "center",
                            theme_text_color= "Custom",
                            text_color= color_hex
                        ),
                    id=f"card_number_button_{level}_{total_cards}",
                )
                card_number_button.monster_level = level
                card_number_button.total_cards = total_cards
                grid_layout.add_widget(card_number_button)
                self.to_remove.append(card_number_button)
                # section add buttons with action to call solution
            self.ids.boxed_content.add_widget(grid_layout)
            self.to_remove.append(grid_layout)
        if len(self.to_remove) > 1:
            self.to_remove[0].on_press(None)

    def update_and_go_edit_screen(self, input_mode = InputMode.EXTRA_DECK):
        """
        update edit input screen controller
        and change screen
        """
        config = self.controller.get_simultaneous_equation_cannons_config()
        self.app.edit_input_screen_controller.update_extra_deck(config.fusion_levels, config.xyz_ranks, input_mode)
        self.app.root.current = "edit_input_screen"
