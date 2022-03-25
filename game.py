"""
Written by Lucas Jensen for BeaverHacks Spring 2022
Last updated 3/24/2022
The main file for playing chess with Pygame over a local network
"""
import os
import pickle
import sys

import pygame

from chess import Chess
from server import serve

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
BOARD = pygame.image.load(os.path.join('assets', 'chess_board.png'))
PLAYER_2 = len(sys.argv) > 1


def pos_to_pix(pos, width):
    """
    converts a coordinate from the chess class to a pixel position
    :param pos: position, ex. 'a1'
    :param width: the width of the Pygame window
    :return: pixel as tuple
    """
    border = (50 / 900) * width
    tile_size = (100 / 900) * width
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


def main():
    """
    The main function for running Chess with Pygame
    """
    chess = Chess()
    pygame.init()
    pygame.display.set_caption("Chess PvP")
    run = True
    changes = True
    move = {
        'sq_from': None,
        'sq_to': None
    }
    # serve()  # serve the game directory locally

    while run:
        x, y = WIN.get_size()
        x = max(x, y)
        y = max(x, y)
        width = x
        border = (50 / 900) * width
        tile_size = (100 / 900) * width

        if PLAYER_2:

            try:
                dbfile = open('/Volumes/Users/lucas/Dropbox/Coding/ChessPvP/game_pickle', 'rb')
                chess = pickle.load(dbfile)
            except FileNotFoundError:
                chess = Chess()
        else:
            try:
                dbfile = open('game_pickle', 'rb')
                chess = pickle.load(dbfile)
            except:
                chess = Chess()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_c:
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
                print("made move!")
                changes = True

                # reset
                move = {
                    'sq_from': None,
                    'sq_to': None
                }

        if move['sq_from']:
            draw_window(chess, sq_from=move['sq_from'], width=x, height=y)
        else:
            draw_window(chess, width=x, height=y)

        if changes:
            if PLAYER_2:
                dbfile = open('/Volumes/Users/lucas/Dropbox/Coding/ChessPvP/game_pickle', 'wb')
                pickle.dump(chess, dbfile)
            else:
                dbfile = open('game_pickle', 'wb')
                # print("saved the game!")
                pickle.dump(chess, dbfile)
            changes = False
            print("game saved!")

    pygame.quit()


if __name__ == '__main__':
    print("Welcome to Chess!")
    print("Game data will persist upon exit.")
    print("Press 'esc' to quit, or 'c' to start a new game.")
    main()
