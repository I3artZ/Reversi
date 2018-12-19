def text_objects(text, font, color=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def count_points(grid):
    whites = 0
    blacks = 0
    for i in grid:
        for z in i:
            if z == 1:
                blacks += 1
            elif z == 2:
                whites += 1
    return [blacks, whites]

