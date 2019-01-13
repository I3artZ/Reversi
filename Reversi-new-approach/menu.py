import pygame
import reversi_func as f
import Rectangle as r

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

        """self.rect_1 = r.Rectangle(screen, 50, 120, 160, 70, grey)
        self.rect_2 = r.Rectangle(screen, 50, 200, 160, 70, grey)
        self.rect_3 = r.Rectangle(screen, 50, 280, 160, 70, grey)
        self.rect_4 = r.Rectangle(screen, 50, 360, 160, 70, grey)
        self.rect_5 = r.Rectangle(screen, 235, 120, 160, 70, grey)
        self.rect_6 = r.Rectangle(screen, 235, 200, 160, 70, grey)
        self.rect_7 = r.Rectangle(screen, 235, 280, 160, 70, grey)
        self.rect_8 = r.Rectangle(screen, 235, 360, 160, 70, grey)
        # board size buttons
        self.rect_9 = r.Rectangle(screen, 430, 120, 90, 70, grey)
        self.rect_10 = r.Rectangle(screen, 430, 200, 90, 70, grey)
        self.rect_11 = r.Rectangle(screen, 430, 280, 90, 70, grey)
        self.rect_12 = r.Rectangle(screen, 430, 360, 90, 70, grey)
        self.rect_13 = r.Rectangle(screen, 545, 120, 90, 70, grey)
        self.rect_14 = r.Rectangle(screen, 545, 200, 90, 70, grey)
        self.rect_15 = r.Rectangle(screen, 545, 280, 90, 70, grey)
        self.rect_16 = r.Rectangle(screen, 545, 360, 90, 70, grey)"""
        # play button
        self.rect_17 = r.Rectangle(screen, 660, 200, 90, 150, grey)
        self.rects = [getattr(self, "rect_" + str(i)) for i in range(1, 18)]
        """self.rects = [self.rect_1, self.rect_2, self.rect_3, self.rect_4, self.rect_5, self.rect_6, self.rect_7,
                      self.rect_8, self.rect_9, self.rect_10, self.rect_11, self.rect_12, self.rect_13, self.rect_14,
                      self.rect_15, self.rect_16, self.rect_17]"""
        self.player_1 = self.rects[0:4]
        self.player_2 = self.rects[4:8]
        self.board_size = self.rects[8:16]

    def draw(self):
        # draw menu buttons and assign properties to them
        # settings fonts
        title_font = pygame.font.SysFont("freesansbold.ttf", 45, True)
        small_text = pygame.font.Font("freesansbold.ttf", 20)
        # rendering welcoming msg
        menu_title = title_font.render("Welcome to a game of Othello!", False, white)
        menu_subtitle = small_text.render("Choose your settings", False, black)
        self.game.screen.blit(menu_title, (150, 40))
        self.game.screen.blit(menu_subtitle, (300, 85))

        for i in range(1, 18):
            rect = getattr(self, "rect_" + str(i))
            rect.draw_rect()

            if i == 1 or i == 5:
                rect.player_type = 'Human'
            if i == 2 or i == 6:
                rect.player_type = 'Minmax'
            if i == 3 or i == 7:
                rect.player_type = 'Monte Carlo'
            if i == 4 or i == 8:
                rect.player_type = 'In progess'
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

        for rect in self.player_2:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + \
                    rect.height:
                for i in self.player_2:
                    i.pressed = False
                rect.pressed = True

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
