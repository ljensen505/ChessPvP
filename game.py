"""
Written by Lucas Jensen for BeaverHacks Spring 2022
Last updated 3/24/2022
The main file for playing chess with Pygame over a local network
"""

import pygame
import os

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess PvP")
BOARD = pygame.image.load(os.path.join('assets', 'chess_board.png'))


def draw_window(width=WIDTH, height=HEIGHT):
    """
    TODO
    """
    WIN.blit(pygame.transform.scale(BOARD, (width, height)), (0, 0))

    pygame.display.update()


def scale_board():
    """
    Scales the board and window based on the user resizing the window. Maintains scale aspect ratio.
    """
    x, y = WIN.get_size()
    x = max(x, y)
    y = max(x, y)
    draw_window(x, y)
    pygame.display.set_mode((x, y), pygame.RESIZABLE)


def main():
    """
    TODO
    """
    pygame.init()
    run = True

    while run:
        scale_board()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == '__main__':
    main()
