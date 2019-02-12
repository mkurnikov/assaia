import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class Color(Enum):
    YELLOW = 'Y'
    RED = 'R'
    EMPTY = ' '


NUMBER_OF_COLUMNS = 7
NUMBER_OF_ROWS = 6


def make_empty_board() -> List[List[Color]]:
    board = []
    for i in range(0, NUMBER_OF_COLUMNS):
        board.append([])
        for j in range(0, NUMBER_OF_ROWS):
            board[i].append(Color.EMPTY)
    return board


class WrongMove(ValueError):
    pass


class Win(ValueError):
    pass


@dataclass
class Board:
    columns: List[List[Color]] = dataclasses.field(default_factory=make_empty_board)

    def add_to_column(self, col_ind: int, player: Color):
        current_length = sum([1 for cell in self.columns[col_ind] if cell != Color.EMPTY])
        next_position = NUMBER_OF_ROWS - current_length - 1
        if next_position < 0:
            raise WrongMove('Cannot add chip to column')
        self.columns[col_ind][NUMBER_OF_ROWS - current_length - 1] = player

    def _check_indexes_equality(self, indexes: List[Tuple[int, int]]):
        value = None
        for row_ind, col_ind in indexes:
            if row_ind < 0 or row_ind >= NUMBER_OF_ROWS:
                return False
            if col_ind < 0 or col_ind >= NUMBER_OF_COLUMNS:
                return False

            if value is None:
                value = self.columns[col_ind][row_ind]

            if value == Color.EMPTY or value != self.columns[col_ind][row_ind]:
                return False
        return True

    def _check_mask(self, row_ind, col_ind):
        # check right
        win_right = self._check_indexes_equality([(row_ind, col_ind),
                                                  (row_ind, col_ind + 1),
                                                  (row_ind, col_ind + 2),
                                                  (row_ind, col_ind + 3)])
        # check down
        win_down = self._check_indexes_equality([(row_ind, col_ind),
                                                 (row_ind - 1, col_ind),
                                                 (row_ind - 2, col_ind),
                                                 (row_ind - 3, col_ind)])
        # check right diag
        win_right_diag = self._check_indexes_equality([(row_ind, col_ind),
                                                       (row_ind - 1, col_ind + 1),
                                                       (row_ind - 2, col_ind + 2),
                                                       (row_ind - 3, col_ind + 3)])
        # check left diag
        win_left_diag = self._check_indexes_equality([(row_ind, col_ind),
                                                      (row_ind - 1, col_ind - 1),
                                                      (row_ind - 2, col_ind - 2),
                                                      (row_ind - 3, col_ind - 3)])
        return any([win_down, win_right, win_left_diag, win_right_diag])

    def check_winning_combination(self) -> None:
        # we need 4 in a row, so check every full 4x4 square (all horizontals, all verticals, diagonals)
        for row_ind in range(NUMBER_OF_ROWS):
            for col_ind in range(NUMBER_OF_COLUMNS):
                current_win = self._check_mask(row_ind, col_ind)
                if current_win:
                    raise Win()

    def show(self):
        for cell_ind in range(len(self.columns[0])):
            for col_ind in range(len(self.columns)):
                print(self.columns[col_ind][cell_ind].value, end=',')
            print('\n')


if __name__ == '__main__':
    board = Board()
    print(f'Starting game with N players: {[color.name for color in Color if color != Color.EMPTY]}')
    board.show()
    while True:
        for color in [color for color in Color if color != Color.EMPTY]:
            while True:
                col_ind = input(f'Player {color.name} turn (number 0 to {NUMBER_OF_COLUMNS}, for every column): ')
                if not col_ind.isnumeric() or int(col_ind) > NUMBER_OF_COLUMNS:
                    print('Try again (invalid position)')
                    continue
                try:
                    board.add_to_column(int(col_ind), color)
                    board.check_winning_combination()
                except WrongMove:
                    print('Try again (wrong move)')
                    continue
                except Win:
                    print(f'Player {color.name} won')
                else:
                    break
            board.show()
