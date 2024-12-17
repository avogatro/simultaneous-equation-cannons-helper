"""
controller for main screen
"""
from configparser import Error
from typing import List
from View.AppMainScreen.app_main_screen_view import AppMainScreenView

from Model.simultaneous_equation_cannons_state import SimultaneousEquationCannonsState
from Model.config_reader import InputConfiguration, read_config, write_config


class AppMainScreenController:
    """
    The `AppMainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    # technically this is our only data model
    _sec_state = SimultaneousEquationCannonsState([2, 3, 4, 5, 6], [2, 3, 4, 5, 6])
    _config: InputConfiguration = None
    def __init__(self, model):
        self.model = model  # Model.app_main_screen.AppMainScreenModel
        self.view = AppMainScreenView(controller=self, model=self.model)
        self.load_simultaneous_equation_cannons_state()
        self.update_view()

    def get_view(self) -> AppMainScreenView:
        """
        generated MVC code: controller creates view
        """
        return self.view

    def load_simultaneous_equation_cannons_state(self):
        """
        load data/model
        """
        self._config = None

        try:
            self._config = read_config()
        except Error as e:
            print(f"config parser error:\n {e}")

        if self._config is not None:
            self._sec_state = SimultaneousEquationCannonsState(fusion_levels=sorted(self._config.fusion_levels),
                                                          xyz_ranks=sorted(self._config.xyz_ranks))

    def save_simultaneous_equation_cannons_state(self):
        """
        save data/model
        """
        input_config = InputConfiguration()
        input_config.xyz_ranks = self._sec_state.xyz_ranks
        input_config.fusion_levels = self._sec_state.fusion_levels
        write_config(input_config)

    def get_simultaneous_equation_cannons_output(self):
        """
        get dict of monster level as key and the allowed total cards in both players hand and on both players board
        """
        return self._sec_state.value_table

    def get_simultaneous_equation_cannons_config(self):
        """
        get config
        """
        return self._config

    def find_solution(self, monster_level: int, total_cards: int):
        """
        find solution for said input, and show what level/rank to choose
        """
        solution = self._sec_state.find_solution(monster_level, total_cards)
        self.view.update_view_with_sec_solution(solution)

    def update_view(self):
        """
        after model change, change view
        """
        self.view.update_view_after_sec_update(self._sec_state.value_table)

    def set_extra_deck_monster_level(self, new_fusion_levels: List[int], new_xyz_ranks: List[int]):
        """
        change model save model and update view
        """
        self._sec_state.set_extra_deck_monster_level(sorted(new_fusion_levels), sorted(new_xyz_ranks))
        self.save_simultaneous_equation_cannons_state()
        self.update_view()
