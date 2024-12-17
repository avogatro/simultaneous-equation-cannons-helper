"""
This is helper class for the card "Simultaneous Equation Cannons" in the Game YoGiOh

Card text:

Banish 1 Fusion Monster and 2 Xyz Monsters with the same Rank from your Extra Deck,
whose combined Level and Ranks equal the total number of cards in both players' hands
and on the field, then you can apply this effect.

- Return 2 of your banished monsters to the Extra Deck (1 Xyz and 1 Fusion) whose
combined Level and Rank equal the Level or Rank of 1 face-up monster your opponent controls, 
then banish all cards they control.

Card Explanation:

I want to activate the 2nd effect, banish all cards my opponent controls.
Imagine there are in total 14 cards in both players hands and on the board, and your opponent has 1 level 8 monster.

To activate my card, I need to banish 2 XYZ Monster with Rank R and 1 fusion monsters Level L.

Equation 1: Rank R + Rank R + Level L = 14
Equation 2: Rank R + Level L = 8

Solution:
Equation 3 is Equation 1 - Equation 2: R = 14-8 = 6

Equation 4 is Equation 2 - Equation 3: L = 8-6 = 2

The XYZ Rank you send is "Total card number in hands and on board" - "the matching monster level".
The Fusion Level you send is "the matching Monster level" - the difference of above.

"""
from typing import List
from dataclasses import dataclass
from enum import Enum


class CardOperation(Enum):
    """add or remove monster level"""
    PLUS = 0
    MINUS = 1


class MonsterKind(Enum):
    """we only care about fusion and xyz for SimultaneousEquationCannons"""
    FUSION = 0
    XYZ = 1


@dataclass
class SimultaneousEquationCannonsSolution:
    """Class for keeping track of SimultaneousEquationCannonsSolution"""
    solution_exist: bool = False
    monster_level: int = 0
    total_cards: int = 0
    xyz_rank: int = 0
    fusion_level: int = 0


class SimultaneousEquationCannonsState():
    """Class for organizing State of SimultaneousEquationCannons Helper"""
    _fusion_levels = [2, 3, 4, 5, 6]
    _xyz_ranks = [2, 3, 4, 6, 5]
    _value_table = dict()

    def __init__(self, fusion_levels: List[int], xyz_ranks: List[int]):
        self.set_extra_deck_monster_level(fusion_levels, xyz_ranks)

    def _generate_value_table(self):
        self._value_table = dict()
        for l in self._fusion_levels:
            for r in self._xyz_ranks:
                if l + r in self._value_table:
                    self._value_table[l + r] = sorted(set(self._value_table[l + r] + [l + r + r]))
                else:
                    self._value_table[l + r] = [l + r + r]

    def set_extra_deck_monster_level(self, new_fusion_levels: List[int], new_xyz_ranks: List[int]):
        """set extra deck input and prepare value table"""
        extra_deck_size = len(new_fusion_levels) + len(new_xyz_ranks) * 2
        if extra_deck_size < 0 or extra_deck_size > 15:
            raise ValueError(f"extra_deck_size out of range: {extra_deck_size}")

        for level in new_fusion_levels:
            if level < 1 or level > 12:
                raise ValueError(f"fusion level out of range {level}")
        self._fusion_levels = new_fusion_levels

        for rank in new_xyz_ranks:
            if rank < 0 or rank > 13:
                raise ValueError(f"xyz level out of range {rank}")
        self._xyz_ranks = new_xyz_ranks
        self._generate_value_table()

    @property
    def fusion_levels(self):
        """fusion monster levels in extra deck"""
        return self._fusion_levels

    @property
    def xyz_ranks(self):
        """xyz monster ranks in extra deck"""
        return self._xyz_ranks

    @property
    def value_table(self):
        """show what total card number and matching monster level are needed for the banash effect to resolve"""
        return self._value_table

    def print_value_table(self):
        """debug output print value_table """
        print(f"fusion_level\t{self._fusion_levels}")
        print(f"xyz_rank\t{self._xyz_ranks}")
        for k in sorted(self._value_table.keys()):
            print(f"Monster Lvl/Rank to Match: {k} \t Possible Total Cards: {self._value_table[k]}")

    def find_solution(self, monster_level: int, total_cards: int):
        """find out if the banish effect can be activated"""
        res = SimultaneousEquationCannonsSolution(solution_exist=False,
                                              monster_level=monster_level,
                                              total_cards=total_cards)
        if monster_level not in self._value_table:
            return res

        if total_cards not in self._value_table[monster_level]:
            return res

        res.solution_exist = True
        res.xyz_rank = total_cards - monster_level
        res.fusion_level = monster_level - res.xyz_rank
        return res

    def change_monster(self, level: int, monster_kind: MonsterKind, card_operation: CardOperation):
        """change a single monster in extra deck"""
        temp_fusion_level = self._fusion_levels
        temp_xyz_rank = self._xyz_ranks
        try:
            if card_operation == CardOperation.MINUS:
                if monster_kind == MonsterKind.FUSION:
                    temp_fusion_level.remove(level)
                else:
                    temp_xyz_rank.remove(level)

            if card_operation == CardOperation.PLUS:
                if monster_kind == MonsterKind.FUSION:
                    temp_fusion_level.append(level)
                else:
                    temp_xyz_rank.append(level)
        except ValueError as e:
            print(e)
            return
        self.set_extra_deck_monster_level(temp_fusion_level, temp_xyz_rank)


