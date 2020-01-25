import pygame
from settings import *
from random import *
from sprite import *
from draw import *

class Map:

    def __init__(self):

        # Import from settings file
        self.cameraOffsetX    = cameraOffsetX
        self.cameraOffsetY    = cameraOffsetY
        self.switchWallStatus = switchWallStatus
        self.debug = debug
        self.spriteSize = spriteSize

        self.dirt = Sprite("map/grey_dirt0.png")
        self.wall = Sprite("map/stone2_gray0.png")
        # self.dirt = pygame.image.load("map/grey_dirt0.png").convert()
        # self.wall = pygame.image.load("map/stone2_gray0.png").convert()

        self.sprites = []
        self.sprites.append(self.dirt)
        self.sprites.append(self.wall)

        self.map = Map.createBackground(self)
        self.connected = []
        self.visitedBackground = []
        #Map.connectRooms(self)

    def setSpriteSize(self, zoom):
        self.spriteSize = zoom
        for sprite in self.sprites:
            sprite.resize(zoom)
            pass

    def draw(self, window):
        for i, backgroundRow in enumerate(self.map):
            y = i * self.spriteSize + self.cameraOffsetY
            if y + self.spriteSize < 0:
                continue
            elif y >= height:
                break
            for j, tile in enumerate(backgroundRow):
                x = j * self.spriteSize + self.cameraOffsetX
                if x + self.spriteSize <0:
                    continue
                elif x >= width:
                    break
                self.sprites[tile].draw(window, (x, y))
                # if(tile == 0):
                #     self.wall.draw(window, (j * 32 + self.cameraOffsetX, i * 32 + self.cameraOffsetY))
                # elif(tile == 1):
                #     self.wall.draw(window, (j * 32 + self.cameraOffsetX, i * 32 + self.cameraOffsetY))
                pass
            pass
        if self.debug:
            #moved into a debugDFS function as to reduce overhead for every frame
            # self.connected = []
            # self.visitedBackground = []
            # startX, startY = Map.findClusterPoint(self)
            # while startX != -1 and startY != -1:
            #     Map.connected(self, startX, startY)
            #     startX, startY = Map.findClusterPoint(self)
            for node in self.connected:
                rect(
                window,
                self.spriteSize,
                (100,255,100),
                (node[0], node[1], self.cameraOffsetX, self.cameraOffsetY, 12, 12, 8, 8)
                )
                # pygame.draw.rect(window, (100,255,100), (node[0] * self.spriteSize + 12 + self.cameraOffsetX, node[1] * self.spriteSize + 12 + self.cameraOffsetY, 8, 8))
        return

    def getMouseCoords(self):
        coords = pygame.mouse.get_pos()
        mx = coords[0] - self.cameraOffsetX
        my = coords[1] - self.cameraOffsetY
        return mx, my

    def switchWall(self):
        mx, my = Map.getMouseCoords(self)
        mx = int(mx / self.spriteSize)
        my = int(my / self.spriteSize)
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
                    self.connected.append((j,i))
                    # pygame.draw.rect(win, (255,255,255), (j * 32 + 12 + cameraOffsetX, i * 32 + 12 + cameraOffsetY, 8, 8))
                    return startX, startY
        return startX, startY

    def findClusterPoint(self): #will be used to find the next room to create a path too. the same as getStartPoint just didnt want to rename that function and change it a little without discussing first
        startX = -1
        startY = -1
        for i, backgroundRow in enumerate(self.map):
            for j, tile in enumerate(backgroundRow):
                if self.map[i][j] == 0 and not (j , i) in self.visitedBackground:
                    startX = j
                    startY = i
                    # pygame.draw.rect(win, (255,255,255), (j * 32 + 12 + cameraOffsetX, i * 32 + 12 + cameraOffsetY, 8, 8))
                    return startX, startY
        return startX, startY

    def connected(self, startX,startY):
        queue = []
        queue.append((startX,startY))

        if not (startX,startY) in self.visitedBackground:
            self.visitedBackground.append((startX,startY))
        if not (startX,startY) in self.connected:
            self.connected.append((startX,startY))

        while queue:
            node = queue.pop(0)
            x = node[0]
            y = node[1]
            if x >= 0 and x < tilesX and y >= 0 and y < tilesY:
                for i in range(-1, 2):
                    neighborX = x + i
                    if neighborX >= 0 and neighborX < tilesX:
                        for j in range (-1, 2):
                            if i == 0 or j == 0:   #only does dfs on non-diagonal neighbors to stop diagonal only path connections if  (abs(i) != 1 or abs(j) != 1):
                                neighborY = y + j
                                if neighborY >= 0 and neighborY < tilesY:
                                    if self.map[neighborY][neighborX] == 0 and not (neighborX,neighborY) in self.visitedBackground:
                                        if not (i == 0 and j == 0):
                                            self.visitedBackground.append((neighborX,neighborY))
                                            if not (neighborX,neighborY) in self.connected:
                                                self.connected.append((neighborX,neighborY))
                                            queue.append((neighborX,neighborY))

        return

    def createBackground(self):
        self.map = []
        for i in range(tilesY):
            backgroundRow = []
            for j in range(tilesX):
                backgroundRow.append(1)
            self.map.append(backgroundRow)
        roomNumber = randint(roomMin,roomMax)

        #offset = 0.03
        offsetX = 1
        offsetY = 1
        for i in range(roomNumber):
            roomX = randint(offsetX, tilesX- 1 - offsetX)
            roomY = randint(offsetY, tilesY- 1 - offsetY)
            roomWidth = randint(roomMinWidth, roomMaxWidth)
            roomHeight = randint(roomMinHeight, roomMaxHeight)

            if roomX + roomWidth -1 >= tilesX - offsetX:
                 roomX += (tilesX - offsetX -1) - (roomX + roomWidth - 1)
                 if roomX < offsetX:
                     roomWidth += roomX - offsetX
                     roomX = offsetX

            if roomY + roomHeight -1 >= tilesY -offsetY:
                roomY += (tilesY - offsetY -1) - (roomY + roomHeight - 1)
                if roomY < offsetY:
                    roomHeight += roomY - offsetY
                    roomY = offsetY

            self.map[roomY][roomX] = 0
            for j  in range(roomHeight):
                if(roomY + j >= offsetY and roomY + j < tilesY - offsetY):
                    for k in range(roomWidth):
                        if(roomX + k >= offsetX and roomX + k < tilesX - offsetX):
                            self.map[roomY + j][roomX + k] = 0

        self.connected = []
        self.visitedBackground = []
        self.debugBFS()
        return self.map

    def connectRooms(self):
        self.visitedBackground = []
        startX, startY = Map.getStartPoint(self)
        Map.connected(self, startX, startY)
        endX, endY = Map.findClusterPoint(self)
        while endX != -1 and endY != -1:
            #connected(endX, endY)
            Map.createPath(self, startX, startY, endX, endY)
            endX, endY = Map.findClusterPoint(self)
        return

    def createPath(self, startX, startY, endX, endY):
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
        while not (endX, endY) in self.visitedBackground:
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

    def debugToggle(self):
        if self.debug == True:
            self.debug = False
        else:
            self.debug = True
            self.debugBFS()

    def debugBFS(self):
        if self.debug == True:
            self.connected = []
            self.visitedBackground = []
            startX, startY = Map.findClusterPoint(self)
            while startX != -1 and startY != -1:
                Map.connected(self, startX, startY)
                startX, startY = Map.findClusterPoint(self)

        return
