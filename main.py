import pygame
from random import *
pygame.init()

def switchWall():
    coords = pygame.mouse.get_pos()
    mx = coords[0]
    my = coords[1]
    mx = int(mx / 32)
    my = int(my / 32)
    background[my][mx] = switchWallStatus
    return

def getStartPoint():
    startX = -1
    startY = -1
    for i, backgroundRow in enumerate(background):
        for j, tile in enumerate(backgroundRow):
            if background[i][j] == 0:
                startX = j
                startY = i
                pygame.draw.rect(win, (255,255,255), (j * 32 + 12, i * 32 + 12, 8, 8))
                return startX, startY
    return

def connected(x,y):
    visitedBackground.append((x,y))
    if x >= 0 and x < tilesX and y >= 0 and y < tilesY:
        for i in range(-1, 2):
            neighborX = x + i
            if neighborX >= 0 and neighborX < tilesX:
                for j in range (-1, 2):
                    neighborY = y + j
                    if neighborY >= 0 and neighborY < tilesY:
                        if background[neighborY][neighborX] == 0 and not (neighborX,neighborY) in visitedBackground:
                            if not (i == 0 and j == 0):
                                pygame.draw.rect(win, (100,255,100), (neighborX * 32 + 12, neighborY * 32 + 12, 8, 8))
                                connected(neighborX, neighborY)
    return

def createBackground():
    background = []
    for i in range(tilesY):
        backgroundRow = []
        for j in range(tilesX):
            backgroundRow.append(1)
        background.append(backgroundRow)
    roomNumber = randint(3,7)

    for i in range(roomNumber):
        roomX = randint(0, tilesX-1)
        roomY = randint(0, tilesY-1)
        roomWidth = randint(2,8)
        roomHeight = randint(2,6)
        background[roomY][roomX] = 0
        for j  in range(roomHeight):
            if(roomY + j >= 0 and roomY + j < tilesY):
                for k in range(roomWidth):
                    if(roomX + k >= 0 and roomX + k < tilesX):
                        background[roomY + j][roomX + k] = 0
    return background

def update():
    win.fill(background_colour)
    for i, backgroundRow in enumerate(background):
        for j, tile in enumerate(backgroundRow):
            if(tile == 0):
                win.blit(dirt, (j * 32, i * 32))
            elif(tile == 1):
                win.blit(wall, (j * 32, i * 32))
            pass
        pass
    startX, startY = getStartPoint()
    connected(startX, startY)
    pygame.display.flip()
    return 1

switchWallStatus = 0

width = 1024
height = 768
tilesX = int(width / 32)
tilesY = int(height / 32)
background_colour = (255,255,255)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gnome")
win.fill(background_colour)

# Load sprites
dirt = pygame.image.load("map/grey_dirt0.png").convert()
wall = pygame.image.load("map/stone2_gray0.png").convert()

background = createBackground()
visitedBackground = []

pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F1:
                background = createBackground()
            if event.key == pygame.K_f:
                switchWallStatus = not switchWallStatus
        if pygame.mouse.get_pressed()[0]:
            switchWall()
    visitedBackground = []
    update()
pygame.quit()
