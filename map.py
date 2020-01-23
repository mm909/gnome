import pygame
from mapGenSettings import *
from random import *

class Map:
    def __init__(self):

        self.cameraOffsetX    = cameraOffsetX
        self.cameraOffsetY    = cameraOffsetY
        self.switchWallStatus = switchWallStatus

        self.map = Map.createBackground(self)
        visitedBackground = []
        Map.connectRooms(self)

    def getMouseCoords(self):
        coords = pygame.mouse.get_pos()
        mx = coords[0] - self.cameraOffsetX
        my = coords[1] - self.cameraOffsetY
        return mx, my

    def switchWall(self):
        mx, my = Map.getMouseCoords(self)
        mx = int(mx / 32)
        my = int(my / 32)
        if my >= 0 and my < tilesY and mx >= 0 and mx < tilesX:
            self.map[my][mx] = self.switchWallStatus
        return

    def getStartPoint(self):
        startX = -1
        startY = -1
        for i, backgroundRow in enumerate(self.map):
            for j, tile in enumerate(backgroundRow):
                if self.map[i][j] == 0:
                    startX = j
                    startY = i
                    # pygame.draw.rect(win, (255,255,255), (j * 32 + 12 + cameraOffsetX, i * 32 + 12 + cameraOffsetY, 8, 8))
                    return startX, startY
        return startX, startY

    def findClusterPoint(self): #will be used to find the next room to create a path too. the same as getStartPoint just didnt want to rename that function and change it a little without discussing first
        startX = -1
        startY = -1
        for i, backgroundRow in enumerate(self.map):
            for j, tile in enumerate(backgroundRow):
                if self.map[i][j] == 0 and not (j , i) in visitedBackground:
                    startX = j
                    startY = i
                    # pygame.draw.rect(win, (255,255,255), (j * 32 + 12 + cameraOffsetX, i * 32 + 12 + cameraOffsetY, 8, 8))
                    return startX, startY
        return startX, startY

    def connected(self, x,y):
        visitedBackground.append((x,y))
        if x >= 0 and x < tilesX and y >= 0 and y < tilesY:
            for i in range(-1, 2):
                neighborX = x + i
                if neighborX >= 0 and neighborX < tilesX:
                    for j in range (-1, 2):
                        if i == 0 or j == 0:   #only does dfs on non-diagonal neighbors to stop diagonal only path connections if  (abs(i) != 1 or abs(j) != 1):
                            neighborY = y + j
                            if neighborY >= 0 and neighborY < tilesY:
                                if self.map[neighborY][neighborX] == 0 and not (neighborX,neighborY) in visitedBackground:
                                    if not (i == 0 and j == 0):
                                        # pygame.draw.rect(win, (100,255,100), (neighborX * 32 + 12 + cameraOffsetX, neighborY * 32 + 12 + cameraOffsetY, 8, 8))
                                        Map.connected(self, neighborX, neighborY)
        return

    def createBackground(self):
        self.map = []
        for i in range(tilesY):
            backgroundRow = []
            for j in range(tilesX):
                backgroundRow.append(1)
            self.map.append(backgroundRow)
        roomNumber = randint(roomMin,roomMax)

        offset = 0.05
        for i in range(roomNumber):
            roomX = randint(0 + int(tilesX*offset), tilesX-1 - int(tilesX * offset))
            roomY = randint(0 + int(tilesY*offset), tilesY-1 - int(tilesY * offset))
            roomWidth = randint(roomMinWidth, roomMaxWidth)
            roomHeight = randint(roomMinHeight, roomMaxHeight)
            self.map[roomY][roomX] = 0
            for j  in range(roomHeight):
                if(roomY + j >= 0 and roomY + j < tilesY):
                    for k in range(roomWidth):
                        if(roomX + k >= 0 and roomX + k < tilesX):
                            self.map[roomY + j][roomX + k] = 0
        return self.map

    def connectRooms(self):
        global visitedBackground
        visitedBackground = []
        startX, startY = Map.getStartPoint(self)
        Map.connected(self, startX, startY)
        endX, endY = Map.findClusterPoint(self)
        while endX != -1 and endY != -1:
            #connected(endX, endY)
            Map.createPath(self, startX, startY, endX, endY)
            endX, endY = Map.findClusterPoint(self)
        return

    def createPath(self, startX, startY, endX, endY):
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
                    self.map[currY][currX] = 0
                    slopeX = slopeX - 1
                    Map.connected(self, currX, currY)
                else:
                    moveX = False

            elif moveX == False:
                if slopeY > 0:
                    currY = currY + dy
                    self.map[currY][currX] = 0
                    slopeY = slopeY - 1
                    Map.connected(self, currX, currY)
                else:
                    moveX = True

        return
