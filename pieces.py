"""
Written by Lucas Jensen
Last updated 3/24/2022
A Piece parent class and various piece-specific classes that inherit from Piece
"""
import os


class Piece:
    """
    A parent class representing a generic chess piece.  Specific classes for each piece
    will inherit from this class.
    """
    def __init__(self, color, position):
        """A generic class to represent a chess piece. Specific pieces inherit from this parent class"""
        self._color = color  # should be 'W' or 'B'
        self._position = position
        self._is_captured = False
        self._sprite = None
        self._has_moved = False
        self._piece_type = None
        self._image = None
        self._legal_moves = None
        self._targets = None

    def get_targets(self):
        """returns a list of potential targets"""
        return self._targets

    def set_targets(self, targets):
        """updates a list of pieces that self can capture"""
        self._targets = targets

    def set_legal_moves(self, legal_moves):
        """updates the piece's available moves"""
        self._legal_moves = legal_moves

    def get_image(self):
        """returns the filepath of the piece's corresponding image"""
        return self._image

    def get_legal_moves(self):
        """returns a list of legal moves"""
        return self._legal_moves

    def set_is_captured(self):
        """sets capture status to True and position to None"""
        self._is_captured = True
        self._position = None

    def get_has_moved(self):
        """returns whether the piece has moved"""
        return self._has_moved

    def set_has_moved(self):
        """sets self._has_moved to True"""
        self._has_moved = True

    def get_piece_type(self):
        """returns the piece type"""
        return self._piece_type

    def get_sprite(self):
        """returns the piece's sprite"""
        return self._sprite

    def get_position(self):
        """returns the piece's position"""
        return self._position

    def set_position(self, position):
        """sets the piece's position"""
        self._position = position

    def get_color(self):
        """returns the piece's color"""
        return self._color

    def get_is_captured(self):
        """returns the piece's capture status"""
        return self._is_captured


class Pawn(Piece):
    """Represents a Pawn in Chess. Inherits from the generic Piece class"""
    def __init__(self, color, position):
        super().__init__(color, position)
        self._sprite = 'P'
        self._piece_type = 'Pawn'
        self._image = os.path.join(f"{letter_to_color(self.get_color())}_{self._piece_type.lower()}.png")


class Rook(Piece):
    """Represents a Pawn in Chess. Inherits from the generic Piece class"""
    def __init__(self, color, position):
        super().__init__(color, position)
        self._sprite = 'R'
        self._piece_type = 'Rook'
        self._image = os.path.join(f"{letter_to_color(self.get_color())}_{self._piece_type.lower()}.png")


class Bishop(Piece):
    """Represents a Pawn in Chess. Inherits from the generic Piece class"""
    def __init__(self, color, position):
        super().__init__(color, position)
        self._sprite = 'B'
        self._piece_type = 'Bishop'
        self._image = os.path.join(f"{letter_to_color(self.get_color())}_{self._piece_type.lower()}.png")


class Knight(Piece):
    """Represents a Pawn in Chess. Inherits from the generic Piece class"""
    def __init__(self, color, position):
        super().__init__(color, position)
        self._sprite = 'H'  # H for horse, as K is taken by King
        self._piece_type = 'Knight'
        self._image = os.path.join(f"{letter_to_color(self.get_color())}_{self._piece_type.lower()}.png")


class Queen(Piece):
    """Represents a Pawn in Chess. Inherits from the generic Piece class"""
    def __init__(self, color, position):
        super().__init__(color, position)
        self._sprite = 'Q'
        self._piece_type = 'Queen'
        self._image = os.path.join(f"{letter_to_color(self.get_color())}_{self._piece_type.lower()}.png")


class King(Piece):
    """Represents a Pawn in Chess. Inherits from the generic Piece class"""
    def __init__(self, color, position):
        super().__init__(color, position)
        self._sprite = 'K'
        self._piece_type = 'King'
        self._check = False
        self._image = os.path.join(f"{letter_to_color(self.get_color())}_{self._piece_type.lower()}.png")

    def get_check(self):
        """returns the king's check status"""
        return self._check

    def set_check(self, status):
        """
        sets the king's check status
        :param status: True or False
        :return: nothing
        """
        self._check = status


def letter_to_color(char):
    """converts 'W' or 'B' into 'white' or 'black'"""
    if char == 'B':
        return "black"
    else:
        return "white"


if __name__ == "__main__":
    print(Pawn('W', 'a2').get_image())
    print(King('B', 'd8').get_image())
