# -*- coding: utf8 -*-

import pygame, sys, lab
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((1000, 1000), 0, 32)
pygame.display.set_caption('Klasterization')

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
YELLOW= (255, 255,   0)
VIOLET= ( 255,  0, 255)

COLORS = [ BLUE, RED, BLACK, GREEN, YELLOW, VIOLET ]

DISPLAYSURF.fill(WHITE)

def drawKlasters( z ):

    for i in range( len(z)): 
        c = COLORS[i]
        x = z[i]

        for d in x:
            p = ( d[0] / 100, d[1] / 100 )
            pygame.draw.circle(DISPLAYSURF, c, p, 2, 0)

drawKlasters(lab.Z)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()