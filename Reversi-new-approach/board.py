import pygame, json
import reversi_func as f
import Rectangle as r
from statistics import mean

lines = (0, 0, 0)
black = (20, 20, 20)
white = (255, 255, 255)
green = (0, 170, 50)
peach = (200, 150, 100)
active = (190, 180, 25)
d_grey = (50, 50, 50)


class Board:

    def __init__(self, game):
        self.game = game
        self.margin = 5
        self.cell_size = 50
        self.grid_size = self.game.grid_size
        self.grid = [[0 for x in range(self.grid_size)] for y in range(self.grid_size)]
        self.winner = None
        # starting positions
        a = int(self.grid_size/2-1)
        b = int(self.grid_size/2)

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

        self.game.screen_width = self.grid_size * (self.cell_size + self.margin) + self.margin
        self.game.screen_height = self.grid_size * (
                self.cell_size + self.margin) + 50 + self.margin

        # centering game window
        f.center_window(self.game)

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
        self.game_end()


    def print_score(self):
        black = self.game.score[1]
        white = self.game.score[2]
        font = pygame.font.Font("freesansbold.ttf", 20)

        scoreboard_b = r.Rectangle(self.game.screen, 0, 0, self.game.screen_width/2, 50, d_grey)
        scoreboard_w = r.Rectangle(self.game.screen, self.game.screen_width / 2, 0,
                                   self.game.screen_width / 2, 50, d_grey)

        scoreboards = [scoreboard_w, scoreboard_b]

        for scoreboard in scoreboards:
            scoreboard.draw_rect()
            if scoreboard == scoreboard_b:
                text_surface, text_rect = f.text_objects("Black: " + str(black), font, (255, 255, 255))
                text_rect.center = (scoreboard.left + scoreboard.width / 2), (scoreboard.top + scoreboard.height / 2)
                self.game.screen.blit(text_surface, text_rect)
            if scoreboard == scoreboard_w:
                text_surface, text_rect = f.text_objects("White: " + str(white), font, (255, 255, 255))
                text_rect.center = (scoreboard.left + scoreboard.width / 2), (scoreboard.top + scoreboard.height / 2)
                self.game.screen.blit(text_surface, text_rect)

        if self.game.turn == 1:
            r.Rectangle(self.game.screen, 10, 40, self.game.screen_width/2 - 20, 5, active).draw_rect()
        else:
            r.Rectangle(self.game.screen, self.game.screen_width / 2 + 10, 40,
                        self.game.screen_width / 2 - 20, 5, active).draw_rect()

    def game_end(self):
        black = self.game.score[1]
        white = self.game.score[2]
        font = pygame.font.Font("freesansbold.ttf", int(self.game.screen_height * 0.1))
        if self.game.rules.get_valid_move(self.game.board.grid, 1) == [] and \
                self.game.rules.get_valid_move(self.game.board.grid, 2) == []:
            box = r.Rectangle(self.game.screen, self.game.screen_width * 0.1, self.game.screen_height * 0.2 + 25,
                              self.game.screen_width*0.8, self.game.screen_height * 0.6, (180, 150, 0))
            box.draw_rect()

            if black > white:
                winner = "Black wins!"
                self.winner = "Black"
            elif black < white:
                winner = "White wins!"
                self.winner = "White"
            else:
                winner = "It's a draw!"
                self.winner = "Draw"

            text_surface, text_rect = f.text_objects(winner, font, (255, 255, 255))
            text_rect.center = (box.left + box.width / 2), (box.top + box.height / 2)
            self.game.screen.blit(text_surface, text_rect)
            #pygame.display.update()

            # to be deleted on menu version
            self.game.game_status = False

    def save_game_info(self):
        if self.winner:
            with open('games_results.json', 'r+') as results:
                game_info = json.load(results)
                results.close()
                game_info["results"].append({
                    "player_1": {
                        "player_type": self.game.player_1_type[:self.game.player_1_type.index("(")],
                        "minmax_dept_of_search": self.game.player_1.depth_of_search,
                        "montecarlo_iter_max": self.game.player_1.iter_max,
                        "avg_move_time": mean(self.game.p_1_move_times),
                        "total_time": sum(self.game.p_1_move_times)},
                    "player_2": {
                        "player_type": self.game.player_2_type[:self.game.player_2_type.index("(")],
                        "minmax_dept_of_search": self.game.player_2.depth_of_search,
                        "montecarlo_iter_max": self.game.player_2.iter_max,
                        "avg_move_time": mean(self.game.p_2_move_times),
                        "total_time": sum(self.game.p_2_move_times)},
                    "board_size": self.grid_size,
                    "score": self.game.score,
                    "winner": self.winner
                })
            with open('games_results.json', 'w+') as results:
                results.write(json.dumps(game_info, indent=3))

