import pygame, sys
from menu import Menu
from board import Board
from rules import Rules
from players import Human, MinMax, MonteCarlo
# some colors
black = (20, 20, 20)
green_menu = (0, 135, 10)
red = (0, 0, 255)


class Game:

    def __init__(self):
        pygame.init()
        # set a screen
        self.screen_width = 800
        self.screen_height = 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Reversi")

        self.clock = pygame.time.Clock()
        self.pos = []
        self.menu = Menu(self)
        self.close = False
        self.game_status = False

        # grid's cell size
        self.grid_size = 0
        self.rules = Rules(self)
        # player 1 (black)
        self.player_1 = ""
        # player 2 (white)
        self.player_2 = ""
        # program loop
        while not self.close:
            self.turn = 1
            while self.menu.state:
                self.screen_width = 800
                self.screen_height = 500
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
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
                    if event.type == pygame.MOUSEBUTTONDOWN:  # choosing settings
                        self.menu.press_button()
                        # passing chosen player 1 type
                        for rect in self.menu.player_1:
                            if rect.pressed:
                                self.player_1 = rect.player_type
                        # passing chosen player 2 type
                        for rect in self.menu.player_2:
                            if rect.pressed:
                                self.player_2 = rect.player_type
                        # passing chosen board size
                        for rect in self.menu.board_size:
                            if rect.pressed:
                                self.grid_size = rect.size
                    # draw menu
                    self.screen.fill(green_menu)
                    self.menu.draw()
                    self.menu.highlight()
                    pygame.display.flip()

            # initialize board with chosen size
            self.board = Board(self)
            # creating players
            if self.player_1 == "human":
                self.player_1 = Human(self, 1)
            elif self.player_1 == "minmax":
                self.player_1 = MinMax(self, 1)
            elif self.player_1 == "monte carlo":
                self.player_1 = MonteCarlo(self, 1)
            if self.player_2 == "human":
                self.player_2 = Human(self, 2)
            elif self.player_2 == "minmax":
                    self.player_2 = MinMax(self, 2)
            elif self.player_2 == "monte carlo":
                    self.player_2 = MonteCarlo(self, 2)


            # changing size of screen to fit chosen board
            self.screen_width = self.grid_size * (self.board.cell_size + self.board.margin) + self.board.margin
            self.screen_height = self.grid_size * (self.board.cell_size + self.board.margin) + 50 + self.board.margin
            # game loop
            while self.game_status:
                for event in pygame.event.get():
                    self.pos = pygame.mouse.get_pos()
                    x = self.pos[0]
                    y = self.pos[1]
                    if event.type == pygame.QUIT:
                        self.game_status = False
                        self.menu.state = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_status = False
                        self.menu.state = True

                    # checking if "click" was done inside of playable field
                    if x < (self.screen_width - self.board.margin) and 50 < y < (self.screen_height - self.board.margin):
                        column = x // (self.board.cell_size + self.board.margin)
                        row = (y-50) // (self.board.cell_size + self.board.margin)
                        # print(row, column)

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.turn == 1 and self.rules.is_valid_move(self.board.grid, 1, column, row):
                        self.player_1.make_a_move(row, column)
                        if self.rules.get_valid_move(self.board.grid, 2) == []:
                            self.turn = 1
                        else:
                            self.turn = 2
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.turn == 2 and self.rules.is_valid_move(self.board.grid, 2, column, row):
                        self.player_2.make_a_move(row, column)
                        if self.rules.get_valid_move(self.board.grid, 1) == []:
                            self.turn = 2
                        else:
                            self.turn = 1

                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                # drawing a board
                self.board.draw()
                pygame.display.flip()

if __name__ == "__main__":
    Game()
