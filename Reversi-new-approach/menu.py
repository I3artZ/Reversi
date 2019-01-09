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

        # players buttons
        self.rect_1 = r.Rectangle(self.game.screen, 50, 120, 160, 70, grey)
        self.rect_2 = r.Rectangle(self.game.screen, 50, 200, 160, 70, grey)
        self.rect_3 = r.Rectangle(self.game.screen, 50, 280, 160, 70, grey)
        self.rect_4 = r.Rectangle(self.game.screen, 50, 360, 160, 70, grey)
        self.rect_5 = r.Rectangle(self.game.screen, 235, 120, 160, 70, grey)
        self.rect_6 = r.Rectangle(self.game.screen, 235, 200, 160, 70, grey)
        self.rect_7 = r.Rectangle(self.game.screen, 235, 280, 160, 70, grey)
        self.rect_8 = r.Rectangle(self.game.screen, 235, 360, 160, 70, grey)
        # board size buttons
        self.rect_9 = r.Rectangle(self.game.screen, 430, 120, 90, 70, grey)
        self.rect_10 = r.Rectangle(self.game.screen, 430, 200, 90, 70, grey)
        self.rect_11 = r.Rectangle(self.game.screen, 430, 280, 90, 70, grey)
        self.rect_12 = r.Rectangle(self.game.screen, 430, 360, 90, 70, grey)
        self.rect_13 = r.Rectangle(self.game.screen, 545, 120, 90, 70, grey)
        self.rect_14 = r.Rectangle(self.game.screen, 545, 200, 90, 70, grey)
        self.rect_15 = r.Rectangle(self.game.screen, 545, 280, 90, 70, grey)
        self.rect_16 = r.Rectangle(self.game.screen, 545, 360, 90, 70, grey)
        # ok button
        self.rect_17 = r.Rectangle(self.game.screen, 660, 200, 90, 150, grey)
        self.rects = [self.rect_1, self.rect_2, self.rect_3, self.rect_4, self.rect_5, self.rect_6, self.rect_7,
                      self.rect_8, self.rect_9, self.rect_10, self.rect_11, self.rect_12, self.rect_13, self.rect_14,
                      self.rect_15, self.rect_16, self.rect_17]
        self.player_1 = self.rects[0:4]
        self.player_2 = self.rects[4:8]
        self.board_size = self.rects[8:16]

    def draw(self):

        title_font = pygame.font.SysFont("freesansbold.ttf", 45)
        smallText = pygame.font.Font("freesansbold.ttf", 20)


        title_font = pygame.font.SysFont("freesansbold.ttf",45,True)
        smallText = pygame.font.Font("freesansbold.ttf", 20)

        menu_title = title_font.render("Hello to a game of Reversi!", False, white)
        menu_subtitle = smallText.render("Choose your settings", False, black)
        self.game.screen.blit(menu_title, (175, 40))
        self.game.screen.blit(menu_subtitle, (300, 85))

        for rect in self.rects:
            rect.drawRect()
            if rect == self.rect_1 or rect == self.rect_5:
                rect.player_type = 'human'
                textSurface, textRect = f.text_objects("Human", smallText)
            if rect == self.rect_2 or rect == self.rect_6:
                rect.player_type = 'minmax'
                textSurface, textRect = f.text_objects("Minmax", smallText)
            if rect == self.rect_3 or rect == self.rect_7:
                rect.player_type = 'monte carlo'
                textSurface, textRect = f.text_objects("Monte Carlo", smallText)
            if rect == self.rect_4 or rect == self.rect_8:
                rect.player_type = 'in progess'
                textSurface, textRect = f.text_objects("In progress...", smallText)
            if rect == self.rect_9:
                rect.size = 8
                textSurface, textRect = f.text_objects("8 x 8", smallText)
            if rect == self.rect_10:
                rect.size = 10
                textSurface, textRect = f.text_objects("10 x 10", smallText)
            if rect == self.rect_11:
                rect.size = 12
                textSurface, textRect = f.text_objects("12 x 12", smallText)
            if rect == self.rect_12:
                rect.size = 14
                textSurface, textRect = f.text_objects("14 x 14", smallText)
            if rect == self.rect_13:
                rect.size = 16
                textSurface, textRect = f.text_objects("16 x 16", smallText)
            if rect == self.rect_14:
                rect.size = 18
                textSurface, textRect = f.text_objects("18 x 18", smallText)
            if rect == self.rect_15:
                rect.size = 20
                textSurface, textRect = f.text_objects("20 x 20", smallText)
            if rect == self.rect_16:
                rect.size = 30
                textSurface, textRect = f.text_objects("30 x 30", smallText)
            if rect == self.rect_17:
                textSurface, textRect = f.text_objects("Play", smallText)

            textRect.center = (rect.left + rect.width / 2), (rect.top + rect.height / 2)
            self.game.screen.blit(textSurface, textRect)

    def highlight(self):
        # make it brighter!
        for rect in self.rects:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + rect.height:
                rect.color = l_grey
            elif rect.pressed:
                rect.color = yellow
            else:
                rect.color = grey

    def press_button(self):

        for rect in self.player_1:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + rect.height:
                for i in self.player_1:
                    i.pressed = False
                rect.pressed = True

        for rect in self.player_2:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + rect.height:
                for i in self.player_2:
                    i.pressed = False
                rect.pressed = True

        for rect in self.board_size:
            if rect.left < self.game.pos[0] < rect.width + rect.left and rect.top < self.game.pos[1] < rect.top + rect.height:
                for i in self.board_size:
                    i.pressed = False
                rect.pressed = True

        self.play()

    def play(self):
        pressed_keys = [1 for rect in self.rects if rect.pressed]
        if sum(pressed_keys) == 3 and self.rect_17.left < self.game.pos[0] < self.rect_17.width + self.rect_17.left:
            if self.rect_17.top < self.game.pos[1] < self.rect_17.top + self.rect_17.height:
                self.game.menu.state = False
                self.game.game_status = True


