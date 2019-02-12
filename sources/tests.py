from unittest import TestCase

from sources.main import Board, Color, Win


class BoardTestCase(TestCase):
    def test_no_winning_combination(self):
        board = Board()
        for i in range(0, 3):
            board.add_to_column(0, Color.YELLOW)
        board.check_winning_combination()

        board = Board()
        for i in range(0, 3):
            board.add_to_column(1, Color.YELLOW)
        board.check_winning_combination()

    def test_winning_combination_on_first_column(self):
        board = Board()
        with self.assertRaises(Win):
            for i in range(0, 4):
                board.add_to_column(0, Color.YELLOW)
            board.check_winning_combination()

    def test_winning_combination_on_first_row(self):
        board = Board()
        with self.assertRaises(Win):
            for i in range(0, 4):
                board.add_to_column(i, Color.YELLOW)
            board.check_winning_combination()
