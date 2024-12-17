"""
view class for 
editing extra deck monster level
"""
from enum import Enum, unique
from typing import List

import kivy.properties as KivyProps
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText

from Model.simultaneous_equation_cannons_state import MonsterKind
from View.base_screen import BaseScreenView


@unique
class InputMode(Enum):
    """
    choose input mode for edit input screen
    """
    EXTRA_DECK = 0  # choose xyz fusion lvl/rank from extra deck
    BANISHED_ZONE = 1  # choose xyz fusion lvl/rank in banished zone, for more equation options at 2nd/3rd SEC


class CardSelectionButton(MDButton):
    """
    MDButton for updating extra deck level selections
    """
    kind: MonsterKind
    level: int
    selected = KivyProps.BooleanProperty(False)

    def set_style(self):
        """
        change style for selected and not selected states, like check box
        """
        if self.selected:
            self._button_icon.icon = "minus"
            self.style = "outlined"
        else:
            self._button_icon.icon = "plus"
            self.style = "text"

    def on_release(self, *args):
        if  self.parent.parent.parent.input_mode == InputMode.EXTRA_DECK and not self.selected and \
                not self.parent.parent.parent.check_total_extra_deck_size(self.kind, self.level):
            prefix = "Extra Deck Size "
            self.parent.parent.parent.ids['"label_extra_deck_count"'].text = f"{prefix} can't be > 15"

        else:
            self.selected = not self.selected
            self.set_style()
            self.parent.parent.parent.change_level(self.kind, self.level, self.selected)


class EditInputScreenView(BaseScreenView):
    """
    view class for edit input screen
    """
    total_cards = 0
    fusion_levels: List[int] = []
    xyz_ranks: List[int] = []
    all_buttons: List[CardSelectionButton]

    input_mode = InputMode.EXTRA_DECK

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def check_total_extra_deck_size(self, monster_kind: MonsterKind, level: int):
        """
        check if total extra deck size will exceed 15
        """
        total = len(self.fusion_levels) + 2 * len(self.xyz_ranks)
        if monster_kind == MonsterKind.FUSION and level not in self.fusion_levels:
            return total <= 14
        if monster_kind == MonsterKind.XYZ and level not in self.xyz_ranks:
            return total <= 13

    def change_level(self, monster_kind: MonsterKind, level: int, selected: KivyProps.BooleanProperty):
        """
        update extra deck monster level locally for this view
        """
        if selected:
            if not self.check_total_extra_deck_size(monster_kind, level):
                return
            if monster_kind == MonsterKind.FUSION:
                self.fusion_levels.append(level)
            else:
                self.xyz_ranks.append(level)
        else:
            if monster_kind == MonsterKind.FUSION:
                self.fusion_levels.remove(level)
            else:
                self.xyz_ranks.remove(level)

        self.update_extra_deck_size()

    def update_extra_deck_size(self):
        """update label indicate extra deck size"""
        prefix = ""
        if self.input_mode == InputMode.EXTRA_DECK:
            prefix = "Extra Deck Size: "
            total = len(self.fusion_levels) + 2 * len(self.xyz_ranks)
            self.ids['"label_extra_deck_count"'].text = f"{prefix}{total}"
        else:
            prefix = "Banished Monsters"
            self.ids['"label_extra_deck_count"'].text = f"{prefix}"

    def update_extra_deck_monsters(self, fusion_levels: List[int], xyz_ranks: List[int],
                                   input_mode=InputMode.EXTRA_DECK):
        """
        update selection from controller
        """
        self.fusion_levels = fusion_levels
        self.xyz_ranks = xyz_ranks
        self.input_mode = input_mode
        for button in self.all_buttons:
            if button.kind == MonsterKind.FUSION:
                button.selected = button.level in fusion_levels
                button.set_style()
            else:
                button.selected = button.level in xyz_ranks
                button.set_style()
        self.update_extra_deck_size()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_buttons = list[CardSelectionButton]()
        self._generate_xyz_selections()
        self._generate_fusion_selections()

    def _generate_xyz_selections(self):
        for i in range(12):
            button = CardSelectionButton(
                MDButtonIcon(id=f"icon_xyz_{i+1}", icon="plus"),
                MDButtonText(id=f"text_xyz_{i+1}", text=f"Rank {i+1}", pos_hint= {"center_x": .5, "center_y": .5}),
                id=f"xyz_{i+1}",
            )
            button.level = i + 1
            button.kind = MonsterKind.XYZ
            self.ids["\"xyz_grid\""].add_widget(button)
            self.all_buttons.append(button)

    def _generate_fusion_selections(self):
        for i in range(12):
            button = CardSelectionButton(
                MDButtonIcon(id=f"icon_fusion_{i+1}", icon="plus"),
                MDButtonText(id=f"text_fusion_{i+1}", text=f"Level {i+1}", pos_hint= {"center_x": .5, "center_y": .5}),
                id=f"fusion_{i+1}",
            )
            button.level = i + 1
            button.kind = MonsterKind.FUSION
            self.ids["\"fusion_grid\""].add_widget(button)
            self.all_buttons.append(button)
