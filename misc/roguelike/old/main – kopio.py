import pygame
import numpy as np

pygame.init()

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('My Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)
ORANGE = (255, 140, 0)

SCREEN.fill(BLACK)
pygame.font.init()
F = pygame.font.SysFont('monospace',20)
Wall = F.render('#', False, ORANGE)
Player = F.render('@', False, WHITE)
xgrid = 10
ygrid = 20

playerpos = [xgrid*10,ygrid*20]


def update():
    SCREEN.fill(BLACK)
    for x in np.arange(0,WIDTH, xgrid):
        for y in range(0,HEIGHT, ygrid):
            if x == 0 or y == 0 or x == WIDTH-10 or y == HEIGHT-20:
                SCREEN.blit(Wall,(x,y))
            if x == playerpos[0] and y == playerpos[1]:
                SCREEN.blit(Player,(x,y))
            
    pygame.display.flip()

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.dict['key'] == pygame.K_KP6:
                # Move right
                playerpos[0] += xgrid*1
            if event.dict['key'] == pygame.K_KP4:
                # Move left
                playerpos[0] -= xgrid*1
            if event.dict['key'] == pygame.K_KP8:
                # Move up
                playerpos[1] -= ygrid*1
            if event.dict['key'] == pygame.K_KP2:
                # Move down
                playerpos[1] += ygrid*1
            if event.dict['key'] == pygame.K_KP9:
                playerpos[0] += xgrid*1
                playerpos[1] -= ygrid*1
            if event.dict['key'] == pygame.K_KP7:
                playerpos[0] -= xgrid*1
                playerpos[1] -= ygrid*1
            if event.dict['key'] == pygame.K_KP3:
                playerpos[0] += xgrid*1
                playerpos[1] += ygrid*1
            if event.dict['key'] == pygame.K_KP1:
                playerpos[0] -= xgrid*1
                playerpos[1] += ygrid*1
            
        if event.type == pygame.QUIT:
            is_running = False

        update()

pygame.quit()
