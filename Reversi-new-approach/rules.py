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
    
    def getScoreOfBoard(self,board):
    # Determine the score by counting the tiles. Returns a dictionary with keys '1' and '2'.
    # We should add our heuristics here
        xscore = 0
        oscore = 0
        for x in range(self.game.grid_size):
            for y in range(self.game.grid_size):
                if board[y][x] == 1:
                    xscore += 1
                if board[y][x] == 2:
                    oscore += 1
        return {1:xscore, 2:oscore}

    def IsTerminalNode(self, player):
        possibleMoves = self.get_valid_move(self.game.board.grid,player)
        if possibleMoves.__len__ == 0:
            return False
        return True
    
