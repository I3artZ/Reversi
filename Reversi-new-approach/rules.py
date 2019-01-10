import copy
import pygame


# game rules
class Rules:

    def __init__(self, game):
        self.game = game

    def is_on_board(self, x, y):
        # Returns True if the coordinates are located on the board.
        return 0 <= x <= (self.game.grid_size-1) and 0 <= y <= (self.game.grid_size-1)

    def is_valid_move(self, grid, tile, x_start, y_start):
        if grid[y_start][x_start] == 1 or grid[y_start][x_start] == 2 or not self.is_on_board(x_start, y_start):
            return False

        if tile == 2:
            other_tile = 1
        else:
            other_tile = 2

        tiles_to_flip = []
        for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = x_start, y_start
            x += x_direction  # first step in the direction
            y += y_direction  # first step in the direction
            if self.is_on_board(x, y) and grid[y][x] == other_tile:
                # There is a piece belonging to the other player next to our piece.
                x += x_direction
                y += y_direction
                if not self.is_on_board(x, y):
                    continue
                while grid[y][x] == other_tile:
                    x += x_direction
                    y += y_direction
                    if not self.is_on_board(x, y):  # break out of while loop, then continue in for loop
                        break
                if not self.is_on_board(x, y):
                    continue
                if grid[y][x] == tile:
                    # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                    while True:
                        x -= x_direction
                        y -= y_direction
                        if x == x_start and y == y_start:
                            break
                        tiles_to_flip.append([x, y])

        grid[y_start][x_start] = 0  # restore the empty space
        if len(tiles_to_flip) == 0:  # If no tiles were flipped, this is not a valid move.
            return False
        return tiles_to_flip

    def get_valid_move(self, grid, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        valid_moves = []
        for x in range(self.game.grid_size):
            for y in range(self.game.grid_size):
                if self.is_valid_move(grid, tile, x, y):
                    valid_moves.append([x, y])
        return valid_moves

    def make_move(self, grid, tile, x_start, y_start):
        # Place the tile on the board at x start, y start, and flip any of the opponent's pieces.
        # Returns False if this is an invalid move, True if it is valid.
        tiles_to_flip = self.is_valid_move(grid, tile, x_start, y_start)
        if tiles_to_flip == False:
            return False
        grid[y_start][x_start] = tile
        for x, y in tiles_to_flip:
            grid[y][x] = tile
        return True
    
    def getScoreOfBoard(self, board):
    # Determine the score by counting the tiles. Returns a dictionary with keys '1' and '2'.
    # We should add our heuristics here

        heuristics = [self.points_for_tiles(board), self.points_for_position(board)]
                     #self.points_for_stability(board)]
        whites = (0.33 * heuristics[0][1] + 0.33 * heuristics[1][1])
        blacks = (0.33 * heuristics[0][2] + 0.33 * heuristics[1][2])

        return {1: whites, 2: blacks}

    def IsTerminalNode(self, player):
        possible_moves = self.get_valid_move(self.game.board.grid, player)
        if possible_moves.__len__ == 0:
            return False
        return True

    def points_for_tiles(self, board):
        whites = 0
        blacks = 0
        grid_size = self.game.grid_size

        for x in range(grid_size):
            for y in range(grid_size):
                if board[y][x] == 1:
                    whites += 1
                if board[y][x] == 2:
                    blacks += 1
        return {1: whites, 2: blacks}

    def points_for_position(self, board):
        whites = 0
        blacks = 0
        grid_size = self.game.grid_size
        grid_points = [[0 for x in range(grid_size)] for y in range(grid_size)]

        for x in range(grid_size):
            for y in range(grid_size):
                # a / corners +3
                if (x == 0 and y == grid_size - 1) or (x == grid_size - 1 and y == 0) or (y == 0 and x == 0) or (
                        y == grid_size - 1 and x == grid_size - 1):
                    grid_points[y][x] = 3

                # b corners neighbors -1
                if (x == 1 and y == grid_size - 1) or (x == 1 and y == 0) or \
                        (x == grid_size - 2 and y == 0) or (x == grid_size - 2 and y == grid_size - 1) or \
                        (y == 1 and x == grid_size - 1) or (y == 1 and x == 0) or \
                        (y == grid_size - 2 and x == 0) or (y == grid_size - 2 and x == grid_size - 1):
                    grid_points[y][x] = -2

                # c / worst place -3
                if (x == 1 and y == grid_size - 2) or (x == grid_size - 2 and y == 1) or (y == 1 and x == 1) or (
                        y == grid_size - 2 and x == grid_size - 2):
                    grid_points[y][x] = -3

                # d +1
                if (x == 0 and 1 < y < grid_size - 2) or (x == grid_size - 1 and 1 < y < grid_size - 2) or (
                        y == 0 and 1 < x < grid_size - 2) or (y == grid_size - 1 and 1 < x < grid_size - 2):
                    grid_points[y][x] = 1
                # e -1
                if (x == 1 and 1 < y < grid_size - 2) or (x == grid_size - 2 and 1 < y < grid_size - 2) or (
                        y == 1 and 1 < x < grid_size - 2) or (y == grid_size - 2 and 1 < x < grid_size - 2):
                    grid_points[y][x] = -1

        for x in range(grid_size):
            for y in range(grid_size):
                if board[y][x] == 1:
                    whites += grid_points[y][x]
                if board[y][x] == 2:
                    blacks += grid_points[y][x]

        return {1: whites, 2: blacks}


    def points_for_mobility(self, board, turn):
        scores = {}
        grid = copy.deepcopy(board)
        for x, y in self.get_valid_move(grid, turn):
            if turn == 1:
                self.make_move(grid, turn, x, y)
                scores[(x, y)] = len(self.get_valid_move(grid, 2))
                grid = copy.deepcopy(board)
            elif turn == 2:
                self.make_move(grid, turn, x, y)
                scores[(x, y)] = len(self.get_valid_move(grid, 1))
                grid = copy.deepcopy(board)

        return scores

    def points_for_stability(self, board):
        pass

    def get_game_state(self, game):
        pass

    '''def get_hints(self, board, turn):
        for x, y in self.game.rules.get_valid_move(board.grid, turn):
            board.grid[y][x] = 3

            pygame.draw.rect(self.game.screen, (200, 150, 100), [board.margin + (board.margin + board.cell_size) * y,
                                                                 board.margin + 50 + (board.margin + board.cell_size)
                                                                 * x, board.cell_size, board.cell_size])'''


