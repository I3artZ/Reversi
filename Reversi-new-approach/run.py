import pygame, json, sys
from menu import Menu
from board import Board
from rules import Rules
from players import Human, MinMax, MonteCarlo
import reversi_func as f
import os

# some colors
black = (20, 20, 20)
green_menu = (0, 135, 10)
red = (0, 0, 255)


class Game:

    def __init__(self):
        pygame.init()
        self.screen_resolution_w = pygame.display.Info().current_w
        self.screen_resolution_h = pygame.display.Info().current_h
        # set a screen
        self.screen_width = 800
        self.screen_height = 500

        """x = (self.screen_resolution_w - self.screen_width)/2
        y = (self.screen_resolution_h - self.screen_height)/2 + 10
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))"""
        f.center_window(self)
        pygame.display.set_caption("Reversi")

        # self.clock = pygame.time.Clock()
        self.pos = []
        self.close = False
        self.game_status = False

        # grid's cell size
        self.grid_size = 0

        # program loop
        while not self.close:
            self.turn = 1
            self.menu = Menu(self)

            while self.menu.state:
                self.screen_width = 800
                self.screen_height = 500

                #centering menu window
                """x = (self.screen_resolution_w - self.screen_width) / 2
                y = (self.screen_resolution_h - self.screen_height) / 2 + 10
                os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))"""
                f.center_window(self)

                # reading position of mouse
                self.pos = pygame.mouse.get_pos()
                # close program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.menu.state = False  # quit menu loop
                        self.close = True        # quit main loop
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.menu.state = False  # quit menu loop
                        self.close = True        # quit main loop
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # choosing settings
                        self.menu.press_button()
                        # passing chosen player 1 type
                        for rect in self.menu.player_1:
                            if rect.pressed:
                                self.player_1_type = rect.player_type + "(self, 1, iter_max=" + str(
                                    self.menu.player_1_iter_max) + ", depth_of_search=" + str(
                                    self.menu.player_1_depth_of_search) + ")"
                                #self.player_1 = eval(self.player_1_type)
                        # passing chosen player 2 type
                        for rect in self.menu.player_2:
                            if rect.pressed:
                                self.player_2_type = rect.player_type + "(self, 2, iter_max=" + str(
                                    self.menu.player_2_iter_max) + ", depth_of_search=" + str(
                                    self.menu.player_2_depth_of_search) + ")"
                                #self.player_2 = eval(self.player_2_type)
                        # passing chosen board size
                        for rect in self.menu.board_size:
                            if rect.pressed:
                                self.grid_size = rect.size
                    # draw menu
                    self.screen.fill(green_menu)
                    self.menu.draw()
                    self.menu.highlight()
                    pygame.display.flip()



            # game loop
            while self.game_status:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

                # initialize board with chosen size
                self.board = Board(self)
                self.rules = Rules(self)

                # creating players
                self.player_1 = eval(self.player_1_type)
                self.player_2 = eval(self.player_2_type)

                while pygame.QUIT not in [event.type for event in pygame.event.get()] \
                        and not pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.score = self.rules.points_for_tiles(self.board.grid)
                    self.pos = pygame.mouse.get_pos()
                    x = self.pos[0]
                    y = self.pos[1]
                    column = 0
                    row = 0
                    if x < (self.screen_width - self.board.margin) and 50 < y < (
                            self.screen_height - self.board.margin):
                        column = x // (self.board.cell_size + self.board.margin)
                        row = (y - 50) // (self.board.cell_size + self.board.margin)

                    for x, y in self.rules.get_valid_move(self.board.grid, self.turn):
                        self.board.grid[y][x] = 3
                    #print(self.rules.points_for_mobility(self.board.grid, self.turn))

                    if self.turn == 1:
                        if isinstance(self.player_1, Human):
                            #print(self.rules.points_for_mobility(self.board.grid, self.turn))
                            if pygame.mouse.get_pressed()[0] == 1 and self.rules.is_valid_move(
                                    self.board.grid, 1, column, row):
                                self.player_1.make_a_move(row, column)
                                if self.rules.get_valid_move(self.board.grid, 2):
                                    self.turn = 2
                        else:
                            self.player_1.make_a_move(row, column)
                            if self.rules.get_valid_move(self.board.grid, 2):
                                self.turn = 2

                        self.score = self.rules.points_for_tiles(self.board.grid)
                        self.board.draw()
                        pygame.display.update()

                    if self.turn == 2:
                        if isinstance(self.player_2, Human):
                            # print(self.rules.points_for_mobility(self.board.grid, self.turn))
                            if pygame.mouse.get_pressed()[0] == 1 and self.rules.is_valid_move(
                                    self.board.grid, 2, column, row):
                                self.player_2.make_a_move(row, column)
                                if self.rules.get_valid_move(self.board.grid, 1):
                                    self.turn = 1
                        else:
                            self.player_2.make_a_move(row, column)
                            if self.rules.get_valid_move(self.board.grid, 1):
                                self.turn = 1

                        self.score = self.rules.points_for_tiles(self.board.grid)
                        self.board.draw()
                        pygame.display.update()
                    # pygame.display.flip()

                # after closing single game -> back to menu
                file = open("games_results.txt", "a+")
                file.write(json.dumps(self.board.save_game_info(), indent=3))
                # print(json.dumps(self.board.save_game_info(), indent=3))
                self.game_status = False
                self.menu.state = True


if __name__ == "__main__":
    Game()
