# -*- coding: utf8 -*-

import pygame, sys, lab as lab
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((520, 300), 0, 32)
pygame.display.set_caption('Outlier')

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
YELLOW= (255, 255,   0)
VIOLET= ( 255,  0, 255)

COLORS = [ BLUE, RED, BLACK, GREEN, YELLOW, VIOLET ]

DISPLAYSURF.fill(WHITE)

def drawSmirnov( z ):

    for i in range( len(z)): 
        c = COLORS[i]
        x = z[i]

        for d in range( len(x) ):
            p1 = ( x[d][0] / 100.0 + 10, 200 - x[d][1] * 10 )
            p2 = ( x[d][0] / 100.0 + 20, 200 - x[d][1] * 10 )

            pygame.draw.line(DISPLAYSURF, c, p1, p2)

            if d > 0:
                p1 = ( x[d][0] / 100.0 + 10, 200 - x[d-1][1] * 10 )
                p2 = ( x[d][0] / 100.0 + 10, 200 - x[d][1] * 10 )

                pygame.draw.line(DISPLAYSURF, c, p1, p2)

drawSmirnov(lab.Z)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()