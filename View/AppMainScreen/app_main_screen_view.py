"""
main screen view
"""

import kivy.properties as KivyProps
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText

from View.EditInputScreen.edit_input_screen_view import InputMode
from View.base_screen import BaseScreenView

from Model.simultaneous_equation_cannons_state import SimultaneousEquationCannonsSolution


class CardNumberSelectionButton(MDButton):
    """
    button for displaying each value of (monster level and total cards) 
    for data from Simultaneous Equation Cannons value_table
    """
    monster_level: int = 0
    total_cards: int = 0
    selected = KivyProps.BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.style = "text"
        #self.md_textfield = (2, 2, 2, 2)
        # self.md_bg_color="#303A29"
        self.radius = 5
        self.width = 140
        self.theme_width = "Custom"
        #self.size_hint_y = None
        self.padding= "1dp"
        self.spacing= "1dp"
    def on_press(self, *args):
        self.selected = not self.selected
        if self.selected:
            self.style = "outlined"

        self.parent.parent.parent.parent.parent.find_solution(self.monster_level, self.total_cards)


class AppMainScreenView(BaseScreenView):
    """
    main screen view
    """
    to_remove = []

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
                    widget.style = "text"

        self.controller.find_solution(monster_level, total_cards)

    def _remove_old_widgets(self):
        for w in self.to_remove:
            self.ids.boxed_content.remove_widget(w)
        self.to_remove = []

    def update_view_after_sec_update(self, value_table):
        """
        dynamically create UI to display values from model
        can be used by controller or in constructor
        """
        self._remove_old_widgets()
        max_col = 0
        keys = sorted(value_table.keys())

        for level in keys:
            max_col = max(max_col, len(value_table[level]))
        for level in keys:
            # create a section
            grid_layout = MDGridLayout(
                # pos_hint={"center_x": .5, "top": .88},
                cols=max_col,
                # adaptive_size =  True,
                # adaptive_height= True,
                # size_hint_y=  0.05,
                #size_hint_x=1,
                spacing="2dp",
                padding="2dp",
            )
            for total_cards in value_table[level]:
                card_number_button = CardNumberSelectionButton(
                    MDButtonText(text=f"Lvl {level} Total {total_cards}", pos_hint={"left": 0,"center_y": .5}),
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
        app = MDApp.get_running_app()
        config = self.controller.get_simultaneous_equation_cannons_config()
        app.edit_input_screen_controller.update_extra_deck(config.fusion_levels, config.xyz_ranks, input_mode)
        app.root.current = "edit_input_screen"
