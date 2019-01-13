
def text_objects(text, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()
