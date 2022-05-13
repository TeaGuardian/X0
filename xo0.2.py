import pygame
from datetime import datetime, timedelta
pygame.init()
# version 0.2
k = True
win = False
quit = datetime.now()
sc = [150, 150, 150]
black = [255, 255, 255]
red = [150, 20, 20]
blue = [20, 20, 150]
size = [800, 1600]
screen = pygame.display.set_mode(size)
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()
d = [[[0, 100, 248, 398, sc], [250, 100, 248, 398, sc], [500, 100, 248, 398, sc]], [[0, 500, 248, 398, sc], [250, 500, 248, 398, sc], [500, 500, 248, 398, sc]], [[0, 900, 248, 398, sc], [250, 900, 248, 398, sc], [500, 900, 248, 398, sc]]]
titl = 'Сейчас ходят синие'
text = font.render(titl, True, blue)
titl2 = 'Сейчас ходят красные'
text2 = font.render(titl2, True, red)
textpos = (50, 50)
now = red
while k:
    
    screen.fill(sc)
    if now == blue:
        screen.blit(text, textpos)
    elif now == red:
        screen.blit(text2, textpos)
    pygame.draw.line(screen, black, [250, 100], [250, 1300], 5)
    pygame.draw.line(screen, black, [500, 100], [500, 1300], 5)
    pygame.draw.line(screen, black, [0, 500], [750, 500], 5)
    pygame.draw.line(screen, black, [0, 900], [750, 900], 5)
    
    for y in range(3):
        for x in range(3):
            pygame.draw.rect(screen, d[x][y][-1], ((d[x][y][0], d[x][y][1]), (d[x][y][2], d[x][y][3])))
    for event in pygame.event.get():
    	pos = pygame.mouse.get_pos()
    	if event.type == pygame.MOUSEBUTTONDOWN:
    	    if win:
    	        if (datetime.now() - quit) < timedelta(seconds=0.5):
    	            k = 0
    	        else:
    	            quit = datetime.now()
    	    for y in range(3):
    	        for x in range(3):
    	            if(d[x][y][0] < pos[0] < d[x][y][0] + d[x][y][2] and d[x][y][1] < pos[1] < d[x][y][1] + d[x][y][3]):
    	               if(d[x][y][-1] == sc):
    	                   d[x][y][-1] = now
    	                   if now == red:
    	                       now = blue
    	                   elif now == blue:
                               now = red
    for y in range(3):
        if d[0][y][-1] == d[1][y][-1] == d[2][y][-1]:
            if d[0][y][-1] == blue and win != 1:
                titl = 'Победили синие'
                win = 1
            elif d[0][y][-1] == red and win != 1:
                titl = 'Победили красные'
                win = 1
        elif d[y][0][-1] == d[y][1][-1] == d[y][2][-1]:
            if d[y][0][-1] == blue and win != 1:
                titl = 'Победили синие'
                win = 1
            elif d[y][0][-1] == red and win != 1:
                titl = 'Победили красные'
                win = 1
    if d[0][0][-1] == d[1][1][-1] == d[2][2][-1]:
        if d[0][0][-1] == blue and win != 1:
            titl = 'Победили синие'
            win = 1
        elif d[0][0][-1] == red and win != 1:
            titl = 'Победили красные'
            win = 1
            
    if d[2][0][-1] == d[1][1][-1] == d[0][2][-1]:
        if d[1][1][-1] == blue and win != 1:
            titl = 'Победили синие'
            win = 1
        elif d[1][1][-1] == red and win != 1:
            titl = 'Победили красные'
            win = 1
    if win:
        text = font.render(titl, True, [255, 215, 0])
        now = [255, 215, 0]
        screen.blit(text, textpos)
    pygame.display.flip()