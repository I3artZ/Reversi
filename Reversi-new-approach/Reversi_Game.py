import pygame
import reversi_func as f
from Rectangle import Rectangle as r

# some colors
BACK = (0, 0, 0)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 170, 50)
RED = (255, 0, 0)
MENU = (0, 135, 10)
GREY = (200, 200, 175)
DGREY = (215, 215, 190)

pygame.init()
title_font = pygame.font.SysFont("freesansbold.ttf",45)
menu_title = title_font.render("Hello to a game of Reversi!", True, WHITE)

#Size of screen(w,h)
size = (445, 445)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Reversi")

#cell and grid size
margin = 5
width = 50
height = 50
grid = [[0 for x in range(8)] for y in range(8)]

# flag - program ends after pressing close button.
close = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#mouse's button type
LEFT = 1
RIGHT = 3

#starting position
grid[3][3] = 1
grid[3][4] = 2
grid[4][3] = 2
grid[4][4] = 1
turn = 1 

# Game loop
menu = True

while not close:

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #starting a game
                if 50 < pos[0] < 395:
                    if 120 < pos[1] < 190:
                        menu = False

            screen.fill(MENU)
            screen.blit(menu_title, (25, 50))

            pos = pygame.mouse.get_pos()
            
            #making buttons
            rect_1 = r(screen, 50, 120, 345, 70, GREY)
            rect_1.drawRect()
            rect_2 = r(screen, 50, 200, 345, 70, GREY)
            rect_2.drawRect()
            rect_3 = r(screen, 50, 280, 345, 70, GREY)
            rect_3.drawRect()
            rect_4 = r(screen, 50, 360, 345, 70, GREY)
            rect_4.drawRect()
            
            #make it brighter!
            if  50 < pos[0] < 395: 
                if  120 < pos[1] < 190:
                    rect_1.color = DGREY
                    rect_1.drawRect()
                else:
                    rect_1.color = GREY
                    rect_1.drawRect()
                if 200 < pos[1] < 270:
                    rect_2.color = DGREY
                    rect_2.drawRect()
                else:
                    rect_2.color = GREY
                    rect_2.drawRect()
                if 280 < pos[1] < 350:
                    rect_3.color = DGREY
                    rect_3.drawRect()
                else:
                    rect_3.color = GREY
                    rect_3.drawRect()
                if 360 < pos[1] < 430:
                    rect_4.color = DGREY
                    rect_4.drawRect()
                else:
                    rect_4.color = GREY
                    rect_4.drawRect()

            smallText = pygame.font.Font("freesansbold.ttf", 20)


            textSurface, textRect = f.text_objects("Two players!", smallText)
            textRect.center = ((50+345/2)), (120 + 70/2)
            screen.blit(textSurface, textRect)
            textSurface, textRect = f.text_objects("In progress...", smallText)
            textRect.center = ((50+345/2)), (200 + 70/2)
            screen.blit(textSurface, textRect)
            textSurface, textRect = f.text_objects("In progress...", smallText)
            textRect.center = ((50+345/2)), (280 + 70/2)
            screen.blit(textSurface, textRect)
            textSurface, textRect = f.text_objects("In progress...", smallText)
            textRect.center = ((50+345/2)), (360 + 70/2)
            screen.blit(textSurface, textRect)
            pygame.display.update()
            
    # Main event loop
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        column = pos[0] // (width + margin)
        row = pos[1] // (height + margin)

        # User did something
        if event.type == pygame.QUIT: # If user clicked close
            close = True # Flag to close the game

        # black turn
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and turn == 1 and f.isValidMove(grid, turn, column, row):
            # move prints
            print("Click ", pos, "Grid coordinates: ", column, row)
            f.makeMove(grid, 1, column, row)
            grid[row][column] = 1

            print("Whites:", f.count_points(grid)[1], "Blacks:",
                  f.count_points(grid)[0],)  # current score
            # printing possible moves for white
            print("Possible Whites's moves (x,y)", f.getValidMove(grid, 2))
            
            #changing a player
            if f.getValidMove(grid, 2) == []:
                turn = 1
            else: 
                turn = 2

        #white turn
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and turn == 2 and f.isValidMove(grid, turn, column, row):
            # moves prints
            print("Click ", pos, "Grid coordinates: ", column, row)
            f.makeMove(grid, 2, column, row)
            grid[row][column] = 2

            print("Whites:", f.count_points(grid)[1], "Blacks:",
                  f.count_points(grid)[0],) # current score
            print("Possible Black's moves (x,y)", f.getValidMove(grid, 1)) #printing possible moves for black

            #changing a player
            if f.getValidMove(grid, 1) == []:
                turn = 2
            else:
                turn = 1

    #updating the game board
    screen.fill(BACK)
    
    for row in range(8):
        for column in range(8):
            if grid[row][column] == 1:
                color = BLACK
            elif grid[row][column] == 2:
                color = WHITE
            else:
                color = GREEN
            pygame.draw.rect(screen, color, [margin + (margin + width) * column, margin + (margin + height) * row, width, height])

    if f.getValidMove(grid, 1) == [] and f.getValidMove(grid, 2) == []:
        rect_5 = r(screen, 30, 30, 385, 385, GREY)
        rect_5.drawRect()
        if f.count_points(grid)[1] >= f.count_points(grid)[0]:
            txt = "White wins!" 
            txt_2 =  "Whites: " + str(f.count_points(grid)[1]) + "Blacks: " + str(f.count_points(grid)[0])
        else:
            txt = "Black wins!" 
            '''txt_2 = "Whites: " + str(f.count_points(grid)[1]), "Blacks: " + str(f.count_points(grid)[0])'''
        textSurface, textRect = f.text_objects(txt, title_font)
        textRect.center = (30+384/2), (30+384/2)
        screen.blit(textSurface, textRect)
        '''textSurface, textRect = f.text_objects(txt_2, title_font)
        textRect.center = (80+384/2), (30+384/2)
        screen.blit(textSurface, textRect)'''
        pygame.display.update()
    pygame.display.flip()

    #Limit to 60 frames per second
    clock.tick(60)

print("Whites:", f.count_points(grid)[1], "Blacks:",
      f.count_points(grid)[0])  # final score
if f.count_points(grid)[1] >= f.count_points(grid)[0]:
    print("White wins!")
else:
    print("Black wins!")

pygame.quit()


