"""
Written by Lucas Jensen for BeaverHacks Spring 2022
Last updated 3/25/2022
The main file for playing chess with Pygame over a local network
"""
import os
import pickle
import sys

import pygame

from chess import Chess
from server import serve
from errors import CLAError

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
BOARD = pygame.image.load(os.path.join('assets', 'chess_board.png'))


def get_player():
    """
    Checks for valid and existent command line arguments
    :return: bool
    """
    if len(sys.argv) != 2:
        raise CLAError("One command line argument required.")
    elif sys.argv[1].lower() not in ["host", "player2"]:
        raise CLAError("Must specify 'host' or 'player2'")

    return sys.argv[1]


def pos_to_pix(pos, width):
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


def pix_to_coord(coord, border, tile_size):
    """converts coordinate (tuple) to a position"""
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


def draw_window(chess, sq_from=None, width=WIDTH, height=HEIGHT):
    """
    Draws the Pygame window
    :param chess: the chess object that is being played
    :param sq_from: square the piece is moving from
    :param width: width of the Pygame window
    :param height: height of the Pygame window
    """
    WIN.blit(pygame.transform.scale(BOARD, (width, height)), (0, 0))

    for piece in chess.get_pieces():
        if not piece.get_is_captured():
            file_name = os.path.join("assets", piece.get_image())
            image = pygame.image.load(file_name)
            img_size = (100 / 900) * width
            if sq_from:
                if sq_from == piece.get_position():
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)
                    WIN.blit(pygame.transform.scale(image, (img_size, img_size)), mouse_pos)
                else:
                    WIN.blit(pygame.transform.scale(image, (img_size, img_size)), (pos_to_pix(piece.get_position(), width)))
            else:
                WIN.blit(pygame.transform.scale(image, (img_size, img_size)), (pos_to_pix(piece.get_position(), width)))

    pygame.display.update()

    # redraw the window if it has been resized
    w, h = pygame.display.get_surface().get_size()
    if w != width and h != height:
        scale_board(chess)


def scale_board(chess):
    """
    Scales the board and window based on the user resizing the window. Maintains scale aspect ratio.
    """
    x, y = WIN.get_size()
    x = max(x, y)
    y = max(x, y)
    draw_window(chess, width=x, height=y)
    pygame.display.set_mode((x, y), pygame.RESIZABLE)


def greeting():
    print("Welcome to Chess!")
    print("Game data will persist upon exit.")
    print("Press 'esc' to quit, or 'c' to start a new game.")


def open_game(game_save):
    """
    Opens the pickle file and restores (or initializes) the playable Chess object
    :param game_save: file path
    :return: chess object
    """
    try:
        dbfile = open(game_save, 'rb')
        chess = pickle.load(dbfile)
    except:
        # something has gone wrong with the file, such as it not existing, so let's start over.
        chess = Chess()

    return chess


def prep_game():
    """
    Prepared Pygame to run Chess
    :return: player string
    """
    pygame.init()
    pygame.display.set_caption("Chess PvP")
    icon = pygame.image.load('assets/white_queen.png')
    pygame.display.set_icon(icon)

    player = get_player()

    if player == "host":
        serve()  # start the server to share the pickle file

    return player


def get_path(player):
    """
    Determines the file path for the pickled save file
    :param player: string of which player is being played as
    :return: string: file path
    """
    if player == "player2":
        return '/Volumes/Users/lucas/Dropbox/Coding/ChessPvP/game_pickle'

    return 'game_pickle'


def main():
    """
    The main function for running Chess with Pygame
    """
    player = prep_game()
    run = True
    changes = True
    move = {
        'sq_from': None,
        'sq_to': None
    }
    game_save = get_path(player)  # specify file path based upon player number

    while run:
        # the main loop for running the game
        x, y = WIN.get_size()
        x = max(x, y)
        y = max(x, y)
        width = x
        border = (5 / 90) * width  # these numbers come from the original file dimensions
        tile_size = (1 / 9) * width

        # open the pickle file to restore a game, or start from scratch
        try:
            dbfile = open(game_save, 'rb')
            chess = pickle.load(dbfile)
        except:
            # something has gone wrong with the file, such as it not existing, so let's start over.
            chess = Chess()

        # get user input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_c:
                    # clears the board to start a new game
                    chess = Chess()
                    changes = True
            elif event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                move['sq_to'] = None  # verifies there isn't a lingering value in 'sq_to' from a random click
                coord = pygame.mouse.get_pos()
                if border < coord[0] < width - border and border < coord[1] < width - border:
                    move['sq_from'] = pix_to_coord(coord, border, tile_size)

            elif event.type == pygame.MOUSEBUTTONUP:
                coord = pygame.mouse.get_pos()
                if border < coord[0] < width - border and border < coord[1] < width - border:
                    move['sq_to'] = pix_to_coord(coord, border, tile_size)

            if move['sq_from'] and move['sq_to']:
                # make the actual move
                chess.make_move(move['sq_from'], move['sq_to'])
                # print("made move!")
                changes = True

                # reset
                move = {
                    'sq_from': None,
                    'sq_to': None
                }

        # update window
        if move['sq_from']:
            draw_window(chess, sq_from=move['sq_from'], width=x, height=y)
        else:
            draw_window(chess, width=x, height=y)

        # only load the pickle file if changes have been made
        if changes:
            dbfile = open(game_save, 'wb')
            pickle.dump(chess, dbfile)
            changes = False
            # print("game saved!")

    pygame.quit()


if __name__ == '__main__':
    greeting()
    main()
