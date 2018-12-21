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
        self.close = False
        self.game_status = False
        #self.menu = Menu(self)
        # grid's cell size
        self.grid_size = 0

        # program loop
        while not self.close:
            self.turn = 1
            self.menu = Menu(self)
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
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # choosing settings
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

            # initialize board with chosen size
            self.board = Board(self)
            self.rules = Rules(self)

            # game loop
            while self.game_status:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

                while pygame.QUIT not in [event.type for event in pygame.event.get()] \
                        and not pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.score = self.rules.getScoreOfBoard(self.board.grid)
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

                    if isinstance(self.player_1, Human):
                        if pygame.mouse.get_pressed()[0] == 1 and self.turn == 1 and self.rules.is_valid_move(self.board.grid, 1, column, row):
                            self.player_1.make_a_move(row, column)
                            if self.rules.get_valid_move(self.board.grid, 2) == []:
                                self.turn = 1
                            self.turn = 2

                    if not isinstance(self.player_1, Human):
                        if self.turn == 1:
                            self.player_1.make_a_move(row, column)
                            if self.rules.get_valid_move(self.board.grid, 2) == []:
                                self.turn = 1
                            self.turn = 2

                    if isinstance(self.player_2, Human):
                        if pygame.mouse.get_pressed()[0] == 1 and self.turn == 2 and self.rules.is_valid_move(self.board.grid, 2, column, row):
                            self.player_2.make_a_move(row, column)
                            if self.rules.get_valid_move(self.board.grid, 1) == []:
                                self.turn = 2
                            self.turn = 1

                    if not isinstance(self.player_2, Human):
                        if self.turn == 2:
                            self.player_2.make_a_move(row, column)
                            if self.rules.get_valid_move(self.board.grid, 1) == []:
                                self.turn = 2
                            self.turn = 1

                    # getting a score
                    self.score = self.rules.getScoreOfBoard(self.board.grid)
                    self.board.draw()
                    pygame.display.flip()

                #after closing single game -> back to menu
                self.game_status = False
                self.menu.state = True


if __name__ == "__main__":
    Game()
