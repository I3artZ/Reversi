import pygame
import os


def text_objects(text, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def center_window(game):
    x = (game.screen_resolution_w - game.screen_width) / 2
    y = (game.screen_resolution_h - game.screen_height) / 2 + 10
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    game.screen = pygame.display.set_mode((game.screen_width, game.screen_height))
