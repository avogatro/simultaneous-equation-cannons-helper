"""
unittest for simultaneous_equation_cannons_state

test with "python -m unittest .\tests\test_<test_name>.py"

"""
import unittest

from Model.simultaneous_equation_cannons_state import SimultaneousEquationCannonsState, CompareMode


class SecTestCaseEmpty(unittest.TestCase):
    """test empty state"""

    def setUp(self):
        self.sec = SimultaneousEquationCannonsState([], [])

    def test_empty(self):
        """test empty state"""
        res = self.sec.value_table
        self.assertEqual(len(res), 0)


class SecTestCase00(unittest.TestCase):
    """test fusion 1 2, xyz 1 2"""

    def test_2x2(self):
        """normal case no ban"""
        sec = SimultaneousEquationCannonsState([1, 2], [1, 2])
        res = sec.value_table
        self.assertEqual(len(res.keys()), 3)
        self.assertEqual(res[2], [3])
        self.assertEqual(res[3], [4, 5])
        self.assertEqual(res[4], [6])

        solution = sec.find_solution(3, 5)
        self.assertEqual(solution.solution_exist, True)
        self.assertEqual(solution.monster_level, 3)
        self.assertEqual(solution.total_cards, 5)
        self.assertEqual(solution.fusion_level, 1)
        self.assertEqual(solution.xyz_rank, 2)

        solution = sec.find_solution(4, 7)
        self.assertEqual(solution.solution_exist, False)

        solution = sec.find_solution(5, 7)
        self.assertEqual(solution.solution_exist, False)

    def test_2x2_with_ban(self):
        """ban rank 2"""
        sec = SimultaneousEquationCannonsState([1, 2], [1, 2])
        sec.set_banish_zone_monster_level([], [2], CompareMode.EXCLUDE)
        res = sec.value_table
        self.assertEqual(len(res.keys()), 3)
        self.assertEqual(res[2], [3])
        self.assertEqual(res[3], [3, 4])
        self.assertEqual(res[4], [4])

        solution = sec.find_solution(4, 4)
        self.assertEqual(solution.solution_exist, True)
        self.assertEqual(solution.monster_level, 4)
        self.assertEqual(solution.total_cards, 4)
        self.assertEqual(solution.fusion_level, 2)
        self.assertEqual(solution.xyz_rank, 1)


class SecTestCase01(unittest.TestCase):
    """test fusion 2-6 xyz 2-6"""

    def test_5x5(self):
        """normal case find solution monster level 7 total 10"""
        sec = SimultaneousEquationCannonsState([2, 3, 4, 5, 6], [2, 3, 4, 5, 6])
        res = sec.value_table
        self.assertEqual(len(res.keys()), 9)
        res = sec.value_table
        self.assertEqual(res[8], [10, 11, 12, 13, 14])

        solution = sec.find_solution(7, 10)
        self.assertEqual(solution.solution_exist, True)
        self.assertEqual(solution.monster_level, 7)
        self.assertEqual(solution.total_cards, 10)
        self.assertEqual(solution.fusion_level, 4)
        self.assertEqual(solution.xyz_rank, 3)

    def test_5x5_with_ban(self):
        """pre banish rank 4 and level 4, find solution level 9 total 16"""
        sec = SimultaneousEquationCannonsState([2, 3, 4, 5, 6], [2, 3, 4, 5, 6])
        sec.set_banish_zone_monster_level([4], [4], CompareMode.EXCLUDE)

        solution = sec.find_solution(7, 10)
        self.assertEqual(solution.solution_exist, False)

        solution = sec.find_solution(9, 16)
        self.assertEqual(solution.solution_exist, True)
        self.assertEqual(solution.fusion_level, 6)
        self.assertEqual(solution.xyz_rank, 5)

        solution = sec.find_solution(6, 12)
        self.assertEqual(solution.solution_exist, True)
        self.assertEqual(solution.fusion_level, 2)
        self.assertEqual(solution.xyz_rank, 5)
