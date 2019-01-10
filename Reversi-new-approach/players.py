import random
import copy
import datetime
from math import log, sqrt


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
        self.min_eval_board = 0
        self.max_eval_board = 1
        self.depth_of_search = 2

    def Minimax(self, board, player, depth, maximizing_player):
        if depth == 0 or not self.game.rules.IsTerminalNode(player):
            return self.game.rules.getScoreOfBoard(board)[player]
        possible_moves = self.game.rules.get_valid_move(board, player)
        # randomize the order of the possible moves
        random.shuffle(possible_moves)
        if maximizing_player:
            best_value = self.max_eval_board
            for y, x in possible_moves:
                #dupe_board = self.game.board.grid.copy()
                dupe_board = copy.deepcopy(board)
                #print(dupe_board)
                points_for_mobility = self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x]
                self.game.rules.make_move(dupe_board, player, y, x)
                v = self.Minimax(dupe_board, player, depth - 1, False) - 0.1 * points_for_mobility
                best_value = max(best_value, v)
                #print(best_value)
        else:  # minimizingPlayer
            best_value = self.min_eval_board
            for y, x in possible_moves:
                #  dupe_board = self.game.board.grid.copy()
                dupe_board = copy.deepcopy(board)
                #print(dupe_board)
                points_for_mobility = self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x]
                self.game.rules.make_move(dupe_board, player, y, x)
                v = self.Minimax(dupe_board, player, depth - 1, True) - 0.33 * points_for_mobility
                best_value = min(best_value, v)
                #print(best_value)
        return best_value

        '''if depth == 0 or self.game.rules.IsTerminalNode(player):
            return self.game.rules.getScoreOfBoard(board)[player]
        possible_moves = self.game.rules.get_valid_move(board, player)
        # randomize the order of the possible moves
        # random.shuffle(possible_moves)
        if maximizing_player:
            best_value = self.min_eval_board
            for y, x in possible_moves:
                # dupe_board = self.game.board.grid.copy()
                dupe_board = copy.deepcopy(self.game.board.grid)
                self.game.rules.mak
                e_move(dupe_board, player, y, x)
                v = self.Minimax(dupe_board, player, depth - 1, False) - 0.1 * (
                    self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x])
                best_value = max(best_value, v)
        else:  # minimizingPlayer
            best_value = self.max_eval_board
            for y, x in possible_moves:
                #  dupe_board = self.game.board.grid.copy()
                dupe_board = copy.deepcopy(self.game.board.grid)
                self.game.rules.make_move(dupe_board, player, y, x)
                v = self.Minimax(dupe_board, player, depth - 1, True) - 0.1 * (
                    self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x])
                best_value = min(best_value, v)
        return best_value'''


    def make_a_move(self, *args):
        # called from game
        possible_moves = self.game.rules.get_valid_move(self.game.board.grid, self.player)
        # randomize the order of the possible moves
        random.shuffle(possible_moves)
        # Go through all the possible moves and remember the best scoring move
        best_score = -10000
        if possible_moves:
            #  assigning bestY and X to first possible move
            best_y = possible_moves[0][0]
            best_x = possible_moves[0][1]
            #  check for better move
            for y, x in possible_moves:
                #print("current:", y, x)
                #print(possible_moves)
                dupe_board = copy.deepcopy(self.game.board.grid)
                #print(self.game.rules.points_for_mobility(dupe_board, 2))
                #score = self.Minimax(dupe_board, self.player, self.depth_of_search, True) - 0.1 * (self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x])
                points_for_mobility = self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x]
                self.game.rules.make_move(dupe_board, self.player, y, x)
                score = self.Minimax(dupe_board, self.player, self.depth_of_search, True) - 0.1 * points_for_mobility
                #print(score)
                if score > best_score:
                    best_y = y
                    best_x = x
                    best_score = score
                #print("best score", best_score)
                #print("best move", best_y, best_x)
            self.game.rules.make_move(self.game.board.grid, self.player, best_y, best_x)
            return best_y, best_x
        pass


class MonteCarlo:
    # in progress
    def __init__(self, game, player, **kwargs):  # game instead of board
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.game = game
        self.player = player

        '''self.states = []
        seconds = kwargs.get('time', 30)  # default 30 sec
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get("max_moves", 100)  # default 100 moves

        self.wins = {}
        self.plays = {}

        self.C = kwargs.get('C', 1.4)  # default C = 1.4'''

    def make_a_move(self):
        pass













    '''def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.states[-1]
        #player = self.board.current_player(state)
        player = self.game.turn
        legal = self.game.board.legal_plays(self.states[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(p, self.game.board.next_state(state, p)) for p in legal]

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        print(games, datetime.datetime.utcnow()-begin)
        # Pick the move with the highest percentage of wins.

        percent_wins, move = max(
            (self.wins.get((player, S), 0) / self.plays.get((player, S), 1), p) for p, S in moves_states)

        # Display the stats for each possible play.
        for x in sorted(
                ((100 * self.wins.get((player, S), 0) /
                  self.plays.get((player, S), 1),
                  self.wins.get((player, S), 0),
                  self.plays.get((player, S), 0), p)
                 for p, S in moves_states),
                reverse=True):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        print(move)
        return move

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        #player = self.board.current_player(state)
        player = self.game.turn

        expand = True
        for i in range(1, self.max_moves + 1):
            legal = self.game.board.legal_plays(states_copy)
            moves_states = [(p, self.game.board.next_state(state, p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = random.choice(moves_states)

            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.

            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if i > self.max_depth:
                    self.max_depth = i

            visited_states.add((player, state))

            # player = self.board.current_player(state)
            player = self.game.turn
            winner = self.game.board.winner(states_copy)
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] += 1'''
