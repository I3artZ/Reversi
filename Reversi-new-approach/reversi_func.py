def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def isValidMove(grid, tile, xstart, ystart):
    if grid[ystart][xstart] == 1 or grid[ystart][xstart] == 2 or not isOnBoard(xstart, ystart):
        return False
    
    if tile == 2:
        otherTile = 1
    else:
        otherTile = 2

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if isOnBoard(x, y) and grid[y][x] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while grid[y][x] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):  # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if grid[y][x] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    grid[ystart][xstart] = 0  # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

    
def getValidMove(grid, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(grid, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def makeMove(grid, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(grid, tile, xstart, ystart)
    if tilesToFlip == False:
        return False

    grid[ystart][xstart] = tile
    for x, y in tilesToFlip:
        grid[y][x] = tile
    return True

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

def count_points(grid):
    whites = 0
    blacks = 0
    for i in grid:
        for z in i:
            if z == 1:
                blacks += 1
            elif z == 2:
                whites += 1
    return [blacks, whites]

