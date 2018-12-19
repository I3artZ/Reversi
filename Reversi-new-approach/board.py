import pygame
import reversi_func as f
import Rectangle as r

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
        a = int(len(self.grid)/2-1)
        b = int(len(self.grid)/2)

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

    def print_score(self):
        black = self.game.score[1]
        white = self.game.score[2]
        font = pygame.font.Font("freesansbold.ttf", 20)
        # print("Black: " + str(black), "White: " + str(white))

        if self.game.turn == 1:
            scoreboard_b = r.Rectangle(self.game.screen, 0, 0, self.game.screen_width/2, 50, (180, 150, 0))
            scoreboard_w = r.Rectangle(self.game.screen, self.game.screen_width/2, 0, self.game.screen_width / 2, 50, (50, 50, 50))
        if self.game.turn == 2:
            scoreboard_b = r.Rectangle(self.game.screen, 0, 0, self.game.screen_width / 2, 50, (50, 50, 50))
            scoreboard_w = r.Rectangle(self.game.screen, self.game.screen_width / 2, 0, self.game.screen_width / 2, 50,
                                       (180, 150, 0))
        a = [scoreboard_w, scoreboard_b]
        scoreboard_b.drawRect()
        scoreboard_w.drawRect()

        for rect in a:
            if rect == scoreboard_b:
                textSurface, textRect = f.text_objects("Black: " + str(black), font, (255,255,255))
                textRect.center = (rect.left + rect.width / 2), (rect.top + rect.height / 2)
                self.game.screen.blit(textSurface, textRect)
            if rect == scoreboard_w:
                textSurface, textRect = f.text_objects("White: " + str(white), font, (255, 255, 255))
                textRect.center = (rect.left + rect.width / 2), (rect.top + rect.height / 2)
                self.game.screen.blit(textSurface, textRect)
