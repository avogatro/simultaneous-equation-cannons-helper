"""
controller for main screen
"""
from typing import List
from Controller.base_controller import BaseController
from View.AppMainScreen.app_main_screen_view import AppMainScreenView

from Model.simultaneous_equation_cannons_state import CompareMode, SimultaneousEquationCannonsState
from Model.config_reader import InputConfiguration, read_config, write_config


class AppMainScreenController(BaseController):
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

    def load_simultaneous_equation_cannons_state(self):
        """
        load data/model
        """
        self._config = None

        try:
            self._config = read_config()
            if self._config is not None:
                self._sec_state = SimultaneousEquationCannonsState(self._config.fusion_levels, self._config.xyz_ranks)
        except FileNotFoundError as e:
            print(f"config parser error:\n {e}")
            self.save_simultaneous_equation_cannons_state()

    def save_simultaneous_equation_cannons_state(self):
        """
        save data/model
        """
        input_config = InputConfiguration()
        input_config.xyz_ranks = self._sec_state.xyz_ranks
        input_config.fusion_levels = self._sec_state.fusion_levels
        write_config(input_config)
        self._config = input_config

    def get_simultaneous_equation_cannons_output(self):
        """
        get dict of monster level as key and the allowed total cards in both players hand and on both players board
        """
        return self._sec_state.value_table

    def get_simultaneous_equation_cannons_config(self):
        """
        get config
        """
        self._config.banished_fusion_levels = self._sec_state.banished_fusion_levels
        self._config.banished_xyz_ranks = self._sec_state.banished_xyz_ranks
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
        self._sec_state.set_extra_deck_monster_level(new_fusion_levels, new_xyz_ranks)
        self.save_simultaneous_equation_cannons_state()
        self.update_view()

    def set_banish_zone_monster_level(self, new_fusion_levels: List[int], new_xyz_ranks: List[int]):
        "add banished xyz fusion monster to the calculation and update view"
        self._sec_state.set_banish_zone_monster_level(new_fusion_levels, new_xyz_ranks, CompareMode.EXCLUDE)
        self.update_view()

    def reset_banish_zone_monster_level(self):
        """remove all banished xyz fusion monsters and update view"""
        self._sec_state.reset_banish_zone_monster_level()
        self.update_view()
