import random
import copy


class Human:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def make_a_move(self, row, column):
            self.game.rules.make_move(self.game.board.grid, self.player, column, row)
            self.game.board.grid[row][column] = self.player


class MinMax:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.minEvalBoard = -1 # min - 1
        self.maxEvalBoard = game.grid_size * game.grid_size + 4 * game.grid_size + 4 + 1 # max + 1
        self.DEPTHOFSEARCH = 10

    def Minimax(self,board, player, depth, maximizingPlayer):
        if depth == 0 or self.game.rules.IsTerminalNode(player):
            return self.game.rules.getScoreOfBoard(board)[player]
        possibleMoves = self.game.rules.get_valid_move(board,player)
        # randomize the order of the possible moves
        random.shuffle(possibleMoves)
        if maximizingPlayer:
            bestValue = self.minEvalBoard
            for y,x in possibleMoves:
                #dupeBoard = self.game.board.grid.copy()
                dupeBoard = copy.deepcopy(self.game.board.grid)
                self.game.rules.make_move(dupeBoard,player,y,x)
                v = self.Minimax(dupeBoard,player,depth - 1, False)
                bestValue = max(bestValue, v)
        else: # minimizingPlayer
            bestValue = self.maxEvalBoard
            for y,x in possibleMoves:
                #dupeBoard = self.game.board.grid.copy()
                dupeBoard = copy.deepcopy(self.game.board.grid)
                self.game.rules.make_move(dupeBoard,player,y,x)
                v = self.Minimax(dupeBoard,player,depth - 1, True)
                bestValue = min(bestValue, v)
        return bestValue

    def make_a_move(self,row,colum):
        possibleMoves = self.game.rules.get_valid_move(self.game.board.grid,self.player)
        # randomize the order of the possible moves
        random.shuffle(possibleMoves)
        # Go through all the possible moves and remember the best scoring move
        bestScore = -1
        for y,x in possibleMoves:
            #dupeBoard = self.game.board.grid.copy()
            dupeBoard = copy.deepcopy(self.game.board.grid)
            self.game.rules.make_move(dupeBoard, self.player, y, x)
            score = self.Minimax(dupeBoard,self.player,self.DEPTHOFSEARCH,True)
            if score > bestScore:
                #bestMove = [y, x]
                bestY = y
                bestX = x
                bestScore = score
        if possibleMoves:
            self.game.rules.make_move(self.game.board.grid, self.player, bestY, bestX)
        pass


class MonteCarlo:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def make_a_move(self):
        pass

