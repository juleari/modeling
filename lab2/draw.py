# -*- coding: utf8 -*-

import pygame, sys, lab
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((1000, 1000), 0, 32)
pygame.display.set_caption('Triangulation')

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)

DISPLAYSURF.fill(WHITE)

def drawfinal(triangles):

    for t in triangles: 
        for e in triangles[t].es:
            pygame.draw.line(DISPLAYSURF, BLACK, e.p1, e.p2)
            pygame.draw.circle(DISPLAYSURF, BLUE, e.p1, 2, 0)
            pygame.draw.circle(DISPLAYSURF, BLUE, e.p2, 2, 0)

drawfinal(lab.triang())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()