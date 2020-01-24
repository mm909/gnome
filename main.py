import pygame
from map import *
from random import *
from settings import *

pygame.init()

def update():
    win.fill(background_colour)
    map.draw(win)
    pygame.display.flip()
    return

background_colour = (0,0,0)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gnome Dungeon")
win.fill(background_colour)

# Load sprites
dirt = pygame.image.load("map/grey_dirt0.png").convert()
wall = pygame.image.load("map/stone2_gray0.png").convert()

map = Map()

pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F1:
                map = Map()
            if event.key == pygame.K_f:
                map.switchWallStatus = not map.switchWallStatus
            if event.key == pygame.K_h:
                map.connectRooms()

        if pygame.mouse.get_pressed()[0]:
            map.switchWall()

    if pygame.key.get_pressed()[pygame.K_F2]:
        map.debug = True
    else:
        map.debug = False

    if pygame.key.get_pressed()[pygame.K_w]:
        map.cameraOffsetY += cameraSpeed
    if pygame.key.get_pressed()[pygame.K_a]:
        map.cameraOffsetX += cameraSpeed
    if pygame.key.get_pressed()[pygame.K_s]:
        map.cameraOffsetY -= cameraSpeed
    if pygame.key.get_pressed()[pygame.K_d]:
        map.cameraOffsetX -= cameraSpeed

    visitedBackground = []
    update()
pygame.quit()
