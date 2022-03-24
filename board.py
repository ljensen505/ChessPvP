"""
Written by Lucas Jensen
Last updated 3/24/2022
The Board class, which is used as a parameter of Chess
"""
import os


class Board:
    """Represents a chess board"""
    def __init__(self):
        """initialize single data member"""
        self._board = self._initialize_board()
        self._image = os.path.join("assets", "chess_board.png")

    @staticmethod
    def _initialize_board():
        """initializes an empty board"""
        row_8 = ['8', ' ', '.', ' ', '.', ' ', '.', ' ', '.']
        row_7 = ['7', '.', ' ', '.', ' ', '.', ' ', '.', ' ']
        row_6 = ['6', ' ', '.', ' ', '.', ' ', '.', ' ', '.']
        row_5 = ['5', '.', ' ', '.', ' ', '.', ' ', '.', ' ']
        row_4 = ['4', ' ', '.', ' ', '.', ' ', '.', ' ', '.']
        row_3 = ['3', '.', ' ', '.', ' ', '.', ' ', '.', ' ']
        row_2 = ['2', ' ', '.', ' ', '.', ' ', '.', ' ', '.']
        row_1 = ['1', '.', ' ', '.', ' ', '.', ' ', '.', ' ']
        row_0 = ['`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        return [row_8, row_7, row_6, row_5, row_4, row_3, row_2, row_1, row_0]

    def get_board(self):
        """returns the board"""
        return self._board

    def get_image(self):
        """returns the file path of the board image"""
        return self._image
