import os
import pickle
from chess import Chess


def pos_to_pix(pos: str, width: int) -> tuple:
    """
    converts a coordinate from the chess class to a pixel position
    :param pos: position, ex. 'a1'
    :param width: the width of the Pygame window
    :return: pixel as tuple
    """
    border = (5 / 90) * width
    tile_size = (1 / 9) * width

    # ASCII to coordinates
    x_pix = border + (ord(pos[0]) - 97) * tile_size
    y_pix = border + (8 - int(pos[1])) * tile_size
    pix_tuple = (x_pix, y_pix)

    return pix_tuple


def pix_to_coord(coord: tuple, border: int, tile_size: float):
    """
    converts coordinate (tuple) to a position
    """
    x = coord[0]
    y = coord[1]
    pos = []

    if x < border + tile_size:
        pos.append('a')
    elif x < 2 * tile_size + border:
        pos.append('b')
    elif x < 3 * tile_size + border:
        pos.append('c')
    elif x < 4 * tile_size + border:
        pos.append('d')
    elif x < 5 * tile_size + border:
        pos.append('e')
    elif x < 6 * tile_size + border:
        pos.append('f')
    elif x < 7 * tile_size + border:
        pos.append('g')
    elif x < 8 * tile_size + border:
        pos.append('h')
    else:
        return False

    if y < tile_size + border:
        pos.append('8')
    elif y < 2 * tile_size + border:
        pos.append('7')
    elif y < 3 * tile_size + border:
        pos.append('6')
    elif y < 4 * tile_size + border:
        pos.append('5')
    elif y < 5 * tile_size + border:
        pos.append('4')
    elif y < 6 * tile_size + border:
        pos.append('3')
    elif y < 7 * tile_size + border:
        pos.append('2')
    elif y < 8 * tile_size + border:
        pos.append('1')
    else:
        return False

    return ''.join(pos)


def greeting():
    print("Welcome to Chess!")
    print("Game data will persist upon exit.")
    print("Press 'esc' to quit, or 'c' to start a new game.")


def load_game():
    # load a saved gave if it exists, else start new
    if os.path.exists('.game_pickle'):
        dbfile = open('.game_pickle', 'rb')
        chess = pickle.load(dbfile)
    else:
        chess = Chess()

    return chess
