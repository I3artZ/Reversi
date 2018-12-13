

class Human:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def make_a_move(self, row, column):
            # black turn
            # print(self.game.board.grid)
            # print(self.player)
            # print(column, row)
            self.game.rules.make_move(self.game.board.grid, self.player, column, row)
            self.game.board.grid[row][column] = self.player

            '''print("Whites:", f.count_points(grid)[1], "Blacks:",
                            f.count_points(grid)[0],)  # current score
                    # printing possible moves for white
                        print("Possible Whites's moves (x,y)", f.getValidMove(grid, 2))

                    # changing a player
                    if f.getValidMove(grid, 2) == []:
                        turn = 1
                    else:
                        turn = 2'''


class MinMax:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def make_a_move(self):
        pass


class MonteCarlo:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def make_a_move(self):
        pass

