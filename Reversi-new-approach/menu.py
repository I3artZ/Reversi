import pygame
import reversi_func as f
import Rectangle as r
import pyautogui

# some colors definitions
grey = (180, 180, 155)
white = (255, 255, 255)
l_grey = (220, 220, 200)
black = (0, 0, 0)
yellow = (240, 190, 0)


class Menu:

    def __init__(self, game):
        self.game = game
        self.state = True
        screen = self.game.screen

        # players buttons
        # 1st player
        for i in range(1, 5):
            setattr(self, "rect_" + str(i), r.Rectangle(screen, 50, 120+(i-1)*80, 160, 70, grey))
        # 2nd player
        for i in range(5, 9):
            setattr(self, "rect_" + str(i), r.Rectangle(screen, 235, 120+(i-5)*80, 160, 70, grey))
        # board size
        for i in range(9, 13):
            setattr(self, "rect_" + str(i), r.Rectangle(screen, 430, 120+(i-9)*80, 90, 70, grey))
        # board size
        for i in range(13, 17):
            setattr(self, "rect_" + str(i), r.Rectangle(screen, 545, 120+(i-13)*80, 90, 70, grey))

        # play button
        self.rect_17 = r.Rectangle(screen, 660, 200, 90, 150, grey)
        self.rects = [getattr(self, "rect_" + str(i)) for i in range(1, 18)]

        self.player_1 = self.rects[:3]  # in progress button excluded
        self.player_2 = self.rects[4:7]  # in progress button excluded
        self.board_size = self.rects[8:16]

    def draw(self):
        # draw menu buttons and assign properties to them
        # settings fonts
        title_font = pygame.font.SysFont("freesansbold.ttf", 45, True)
        subtitle_font = pygame.font.SysFont("freesansbold.ttf", 35, True)
        small_text = pygame.font.Font("freesansbold.ttf", 20)
        little_text = pygame.font.Font("freesansbold.ttf", 15)
        # rendering welcoming msg
        menu_title = title_font.render("Welcome to a game of Othello!", False, white)
        menu_subtitle = subtitle_font.render("Choose your settings", False, black)
        column_name_1 = little_text.render("Player_1", False, black)
        column_name_2 = little_text.render("Player_2", False, white)
        column_name_3 = little_text.render("Board size", False, black)

        self.game.screen.blit(menu_title, (140, 20))
        self.game.screen.blit(menu_subtitle, (270, 55))
        self.game.screen.blit(column_name_1, (105, 95))
        self.game.screen.blit(column_name_2, (285, 95))
        self.game.screen.blit(column_name_3, (490, 95))

        for i in range(1, 18):
            rect = getattr(self, "rect_" + str(i))
            rect.draw_rect()

            if i == 1 or i == 5:
                rect.player_type = 'Human'
            if i == 2 or i == 6:
                rect.player_type = 'MinMax'
            if i == 3 or i == 7:
                rect.player_type = 'MonteCarlo'
            if i == 4 or i == 8:
                rect.player_type = 'In progress...'

            text_surface, text_rect = f.text_objects(rect.player_type, small_text)

            if i > 8:
                rect.size = 4 + (i-9)*2
                text_surface, text_rect = f.text_objects(str(rect.size) + "x" + str(rect.size), small_text)
            if rect == self.rect_17:
                text_surface, text_rect = f.text_objects("Play", small_text)

            text_rect.center = (rect.left + rect.width / 2), (rect.top + rect.height / 2)
            self.game.screen.blit(text_surface, text_rect)

    def highlight(self):
        # highlight button on which cursor is located
        for rect in self.rects:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + \
                    rect.height:
                rect.color = l_grey
            elif rect.pressed:
                rect.color = yellow
            else:
                rect.color = grey

    def press_button(self):
        # activate chosen button. From each button category only one can be activated.
        for rect in self.player_1:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + \
                    rect.height:
                for i in self.player_1:
                    i.pressed = False
                rect.pressed = True
                if rect.player_type == "MinMax" and rect.pressed:
                    input_value = pyautogui.prompt("BLACK player - chose depth (default=3): ",
                                                   "1st player | MinMax depth")

                    self.game.player_1_depth_of_search = input_value
                    self.game.player_1_iter_max = None

                if rect.player_type == "MonteCarlo" and rect.pressed:
                    input_value_2 = pyautogui.prompt(
                        "BLACK player - chose maximum number of iterations(default=1000): ",
                        "1st player | Monte Carlo max iterations")
                    self.game.player_1_iter_max = input_value_2
                    self.game.player_1_depth_of_search = None

        for rect in self.player_2:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + \
                    rect.height:
                for i in self.player_2:
                    i.pressed = False
                rect.pressed = True
                if rect.player_type == "MinMax" and rect.pressed:
                    input_value = pyautogui.prompt("WHITE player - chose depth (default=3): ",
                                                   "2nd player | MinMax depth")
                    self.game.player_2_depth_of_search = input_value
                    self.game.player_2_iter_max = None

                if rect.player_type == "MonteCarlo" and rect.pressed:
                    input_value = pyautogui.prompt(
                        "WHITE player - chose maximum number of iterations(default=1000) for 2nd player: ",
                        "2nd player | Monte Carlo max iterations")
                    self.game.player_2_iter_max = input_value
                    self.game.player_2_depth_of_search = None

        for rect in self.board_size:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + \
                    rect.height:
                for i in self.board_size:
                    i.pressed = False
                rect.pressed = True

        self.play()

    def play(self):
        # starting the game after clicking on play button if all settings have been chosen
        pressed_keys = [1 for rect in self.rects if rect.pressed]
        if sum(pressed_keys) == 3 and self.rect_17.left < self.game.pos[0] < self.rect_17.width + self.rect_17.left:
            if self.rect_17.top < self.game.pos[1] < self.rect_17.top + self.rect_17.height:
                self.game.menu.state = False
                self.game.game_status = True
                self.game.game_start()

