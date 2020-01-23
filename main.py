import pygame
from mapGenSettings import *
from random import *
pygame.init()

def getMouseCoords():
    coords = pygame.mouse.get_pos()
    mx = coords[0] - cameraOffsetX
    my = coords[1] - cameraOffsetY
    return mx, my

def switchWall():
    mx, my = getMouseCoords()
    print(mx,my)
    mx = int(mx / 32)
    my = int(my / 32)
    if my >= 0 and my < tilesY and mx >= 0 and mx < tilesX:
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
                pygame.draw.rect(win, (255,255,255), (j * 32 + 12 + cameraOffsetX, i * 32 + 12 + cameraOffsetY, 8, 8))
                return startX, startY
    return startX, startY

def findClusterPoint(): #will be used to find the next room to create a path too. the same as getStartPoint just didnt want to rename that function and change it a little without discussing first
    startX = -1
    startY = -1
    for i, backgroundRow in enumerate(background):
        for j, tile in enumerate(backgroundRow):
            if background[i][j] == 0 and not (j , i) in visitedBackground:
                startX = j
                startY = i
                pygame.draw.rect(win, (255,255,255), (j * 32 + 12 + cameraOffsetX, i * 32 + 12 + cameraOffsetY, 8, 8))
                return startX, startY
    return startX, startY

def connected(x,y):
    visitedBackground.append((x,y))
    if x >= 0 and x < tilesX and y >= 0 and y < tilesY:
        for i in range(-1, 2):
            neighborX = x + i
            if neighborX >= 0 and neighborX < tilesX:
                for j in range (-1, 2):
                    if i == 0 or j == 0:   #only does dfs on non-diagonal neighbors to stop diagonal only path connections if  (abs(i) != 1 or abs(j) != 1):
                        neighborY = y + j
                        if neighborY >= 0 and neighborY < tilesY:
                            if background[neighborY][neighborX] == 0 and not (neighborX,neighborY) in visitedBackground:
                                if not (i == 0 and j == 0):
                                    pygame.draw.rect(win, (100,255,100), (neighborX * 32 + 12 + cameraOffsetX, neighborY * 32 + 12 + cameraOffsetY, 8, 8))
                                    connected(neighborX, neighborY)
    return

def createBackground():
    background = []
    for i in range(tilesY):
        backgroundRow = []
        for j in range(tilesX):
            backgroundRow.append(1)
        background.append(backgroundRow)
    roomNumber = randint(roomMin,roomMax)


    offset = 0.05
    for i in range(roomNumber):
        roomX = randint(0 + int(tilesX*offset), tilesX-1 - int(tilesX * offset))
        roomY = randint(0 + int(tilesY*offset), tilesY-1 - int(tilesY * offset))
        roomWidth = randint(roomMinWidth, roomMaxWidth)
        roomHeight = randint(roomMinHeight, roomMaxHeight)
        background[roomY][roomX] = 0
        for j  in range(roomHeight):
            if(roomY + j >= 0 and roomY + j < tilesY):
                for k in range(roomWidth):
                    if(roomX + k >= 0 and roomX + k < tilesX):
                        background[roomY + j][roomX + k] = 0
    return background

def connectRooms():
    global visitedBackground
    visitedBackground = []
    startX, startY = getStartPoint()
    connected(startX, startY)
    endX, endY = findClusterPoint()
    while endX != -1 and endY != -1:
        #connected(endX, endY)
        createPath(startX, startY, endX, endY)
        endX, endY = findClusterPoint()
    return

def createPath(startX, startY, endX, endY):
    global visitedBackground
    dx = 0
    dy = 0

    slopeX = abs(startX - endX)
    slopeY = abs(startY - endY)

    if startX - endX < 0:
        dx = 1
    elif startX - endX > 0:
        dx = -1

    if startY - endY < 0:
        dy = 1
    elif startY - endY > 0:
        dy = -1

    #print(endX, endY)
    moveX = randint(0,1)
    currX = startX
    currY = startY
    while not (endX, endY) in visitedBackground:
        #visitedBackground = []
        if  moveX == True:
            if slopeX >0:
                currX = currX + dx
                background[currY][currX] = 0
                slopeX = slopeX - 1
                connected(currX, currY)
            else:
                moveX = False

        elif moveX == False:
            if slopeY > 0:
                currY = currY + dy
                background[currY][currX] = 0
                slopeY = slopeY - 1
                connected(currX, currY)
            else:
                moveX = True

    return

def update():
    win.fill(background_colour)
    for i, backgroundRow in enumerate(background):
        for j, tile in enumerate(backgroundRow):
            if(tile == 0):
                win.blit(dirt, (j * 32 + cameraOffsetX, i * 32 + cameraOffsetY))
            elif(tile == 1):
                win.blit(wall, (j * 32 + cameraOffsetX, i * 32 + cameraOffsetY))
            pass
        pass
    if debug:
        startX, startY = getStartPoint()
        connected(startX, startY)

    visitedBackground = []
    pygame.display.flip()
    return 1

switchWallStatus = 0

cameraOffsetX = 0
cameraOffsetY = 0
cameraSpeed = 5
debug = 0

background_colour = (0,0,0)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gnome")
win.fill(background_colour)

# Load sprites
dirt = pygame.image.load("map/grey_dirt0.png").convert()
wall = pygame.image.load("map/stone2_gray0.png").convert()

background = createBackground()
visitedBackground = []
connectRooms()

pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F1:
                background = createBackground()
                connectRooms()
            if event.key == pygame.K_f:
                switchWallStatus = not switchWallStatus
        if pygame.mouse.get_pressed()[0]:
            switchWall()

    if pygame.key.get_pressed()[pygame.K_F2]:
        debug = True
    else:
        debug = False

    if pygame.key.get_pressed()[pygame.K_w]:
        cameraOffsetY += cameraSpeed
    if pygame.key.get_pressed()[pygame.K_a]:
        cameraOffsetX += cameraSpeed
    if pygame.key.get_pressed()[pygame.K_s]:
        cameraOffsetY -= cameraSpeed
    if pygame.key.get_pressed()[pygame.K_d]:
        cameraOffsetX -= cameraSpeed

    visitedBackground = []
    update()
pygame.quit()
