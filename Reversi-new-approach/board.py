import pygame
import reversi_func as f
import Rectangle as r
import os

lines = (0, 0, 0)
black = (20, 20, 20)
white = (255, 255, 255)
green = (0, 170, 50)
peach = (200, 150, 100)


class Board:

    def __init__(self, game):
        self.game = game
        self.margin = 5
        self.cell_size = 50
        self.grid_size = self.game.grid_size
        self.grid = [[0 for x in range(self.grid_size)] for y in range(self.grid_size)]
        # starting positions
        a = int(self.grid_size/2-1)
        b = int(self.grid_size/2)

        self.grid[a][a] = 1
        self.grid[a][b] = 2
        self.grid[b][a] = 2
        self.grid[b][b] = 1

    def draw(self):
        self.game.screen.fill(lines)

        # re-size cells to fit the window
        if self.game.grid_size > 12:
            self.cell_size = int(660/(1.1 * self.game.grid_size))
            self.margin = int(0.1 * self.cell_size)
        else:
            self.cell_size = 50
            self.margin = 5

        self.game.screen_width = self.grid_size * (self.cell_size + self.margin) + self.margin
        self.game.screen_height = self.grid_size * (
                self.cell_size + self.margin) + 50 + self.margin

        # centering game window
        x = (self.game.screen_resolution_w - self.game.screen_width) / 2
        y = (self.game.screen_resolution_h - self.game.screen_height) / 2 + 10
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        self.game.screen = pygame.display.set_mode((self.game.screen_width, self.game.screen_height))

        for row in range(self.grid_size):
            for column in range(self.grid_size):
                if self.grid[row][column] == 1:
                    color = black
                elif self.grid[row][column] == 2:
                    color = white
                elif self.grid[row][column] == 3:
                    color = peach
                else:
                    color = green
                pygame.draw.rect(self.game.screen, color, [self.margin + (self.margin + self.cell_size) * column,
                                                           self.margin + 50 + (self.margin + self.cell_size) * row,
                                                           self.cell_size, self.cell_size])
        self.print_score()
        self.game_end()

    def print_score(self):
        black = self.game.score[1]
        white = self.game.score[2]
        font = pygame.font.Font("freesansbold.ttf", 20)
        #print("Black: " + str(black), "White: " + str(white))

        scoreboard_b = r.Rectangle(self.game.screen, 0, 0, self.game.screen_width/2, 50, (180, 150, 0))
        scoreboard_w = r.Rectangle(self.game.screen, self.game.screen_width / 2, 0,
                                   self.game.screen_width / 2, 50, (50, 50, 50))

        scoreboards = [scoreboard_w, scoreboard_b]

        for scoreboard in scoreboards:
            scoreboard.drawRect()
            if scoreboard == scoreboard_b:
                textSurface, textRect = f.text_objects("Black: " + str(black), font, (255,255,255))
                textRect.center = (scoreboard.left + scoreboard.width / 2), (scoreboard.top + scoreboard.height / 2)
                self.game.screen.blit(textSurface, textRect)
            if scoreboard == scoreboard_w:
                textSurface, textRect = f.text_objects("White: " + str(white), font, (255, 255, 255))
                textRect.center = (scoreboard.left + scoreboard.width / 2), (scoreboard.top + scoreboard.height / 2)
                self.game.screen.blit(textSurface, textRect)

    def game_end(self):
        black = self.game.score[1]
        white = self.game.score[2]
        font = pygame.font.Font("freesansbold.ttf", int(self.game.screen_height * 0.1))
        if self.game.rules.get_valid_move(self.game.board.grid, 1) == [] and \
                self.game.rules.get_valid_move(self.game.board.grid, 2) == []:
            box = r.Rectangle(self.game.screen, self.game.screen_width*0.1, self.game.screen_height*0.2+25,
                              self.game.screen_width*0.8, (self.game.screen_height)*0.6, (180, 150, 0))
            box.drawRect()

            if black > white:
                winner = "Black"
            else:
                winner = "White"

            textSurface, textRect = f.text_objects(winner + " wins!", font, (255, 255, 255))
            textRect.center = (box.left + box.width / 2), (box.top + box.height / 2)
            self.game.screen.blit(textSurface, textRect)
