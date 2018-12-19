import pygame

class Rectangle():
    def __init__(self, screen, left, top, width, height, color, pressed=False, player_type=None):
        self.left = left
        self.screen = screen
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.pressed = pressed
        self.player_type = player_type
        self.size = None

    def drawRect(self):
        pygame.draw.rect(self.screen, self.color, (self.left, self.top, self.width, self.height))

