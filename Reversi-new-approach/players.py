import random
import copy
import datetime
from math import log, sqrt


class Human:
    """ human player """
    def __init__(self, game, player, **kwargs):
        self.game = game
        self.player = player
        setattr(self.game.menu, "player_" + str(player) + "_iter_max", None)
        setattr(self.game.menu, "player_" + str(player) + "_depth_of_search", None)

    def make_a_move(self, row, column):
            self.game.rules.make_move(self.game.board.grid, self.player, column, row)
            self.game.board.grid[row][column] = self.player


class MinMax:
    """ player using Minmax algorithm """
    def __init__(self, game, player, depth_of_search=3, **kwargs):
        self.game = game
        self.player = player
        self.min_eval_board = float('inf')
        self.max_eval_board = -float('inf')
        self.depth_of_search = depth_of_search
        #print(self.depth_of_search)

    def minmax(self, board, player, depth, maximizing_player):
        if depth == 0 or self.game.rules.is_terminal_node(player):
            return self.game.rules.get_score_of_board(board)[player]
        possible_moves = self.game.rules.get_valid_move(board, player)

        # randomize the order of the possible moves
        random.shuffle(possible_moves)

        if maximizing_player:
            best_value = self.max_eval_board
            for y, x in possible_moves:
                dupe_board = copy.deepcopy(board)
                points_for_mobility = self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x]
                self.game.rules.make_move(dupe_board, player, y, x)
                v = self.minmax(dupe_board, player, depth - 1, False) + points_for_mobility
                best_value = max(best_value, v)
        else:  # minimizingPlayer
            best_value = self.min_eval_board
            for y, x in possible_moves:
                dupe_board = copy.deepcopy(board)
                points_for_mobility = self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x]
                self.game.rules.make_move(dupe_board, player, y, x)
                v = self.minmax(dupe_board, player, depth - 1, True) + points_for_mobility
                best_value = min(best_value, v)
        return best_value

    def make_a_move(self, *args):
        """chose and make a move"""
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
                #print(possible_moves)
                dupe_board = copy.deepcopy(self.game.board.grid)
                points_for_mobility = self.game.rules.points_for_mobility(dupe_board, self.game.turn)[y, x]
                self.game.rules.make_move(dupe_board, self.player, y, x)
                score = self.minmax(dupe_board, self.player, self.depth_of_search, True) + points_for_mobility
                if score > best_score:
                    best_y = y
                    best_x = x
                    best_score = score

            self.game.rules.make_move(self.game.board.grid, self.player, best_y, best_x)

            return best_y, best_x
        pass


class MonteCarlo:
    """ player using MCTS algorithm """
    def __init__(self, game, player, iter_max=1000, **kwargs):
        self.game = game
        self.player = player
        self.iter_max = iter_max

    def make_a_move(self, *args):
        node = self.Node(self.game, self.player)
        move = self.Node.uct(node, self.game, self.game.board.grid, self.player, 1000)
        if move:
            self.game.rules.make_move(self.game.board.grid, self.player, move[0], move[1])

    class Node:
        """ A node in the game tree. Win or lose from the viewpoint of current MCTS player. """
        def __init__(self, game, player, state=None, move=None, parent=None):
            self.game = game
            self.move = move  # the move which created new node
            self.parent_node = parent  # root_node doesn't have parent (None)
            self.child_nodes = []
            self.wins = 0
            self.visits = 0
            self.state = state  # board.grid (current state of board(board.grid))
            self.player = player
            # MCTS player (white or black) which is currently looking for a move
            if state is not None:
                self.untried_moves = self.game.rules.get_valid_move(self.state, self.player)  # future child nodes

        def uct_select_child(self):
            """ UCB1 formula used to vary the amount of exploration versus exploitation. C parameter = sqrt(2) """
            selected_node = sorted(self.child_nodes, key=lambda node: node.wins / node.visits + sqrt(2 * log(
                self.visits) / node.visits))[-1]  # self.visits = nr of visits in root_node = total num of simulations)
            return selected_node

        def add_child(self, chosen_move, new_state):
            """Removing chosen_move from untried_moves and adding a new child node for it. Return added child node"""
            new_node = MonteCarlo.Node(self.game, self.player, move=chosen_move, parent=self, state=new_state)
            self.untried_moves.remove(chosen_move)
            self.child_nodes.append(new_node)
            return new_node

        def uct(self, game, root_state, player, iter_max):
            """ UCT search for iter_max iterations starting from root_state. Return the best move from the root_state.
            Game result: 1: win, 0: lose"""
            root_node = MonteCarlo.Node(game, player, state=root_state)

            for i in range(iter_max):
                node = root_node
                state = copy.deepcopy(root_state)

                # Selection
                while node.untried_moves == [] and node.child_nodes != []:  # node is fully expanded and non-terminal
                    node = node.uct_select_child()
                    self.game.rules.make_move(state, self.player, node.move[0], node.move[1])

                # Expanding a tree
                if node.untried_moves:  # if we can expand (i.e. state/node is non-terminal)
                    move = random.choice(node.untried_moves)
                    self.game.rules.make_move(state, self.player, move[1], move[0])
                    node = node.add_child(move, state)  # add child and descend tree

                # Simulation
                self.run_simulation(state, self.player)

                # Backpropagation
                while node is not None:  # till root_node
                    node.update(self.get_result(state, self.player))  # state is terminal. Update nodes stats
                    node = node.parent_node  # update stats of each parent of terminal node

            if root_node.child_nodes:
                """ return the move that was most visited """
                return sorted(root_node.child_nodes, key=lambda node: node.visits)[-1].move

        def get_result(self, board, turn):
            """ return 1 if passed player win or 0 in case of lose """
            blacks = 0
            whites = 0
            for x in range(len(board)):
                for y in range(len(board[x])):
                    if board[y][x] == 1:
                        blacks += 1
                    if board[y][x] == 2:
                        whites += 1

            score = {1: blacks, 2: whites}

            if turn == 1 and score[1] > score[2]:
                return 1
            elif turn == 2 and score[2] > score[1]:
                return 1
            else:
                return 0

        def update(self, result):
            """ Updating stats win/visits for "used" nodes. Result from the viewpoint of mcts player """
            self.visits += 1
            self.wins += result

        def run_simulation(self, board, player):
            """ take random moves from chosen node until end of the game. Return result of the game win: 1, lose: 0 """
            dupe_board = copy.deepcopy(board)
            turn = player
            while self.game.rules.get_valid_move(dupe_board, turn):
                move = random.choice(self.game.rules.get_valid_move(dupe_board, turn))
                self.game.rules.make_move(dupe_board, turn, move[0], move[1])

                if turn == 1:
                    if self.game.rules.get_valid_move(dupe_board, 2):
                        turn = 2
                elif turn == 2:
                    if self.game.rules.get_valid_move(dupe_board, 1):
                        turn = 1

            return self.get_result(dupe_board, player)
