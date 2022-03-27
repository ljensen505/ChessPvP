"""
Written by Lucas Jensen
Last updated 3/26/2022
The Chess class which contains a majority of the gameplay logic
"""
from pieces import Pawn, Rook, Bishop, Knight, Queen, King
from board import Board
from colorama import init, Fore, Back, Style


class Chess:
    """The main game class. This handles all the logic for the game, and uses two other classes to create
    portions of the game as objects."""

    def __init__(self):
        """Initialize all data members as private"""
        init(autoreset=True)  # initialize colorama; always reset colors
        self._board = Board()
        self._turn_count = 0
        self._game_state = "UNFINISHED"
        self._pieces = self._make_pieces()
        self._update_legal_moves()
        self._update_targets()

    def get_pieces(self):
        """returns a list of all pieces"""
        return self._pieces

    def get_active_player(self):
        """returns the active player"""
        if self._turn_count % 2 == 0:
            return "W"
        else:
            return "B"

    def make_move(self, sq_from, sq_to):
        """
        Makes a chess move! This is the main method that a user will use
        :param sq_from: origination
        :param sq_to: destination
        :return: bool
        """
        piece = self.get_piece_by_square(sq_from)
        opponent = self.get_piece_by_square(sq_to)
        if piece:
            if self._is_valid_move(sq_from, sq_to):
                self._move_piece(sq_from, sq_to)
                # the piece now exists in sq_to instead of sq_from
                self._update_legal_moves()
                self._update_targets()
                self._check_for_check()

                # check for checkmate
                # TODO :(

                # check for self check
                for piece in self._pieces:
                    if piece.get_piece_type() == "King":
                        if piece.get_check() and piece.get_color() == self.get_piece_by_square(sq_to).get_color():
                            self._move_piece(sq_to, sq_from)
                            if opponent:
                                opponent._is_captured = False
                                opponent.set_position(sq_to)
                            self._update_legal_moves()
                            self._update_targets()

                            return False

                self._turn_count += 1

                return True

        return False

    def _is_checkmate(self, sq_from, sq_to):
        """TODO"""
        for piece in self._pieces:
            if piece.get_color() == self.get_active_player():
                for move in piece.get_legal_moves():
                    orig = piece.get_position()
                    target = self.get_piece_by_square(move)
                    if self.make_move(orig, move):
                        self._turn_count -= 1
                        piece.set_position(orig)
                        if target:
                            target._captured = False
                            target.set_position(move)
                        return False

        return True

    def _check_for_check(self):
        """
        checks all piece targets for check and sets king object attributes accordingly
        :return: nothing
        """
        for piece in self._pieces:
            if piece.get_position() is not None:
                for target in piece.get_targets():
                    target = self.get_piece_by_square(target)
                    if target.get_piece_type() == "King":
                        self._game_state = "CHECK"
                        target.set_check(True)
                        return

        for piece in self._pieces:
            if piece.get_piece_type() == "King":
                self._game_state = "UNFINISHED"
                piece.set_check(False)

    def _update_legal_moves(self):
        """
        update the list of legal moves for each piece object
        :return: nothing
        """
        for piece in self._pieces:
            if piece.get_position() is not None:
                moves = self.legal_moves(piece.get_position())
                piece.set_legal_moves(moves)

    def _update_targets(self):
        """
        updates the list of targets with legal moves for each piece object
        :return: nothing
        """
        for piece in self._pieces:
            targets = []
            for move in piece.get_legal_moves():
                if self.get_piece_by_square(move):
                    if self.get_piece_by_square(move).get_color() != piece.get_color():
                        if piece.get_piece_type() == "Pawn":
                            # pawn is unique in being only able to attack diagonally
                            if move[0] != piece.get_position():
                                targets.append(move)
                        else:
                            targets.append(move)
            piece.set_targets(targets)

    def _is_valid_move(self, sq_from, sq_to):
        """
        determines of a move is valid
        :param sq_from: origination square
        :param sq_to: destination square
        :return: bool
        """
        piece = self.get_piece_by_square(sq_from)
        target = self.get_piece_by_square(sq_to)
        # TODO add check for putting oneself into check
        if self.get_active_player() == piece.get_color():
            if sq_from != sq_to:
                if self._game_state == "UNFINISHED" or self._game_state == "CHECK":
                    if sq_to in self.legal_moves(sq_from):
                        if target:
                            if piece.get_color() != target.get_color():
                                return True
                        else:
                            return True

        return False

    def legal_moves(self, sq_from):
        """
        determines how to find a legal move
        :param sq_from: origination square
        :return: list of valid moves, as generated by a helper function
        """
        piece = self.get_piece_by_square(sq_from)
        if piece.get_position() is not None:
            if piece.get_piece_type() == "Pawn":
                return self._pawn_moves(sq_from)
            elif piece.get_piece_type() == "Knight":
                return self._knight_moves(sq_from)
            elif piece.get_piece_type() == "Rook":
                return self._rook_moves(sq_from)
            elif piece.get_piece_type() == "Bishop":
                return self._bishop_moves(sq_from)
            elif piece.get_piece_type() == "Queen":
                return self._queen_moves(sq_from)
            elif piece.get_piece_type() == "King":
                return self._king_moves(sq_from)
        else:
            return False

    def _pawn_moves(self, sq_from):
        """
        finds all legal moves for a pawn
        :param sq_from: origination square
        :return: list of valid moves
        """
        pawn = self.get_piece_by_square(sq_from)

        # make list of all possible pawn moves
        possible = []
        if pawn.get_color() == 'W':
            square = f"{sq_from[0]}{int(sq_from[1]) + 1}"
            if self.get_square_occupant(square) == 'NONE':
                possible.append(square)
            square = f"{sq_from[0]}{int(sq_from[1]) + 2}"
            if not pawn.get_has_moved() and self.get_square_occupant(square) == 'NONE':
                possible.append(square)
            square = f"{chr(ord(sq_from[0]) + 1)}{int(sq_from[1]) + 1}"
            if self.get_square_occupant(square) == 'B':
                possible.append(square)
            square = f"{chr(ord(sq_from[0]) - 1)}{int(sq_from[1]) + 1}"
            if self.get_square_occupant(square) == 'B':
                possible.append(square)

        else:
            # pawn must be black
            square = f"{sq_from[0]}{int(sq_from[1]) - 1}"
            if self.get_square_occupant(square) == 'NONE':
                possible.append(square)
            square = f"{sq_from[0]}{int(sq_from[1]) - 2}"
            if not pawn.get_has_moved() and self.get_square_occupant(square) == 'NONE':
                possible.append(square)
            square = f"{chr(ord(sq_from[0]) + 1)}{int(sq_from[1]) - 1}"
            if self.get_square_occupant(square) == 'W':
                possible.append(square)
            square = f"{chr(ord(sq_from[0]) - 1)}{int(sq_from[1]) - 1}"
            if self.get_square_occupant(square) == 'W':
                possible.append(square)

        valid = []

        for move in possible:
            if move[0] in self._valid_alpha() and move[1] in self._valid_nums():
                if self.get_square_occupant(move) != self.get_square_occupant(sq_from):
                    valid.append(move)

        return valid

    def _rook_moves(self, sq_from):
        """
        finds all valid moves for a rook
        :param sq_from: origination square
        :return: list of valid destinations
        """
        rook = self.get_piece_by_square(sq_from)

        possible = self._find_horz_vert(rook, sq_from)

        valid = []

        for move in possible:
            if move[0] in self._valid_alpha() and move[1] in self._valid_nums():
                if self.get_square_occupant(move) != self.get_square_occupant(sq_from):
                    valid.append(move)

        return valid

    def _knight_moves(self, sq_from):
        """
        finds all valid moves for a knight
        :param sq_from: origination square
        :return: list of valid moves
        """
        possible = [  # clockwise from up-up-left
            f"{chr(ord(sq_from[0]) - 1)}{int(sq_from[1]) + 2}",
            f"{chr(ord(sq_from[0]) + 1)}{int(sq_from[1]) + 2}",
            f"{chr(ord(sq_from[0]) + 2)}{int(sq_from[1]) + 1}",
            f"{chr(ord(sq_from[0]) + 2)}{int(sq_from[1]) - 1}",
            f"{chr(ord(sq_from[0]) + 1)}{int(sq_from[1]) - 2}",
            f"{chr(ord(sq_from[0]) - 1)}{int(sq_from[1]) - 2}",
            f"{chr(ord(sq_from[0]) - 2)}{int(sq_from[1]) + 1}",
            f"{chr(ord(sq_from[0]) - 2)}{int(sq_from[1]) - 1}",
        ]

        valid = []

        for move in possible:
            if move[0] in self._valid_alpha() and move[1] in self._valid_nums():
                if self.get_square_occupant(move) != self.get_square_occupant(sq_from):
                    valid.append(move)

        return valid

    def _bishop_moves(self, sq_from):
        """
        finds all legal destinations for a bishop
        :param sq_from: origination square
        :return: a list of valid destinations
        """
        bishop = self.get_piece_by_square(sq_from)

        possible = self._find_diagonals(bishop, sq_from)

        valid = []

        for move in possible:
            if move[0] in self._valid_alpha() and move[1] in self._valid_nums():
                if self.get_square_occupant(move) != self.get_square_occupant(sq_from):
                    valid.append(move)

        return valid

    def _queen_moves(self, sq_from):
        """
        finds all legal destinations for a queen
        :param sq_from: origination square
        :return: list of valid destinations
        """
        queen = self.get_piece_by_square(sq_from)

        diags = self._find_diagonals(queen, sq_from)
        possible = self._find_horz_vert(queen, sq_from)

        for move in diags:
            possible.append(move)

        valid = []

        for move in possible:
            if move[0] in self._valid_alpha() and move[1] in self._valid_nums():
                if self.get_square_occupant(move) != self.get_square_occupant(sq_from):
                    valid.append(move)

        return valid

    def _king_moves(self, sq_from):
        """
        finds all legal moves for a king
        :param sq_from: origination square
        :return: list of valid desinations
        """
        king = self.get_piece_by_square(sq_from)
        valid = []
        possible = [
            f"{sq_from[0]}{int(sq_from[1]) + 1}",
            f"{chr(ord(sq_from[0]) + 1)}{int(sq_from[1]) + 1}",
            f"{chr(ord(sq_from[0]) + 1)}{int(sq_from[1])}",
            f"{chr(ord(sq_from[0]) + 1)}{int(sq_from[1]) - 1}",
            f"{sq_from[0]}{int(sq_from[1]) - 1}",
            f"{chr(ord(sq_from[0]) - 1)}{int(sq_from[1]) - 1}",
            f"{chr(ord(sq_from[0]) - 1)}{int(sq_from[1])}",
            f"{chr(ord(sq_from[0]) - 1)}{int(sq_from[1]) + 1}",
        ]

        for move in possible:
            if move[0] in self._valid_alpha() and move[1] in self._valid_nums():
                if self.get_square_occupant(move) != self.get_square_occupant(sq_from):
                    # if not self.self_check(sq_from, move):
                    valid.append(move)

        return valid

    def _move_piece(self, sq_from, sq_to):
        """
        moves a piece from one square to another
        :param sq_from: origination
        :param sq_to: destination
        :return: nothing
        """
        piece = self.get_piece_by_square(sq_from)
        opponent = self.get_piece_by_square(sq_to)
        if opponent:
            if opponent.get_color() != piece.get_color():
                if opponent.get_color() == 'W':
                    color = 'White'
                else:
                    color = 'Black'
                print(f"{color} {opponent.get_piece_type()} has been captured!")
                opponent.set_is_captured()

        piece.set_has_moved()
        piece.set_position(sq_to)

    def _find_horz_vert(self, piece, sq_from):
        """
        finds all valid horizontal and vertical moves. Used by Queen, and Rook
        :param piece: the piece object
        :param sq_from: origination
        :return: list of valid horizontal and vertical destinations
        """
        valid = []

        # check up
        for i in range(8):
            square = f"{sq_from[0]}{int(sq_from[1]) + i}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color():
                break
            if square[0] not in self._valid_alpha() or square[1] not in self._valid_nums():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        # check to right
        for i in range(8):
            square = f"{chr(ord(sq_from[0]) + i)}{int(sq_from[1])}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color():
                break
            if square[0] not in self._valid_alpha() or square[1] not in self._valid_nums():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        # check down
        for i in range(8):
            square = f"{sq_from[0]}{int(sq_from[1]) - i}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color():
                break
            if square[0] not in self._valid_alpha() or square[1] not in self._valid_nums():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        # check to left
        for i in range(8):
            square = f"{chr(ord(sq_from[0]) - i)}{int(sq_from[1])}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color():
                break
            if square[0] not in self._valid_alpha() or square[1] not in self._valid_nums():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        return valid

    def _find_diagonals(self, piece, sq_from):
        """
        checks for validity of diagonal moves. Used by Bishop and Queen
        :param piece: piece object
        :param sq_from: origination
        :return: a list of valid diagonal moves
        """
        # add valid moves to a list, then check sq_to against list
        valid = []

        # check up and to right - these checks can go off-board since moves are already verified as on-board
        for i in range(8):
            square = f"{chr(ord(sq_from[0]) + i)}{int(sq_from[1]) + i}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color() or square[0] not in self._valid_alpha():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        # check down and to right
        for i in range(8):
            square = f"{chr(ord(sq_from[0]) + i)}{int(sq_from[1]) - i}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color() or square[0] not in self._valid_alpha():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        # check down and to left
        for i in range(8):
            square = f"{chr(ord(sq_from[0]) - i)}{int(sq_from[1]) - i}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color() or square[0] not in self._valid_alpha():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        # check up and to left
        for i in range(8):
            square = f"{chr(ord(sq_from[0]) - i)}{int(sq_from[1]) + i}"
            if square == sq_from:
                continue
            if self.get_square_occupant(square) == piece.get_color() or square[0] not in self._valid_alpha():
                break
            valid.append(square)
            if self.is_occupied(square):
                break

        return valid

    def _make_pieces(self):
        """
        A private method that creates pieces of each color. Should never be accessed except by init
        :return: a list of piece objects
        """
        pieces = []

        # create white pieces
        col = 'W'
        for w in range(8):
            # make 8 white pawns
            pieces.append(Pawn(col, f'{self._num_to_alpha(w + 1)}2'))
        pieces.append(Rook(col, 'a1'))
        pieces.append(Rook(col, 'h1'))
        pieces.append(Knight(col, 'b1'))
        pieces.append(Knight(col, 'g1'))
        pieces.append(Bishop(col, 'c1'))
        pieces.append(Bishop(col, 'f1'))
        pieces.append(Queen(col, 'd1'))
        pieces.append(King(col, 'e1'))

        # create black pieces
        col = 'B'
        for b in range(8):
            pieces.append(Pawn('B', f'{self._num_to_alpha(b + 1)}7'))
        pieces.append(Rook(col, 'a8'))
        pieces.append(Rook(col, 'h8'))
        pieces.append(Knight(col, 'b8'))
        pieces.append(Knight(col, 'g8'))
        pieces.append(Bishop(col, 'c8'))
        pieces.append(Bishop(col, 'f8'))
        pieces.append(Queen(col, 'd8'))
        pieces.append(King(col, 'e8'))

        return pieces

    def print_board(self):
        """
        prints the current board, including grid labels
        This method is only used for backend testing.
        :return: nothing
        """
        for row in range(9):
            for col in range(9):
                if col != 0 and row != 8:
                    if self._board.get_board()[row][col] == '.':
                        back = Back.LIGHTBLACK_EX
                    else:
                        back = Back.LIGHTWHITE_EX
                else:
                    back = ''

                square_index = f"{col}{row}"
                square_name = self._convert_to_coord(square_index)
                piece = self.get_piece_by_square(square_name)

                print(back + ' ', end='')
                if self.get_square_occupant(square_name) != "NONE":
                    if self.get_square_occupant(square_name) == 'W':
                        color = Fore.LIGHTMAGENTA_EX
                    else:
                        color = Fore.BLACK
                    print(color + back + Style.BRIGHT + piece.get_sprite(), end='')
                else:
                    tile = self._board.get_board()[row][col]
                    if tile == '`' or tile == '.':
                        print(back + ' ', end='')
                    else:
                        print(back + tile, end='')
                print(back + ' ', end='')

            print('\n', end='')

    def is_occupied(self, square):
        """
        Determines of a specified square is occupied
        :param square: the coordinates of the square a piece wants to move to
        :return: Bool
        """
        if self.get_square_occupant(square) != "NONE":
            return True

        return False

    def get_piece_by_square(self, square):
        """
        Finds the piece object that occupies a specified square, if any
        :param square: the coordinates of the square to check. Ex. 'a2'
        :return: piece object, or False of not occupied
        """
        for piece in self._pieces:
            if piece.get_position() == square:
                return piece

        return False

    def get_square_occupant(self, square):
        """
        Determines the color of the occupant of a square, if any
        :param square: the coordinates of the square to check. Ex. 'a2'
        :return: 'WHITE', 'BLACK', or 'NONE'
        """
        for piece in self._pieces:
            if piece.get_position() == square and not piece.get_is_captured():
                return piece.get_color()

        return 'NONE'

    @staticmethod
    def _convert_to_coord(index):
        """
        converts a coordinate using indices to a string using grid labels
        :param index: [i][j]
        :return: coordinate using the grid
        """
        row_dict = {
            '0': '8',
            '1': '7',
            '2': '6',
            '3': '5',
            '4': '4',
            '5': '3',
            '6': '2',
            '7': '1',
            '8': None,
        }

        col_dict = {
            '0': None,
            '1': 'a',
            '2': 'b',
            '3': 'c',
            '4': 'd',
            '5': 'e',
            '6': 'f',
            '7': 'g',
            '8': 'h',
        }

        row = row_dict[index[1]]
        col = col_dict[index[0]]

        return f"{col}{row}"

    @staticmethod
    def _convert_to_index(coord):
        """
        converts a string coordinate to indices. Ex. 'a2' to '61'
        :param coord: coordinate according to grid label
        :return: coordinate by index
        """
        row_dict = {
            '8': '0',
            '7': '1',
            '6': '2',
            '5': '3',
            '4': '4',
            '3': '5',
            '2': '6',
            '1': '7',
            '0': None,
        }

        col_dict = {
            'a': '1',
            'b': '2',
            'c': '3',
            'd': '4',
            'e': '5',
            'f': '6',
            'g': '7',
            'h': '8',
        }

        col = col_dict[coord[0]]
        row = row_dict[coord[1]]

        return f"{col}{row}"

    @staticmethod
    def _num_to_alpha(num):
        """
        converts an integer (1-8) into a corresponding letter
        :param num: 1 through 8 inclusive
        :return: corresponding number
        """
        num = str(num)
        num_dict = {
            '0': None,
            '1': 'a',
            '2': 'b',
            '3': 'c',
            '4': 'd',
            '5': 'e',
            '6': 'f',
            '7': 'g',
            '8': 'h',
        }

        return num_dict[num]

    @staticmethod
    def _valid_alpha():
        """returns a list of valid alpha grid chars"""
        return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    @staticmethod
    def _valid_nums():
        """returns a list of valid numbers as strings"""
        return [str(num) for num in range(1, 9)]


if __name__ == "__main__":
    game = Chess()
    game.print_board()

