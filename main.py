"""
Written by Lucas Jensen for BeaverHacks Spring 2022
Last updated 10/8/2022
The main file for playing chess with friends!
"""
import os
import pickle
import sys

import pygame

from chess import Chess
from server import Server
from helpers import greeting, pix_to_coord, pos_to_pix, load_game


class Game:
    def __init__(self, chess: Chess):
        self.WIDTH, self.HEIGHT = 800, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.BOARD = pygame.image.load(os.path.join("assets", "chess_board.png"))
        self.chess = chess
        self.game_save = ".game_pickle"
        self.server = Server()

    def scale_board(self):
        """
        Scales the board and window based on the user resizing the window.
        Maintains aspect ratio.
        """
        x, y = self.WIN.get_size()
        x = max(x, y)
        y = max(x, y)
        self.draw_window()
        pygame.display.set_mode((x, y))

    def draw_window(self, sq_from=None):
        """
        Draws the Pygame window
        :param chess: the chess object that is being played
        :param sq_from: square the piece is moving from
        :param width: width of the Pygame window
        :param height: height of the Pygame window
        """
        self.WIN.blit(
            pygame.transform.scale(self.BOARD, (self.WIDTH, self.HEIGHT)), (0, 0)
        )

        for piece in self.chess.get_pieces():
            if not piece.get_is_captured():
                file_name = os.path.join("assets", piece.get_image())
                image = pygame.image.load(file_name)
                img_size = int((100 / 900) * self.WIDTH)
                if sq_from:
                    if sq_from == piece.get_position():
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)
                        self.WIN.blit(
                            pygame.transform.scale(image, (img_size, img_size)),
                            mouse_pos,
                        )
                    else:
                        self.WIN.blit(
                            pygame.transform.scale(image, (img_size, img_size)),
                            (pos_to_pix(piece.get_position(), self.WIDTH)),
                        )
                else:
                    self.WIN.blit(
                        pygame.transform.scale(image, (img_size, img_size)),
                        (pos_to_pix(piece.get_position(), self.WIDTH)),
                    )

        pygame.display.update()

        # redraw the window if it has been resized
        # w, h = pygame.display.get_surface().get_size()
        # if w != self.WIDTH and h != self.HEIGHT:
        #     self.scale_board()

    def play(self):
        """
        The main method for running Chess with Pygame
        """
        making_move = False
        loop_count = 0  # only make get requests on certain iterations
        run = True
        move = {"sq_from": None, "sq_to": None}

        while run:
            # the main loop for running the game
            loop_count %= 30  # no need to exceed 30
            clock.tick(30)
            x, y = self.WIN.get_size()
            x = max(x, y)
            y = max(x, y)
            width = x
            # these numbers come from the original file dimensions
            border = (5 / 90) * width
            tile_size = (1 / 9) * width

            if loop_count == 0 and not making_move:
                # check with API every time loop counter resets
                api_state = self.server.get_game()
                api_time = float(api_state["time"])
                api_turn = int(api_state["turn"])

                if api_time > self.chess.get_time():
                    if api_turn == 0:
                        # the game has been cleared
                        self.chess = Chess(creation=api_time)
                    elif api_turn > self.chess.get_turn():
                        # the opponent has moved
                        self.chess.make_move(api_state["from"], api_state["to"])

            # get user input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # save the game locally and quit
                        dbfile = open(self.game_save, "wb")
                        pickle.dump(self.chess, dbfile)
                        run = False
                    elif event.key == pygame.K_c:
                        # clears the board to start a new game
                        creation = self.server.reset()["time"]
                        self.chess = Chess(creation=creation)

                elif event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # verifies there isn't a lingering value in 'sq_to' from a
                    # random click
                    move["sq_to"] = None

                    coord = pygame.mouse.get_pos()
                    if (
                        border < coord[0] < width - border
                        and border < coord[1] < width - border
                    ):
                        move["sq_from"] = pix_to_coord(coord, border, tile_size)  # type: ignore

                    making_move = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    coord = pygame.mouse.get_pos()
                    if (
                        border < coord[0] < width - border
                        and border < coord[1] < width - border
                    ):
                        move["sq_to"] = pix_to_coord(coord, border, tile_size)  # type: ignore

                if move["sq_from"] and move["sq_to"]:
                    # make the actual move
                    self.chess.make_move(move["sq_from"], move["sq_to"])

                    self.server.make_move(
                        self.chess.get_turn(),
                        {"from": move["sq_from"], "to": move["sq_to"]},
                        self.chess.get_time(),
                    )

                    # reset
                    move = {"sq_from": None, "sq_to": None}

                    making_move = False

            # update window
            if move["sq_from"]:
                self.draw_window(sq_from=move["sq_from"])
            else:
                self.draw_window()

            loop_count += 1

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    greeting()
    clock = pygame.time.Clock()
    game = Game(chess=load_game())
    game.play()
