class State:
    #  in progress/development to be considered
    def __init__(self, game):
        self.game = game


    def update(self, board, agent, opponent, agent_score, opponent_score):
        self.board = self.game.board.grid
        self.agent = self.game.turn
        self.opponent = opponent
        self.agent_score = agent_score
        self.opponent_score = opponent_score

def start(self):
        # Returns a representation of the starting state of the game.
        self.grid = [[0 for x in range(self.game.grid_size)] for y in range(self.game.grid_size)]
        # starting positions
        a = int(self.game.grid_size/2-1)
        b = int(self.game.grid_size/2)

        self.grid[a][a] = 1
        self.grid[a][b] = 2
        self.grid[b][a] = 2
        self.grid[b][b] = 1

    def current_player(self, state):

        pass

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        pass

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass'''