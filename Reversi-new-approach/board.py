import pygame
lines = (0, 0, 0)
black = (20, 20, 20)
white = (255, 255, 255)
green = (0, 170, 50)


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
                else:
                    color = green
                pygame.draw.rect(self.game.screen, color, [self.margin + (self.margin + self.cell_size) * column, self.margin + (self.margin + self.cell_size) * row, self.cell_size, self.cell_size])
