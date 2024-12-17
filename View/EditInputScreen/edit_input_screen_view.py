"""
view class for 
editing extra deck monster level
"""
from typing import List
import kivy.properties as KivyProps
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.app import MDApp

from View.base_screen import BaseScreenView

from Model.simultaneous_equation_cannons_state import MonsterKind


class CardSelectionButton(MDButton):
    """
    MDButton for updating extra deck level selections
    """
    kind: MonsterKind
    level: int
    selected = KivyProps.BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.style = "text"
        # self.md_bg_color="#303A29"
        self.radius = 5
        self.width = 150
        self.theme_width = "Custom"

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

        if not self.selected and not self.parent.parent.parent.check_total_extra_deck_size(self.kind, self.level):
            self.parent.parent.parent.ids['"label_extra_deck_count"'].text = "Extra Deck Size Can't be > 15"
        else:
            self.selected = not self.selected
            self.set_style()
            self.parent.parent.parent.change_level(self.kind, self.level, self.selected)


class EditInputScreenView(BaseScreenView):
    """
    view class for edit input screen
    """
    total_cards = 0

    fusion_levels: List[int]
    xyz_ranks: List[int]
    all_buttons: List[CardSelectionButton] = list[CardSelectionButton]()

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
        total = len(self.fusion_levels) + 2 * len(self.xyz_ranks)
        self.ids['"label_extra_deck_count"'].text = f"Extra Deck Size {total}"

    def change_all_levels(self, fusion_levels: List[int], xyz_ranks: List[int]):
        """
        update selection from controller
        """
        self.fusion_levels = fusion_levels
        self.xyz_ranks = xyz_ranks

        for button in self.all_buttons:
            if button.kind == MonsterKind.FUSION:
                if button.level in self.fusion_levels:
                    button.selected = True
                    button.set_style()
            else:
                if button.level in self.xyz_ranks:
                    button.selected = True
                    button.set_style()
        self.update_extra_deck_size()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generate_xyz_selections()
        self._generate_fusion_selections()

    def _generate_xyz_selections(self):
        for i in range(12):
            button = CardSelectionButton(
                MDButtonIcon(id=f"icon_xyz_{i+1}", icon="plus"),
                MDButtonText(id=f"text_xyz_{i+1}", text=f"Rank {i+1}"),
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
                MDButtonText(id=f"text_fusion_{i+1}", text=f"Level {i+1}"),
                id=f"fusion_{i+1}",
            )
            button.level = i + 1
            button.kind = MonsterKind.FUSION
            self.ids["\"fusion_grid\""].add_widget(button)
            self.all_buttons.append(button)

    def save_model_and_go_back(self):
        """
        trigger controller function to update model, model trigger controller to update view
        """

        app = MDApp.get_running_app()
        app.main_controller.set_extra_deck_monster_level(self.fusion_levels, self.xyz_ranks)
        app.root.current = "app_main_screen"
