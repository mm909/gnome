import pygame
from gameHandler import *
from settings import *
from random import *
from sprite import *
from draw import *
from room import *
from astar import *

class Map:

    def __init__(self):

        # Import from settings file
        self.cameraOffsetX    = cameraOffsetX
        self.cameraOffsetY    = cameraOffsetY
        self.switchWallStatus = switchWallStatus
        self.debug = debug
        self.spriteSize = spriteSize
        self.placingSprite = placingSprite
        self.exit = (-1,-1)
        self.new = True

        self.unseen = Sprite("map/dngn_unseen.png")
        # self.wall = Sprite("map/stone2_gray0.png")
        self.wall = Sprite("map/stone_gray0.png")
        self.dirt0 = Sprite("map/grey_dirt0.png")
        self.dirt1 = Sprite("map/grey_dirt1.png")
        self.dirt2 = Sprite("map/grey_dirt2.png")
        self.dirt3 = Sprite("map/grey_dirt3.png")
        self.dirt4 = Sprite("map/grey_dirt4.png")
        self.dirt5 = Sprite("map/grey_dirt5.png")
        self.dirt6 = Sprite("map/grey_dirt6.png")
        self.dirt7 = Sprite("map/grey_dirt7.png")
        self.stone = Sprite("map/stone_dark0.png")
        # self.cobble = Sprite("map/cobble_blood1.png")
        self.cobble = Sprite("map/rect_gray0.png")
        # self.cobble = Sprite("map/pebble_brown0.png")
        # self.dirt = pygame.image.load("map/grey_dirt0.png").convert()
        self.door = Sprite("map/dngn_closed_door.png")
        self.stairsDown = Sprite("map/stone_stairs_down.png")
        self.roomWall = self.wall

        self.sprites = []
        self.sprites.append(self.unseen)
        self.sprites.append(self.wall)
        self.sprites.append(self.dirt0)
        self.sprites.append(self.dirt1)
        self.sprites.append(self.dirt2)
        self.sprites.append(self.dirt3)
        self.sprites.append(self.dirt4)
        self.sprites.append(self.dirt5)
        self.sprites.append(self.dirt6)
        self.sprites.append(self.dirt7)
        # self.sprites.append(self.stone)
        self.sprites.append(self.cobble)
        self.sprites.append(self.door)
        self.sprites.append(self.stairsDown)
        self.sprites.append(self.roomWall)

        self.unseenMap = []
        self.reserved = []
        self.rooms = []
        self.map = Map.createBackground(self)
        self.connected = []
        self.visitedBackground = []

    def placeExit(self):
        pos = Map.getOpenPos(self, True)
        self.exit = pos
        self.map[pos[1]][pos[0]] = 12

    def hideWalls(self):
        self.unseenMap = []
        for i in range(tilesY):
            row = []
            for j in range(tilesX):
                row.append(1)
            self.unseenMap.append(row)

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if x >= 0 and x < tilesX and y >= 0 and y < tilesY:
                    shown = False
                    for i in range(-1, 2):
                        neighborX = x + i
                        if neighborX >= 0 and neighborX < tilesX:
                            for j in range (-1, 2):
                                neighborY = y + j
                                if neighborY >= 0 and neighborY < tilesY:
                                    if self.map[neighborY][neighborX] > 1 and not self.map[neighborY][neighborX] == 13:
                                        shown = True

                    if not shown:
                        # self.unseenMap.append((x,y))
                        self.unseenMap[y][x] = 0
        return

    def setSpriteSize(self, zoom):
        mx, my  = self.getMouseCoords()
        zoomScale = zoom / self.spriteSize
        self.spriteSize = zoom
        self.cameraOffsetX = self.cameraOffsetX * zoomScale
        self.cameraOffsetY = self.cameraOffsetY * zoomScale
        mx = mx * zoomScale
        my = my * zoomScale

        nmx, nmy = self.getMouseCoords()

        mxOffset = nmx - mx
        myOffset = nmy - my

        self.cameraOffsetX += mxOffset
        self.cameraOffsetY += myOffset

        for sprite in self.sprites:
            sprite.resize(zoom)
            pass

    def getOpenPos(self, inroom):
        tries = 500
        while(tries > 0):
            x = randint(0,tilesX-1)
            y = randint(0,tilesY-1)
            if(self.map[y][x] > 1):
                if inroom:
                    for room in self.rooms:
                        if(room.isInside(x,y)):
                            return(x,y)
                else:
                    return (x,y)
            tries -= 1
        return(-1,-1)

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
                if self.unseenMap[i][j]:
                    self.sprites[tile].draw(window, (x, y))
                else:
                    self.sprites[tile].draw(window, (x, y))
                    self.sprites[0].drawAlpha(window, (x, y), 235)
                pass
            pass

        if self.debug:
            for node in self.connected:
                rect(window, self.spriteSize, (100,255,100),
                    (node[0], node[1], self.cameraOffsetX, self.cameraOffsetY, 12, 12, 8, 8))

            for i, row in enumerate(self.reserved):
                for j, tile in enumerate(row):
                    if(self.reserved[i][j] == 0):
                        rect(window,self.spriteSize, (255,100,100),
                            (j, i, self.cameraOffsetX, self.cameraOffsetY, 14, 14, 4, 4))

            # create a text suface object,
            # on which text is drawn on it.
            font = pygame.font.Font('FreeSansBold.ttf', 22)
            text = font.render('Placing:' , True, (0,0,0), (151,151,151))
            textRect = text.get_rect()
            # textRect.center = (0,0)
            window.blit(text, textRect)
            self.sprites[self.placingSprite].draw(window, (85, 0))
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
            self.map[my][mx] = self.placingSprite
            self.hideWalls()
        self.new = True
        return

    def getStartPoint(self):
        startX = -1
        startY = -1
        for i, backgroundRow in enumerate(self.map):
            for j, tile in enumerate(backgroundRow):
                if self.map[i][j] > 1:
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
                if self.map[i][j] > 1 and not (j , i) in self.visitedBackground:
                    startX = j
                    startY = i
                    # pygame.draw.rect(win, (255,255,255), (j * 32 + 12 + cameraOffsetX, i * 32 + 12 + cameraOffsetY, 8, 8))
                    return startX, startY
        return startX, startY

    def connected(self, startX, startY, localConnections = []):
        queue = []
        queue.append((startX,startY))

        if not (startX,startY) in self.visitedBackground:
            self.visitedBackground.append((startX,startY))
        if not (startX,startY) in self.connected:
            self.connected.append((startX,startY))
        if not (startX, startY) in localConnections:
            localConnections.append((startX, startY))


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
                                    # and self.map[neighborY][neighborX] < 13
                                    if self.map[neighborY][neighborX] > 1 and not (neighborX,neighborY) in localConnections :
                                        if not (i == 0 and j == 0):
                                            if not (neighborX,neighborY) in self.visitedBackground:
                                                self.visitedBackground.append((neighborX,neighborY))
                                            if not (neighborX,neighborY) in self.connected:
                                                self.connected.append((neighborX,neighborY))
                                            localConnections.append((neighborX,neighborY))
                                            queue.append((neighborX,neighborY))

        return

    def createBackground(self):
        self.reserved = []
        self.map = []
        self.rooms = []
        for i in range(tilesY):
            backgroundRow = []
            backgroundRowR = []
            for j in range(tilesX):
                backgroundRow.append(1)
                backgroundRowR.append(1)
            self.map.append(backgroundRow)
            self.reserved.append(backgroundRowR)
        roomNumber = randint(roomMin,roomMax)

        #offset = 0.03
        offsetX = 1
        offsetY = 1
        for i in range(roomNumber):
            tries = 100
            while tries > 0:
                roomX = randint(offsetX, tilesX- 1 - offsetX)
                roomY = randint(offsetY, tilesY- 1 - offsetY)
                if(self.reserved[roomY][roomX] != 0):
                    break
                tries -= 1
            roomWidth = randint(roomMinWidth, roomMaxWidth)
            roomHeight = randint(roomMinHeight, roomMaxHeight)

            if roomX + roomWidth - 1 >= tilesX - offsetX:
                 roomX += (tilesX - offsetX -1) - (roomX + roomWidth - 1)
                 if roomX < offsetX:
                     roomWidth += roomX - offsetX
                     roomX = offsetX

            if roomY + roomHeight - 1 >= tilesY -offsetY:
                roomY += (tilesY - offsetY -1) - (roomY + roomHeight - 1)
                if roomY < offsetY:
                    roomHeight += roomY - offsetY
                    roomY = offsetY

            goodRoom = True
            for j  in range(roomHeight):
                if(roomY + j >= offsetY and roomY + j < tilesY - offsetY):
                    for k in range(roomWidth):
                        if(roomX + k >= offsetX and roomX + k < tilesX - offsetX):
                            if(self.reserved[roomY + j][roomX + k] == 0):
                                goodRoom = False

            # these two loops can be combined
            if goodRoom:
                self.rooms.append(Room(roomX, roomY, roomWidth, roomHeight))

                for j  in range(-3, roomHeight + 3):
                    if(roomY + j >= offsetY and roomY + j < tilesY - offsetY):
                        for k in range(-3, roomWidth + 3):
                            if(roomX + k >= offsetX and roomX + k < tilesX - offsetX):
                                self.reserved[roomY + j][roomX + k] = 0
                for j  in range(roomHeight):
                    if(roomY + j >= offsetY and roomY + j < tilesY - offsetY):
                        for k in range(roomWidth):
                            if(roomX + k >= offsetX and roomX + k < tilesX - offsetX):
                                self.map[roomY + j][roomX + k] = randint(2,9)

                for j in range(roomX -1, roomX + roomWidth+1):
                    self.map[roomY-1][j] = 13
                    self.map[roomY + roomHeight][j] = 13

                for j in range(roomY-1, roomY + roomHeight +1):
                    self.map[j][roomX-1] = 13
                    self.map[j][roomX + roomWidth] = 13


        self.connected = []
        self.visitedBackground = []
        Map.connectRooms(self)
        self.debugBFS()
        self.hideWalls()
        self.placeExit()
        # print(self.rooms)
        self.new = True
        return self.map

    def connectRooms(self):
        self.visitedBackground = []
        localConnections = []
        roomFrom = self.getRoom(localConnections, False)
        Map.connected(self, roomFrom.x, roomFrom.y, localConnections)

        roomTo = self.getRoom(localConnections, False)
        while roomTo != -1:
            #connected(endX, endY)

            print("creating a new path")
            Map.createPath(self, roomFrom, roomTo, localConnections)
            print("path created")
            #print("back from creating path")

            roomFrom = self.getRoom(localConnections, True)

            if roomFrom == -1:
                break
            # Map.connected(self, roomFrom.x, roomFrom.y, localConnections)

            roomTo = self.getRoom(localConnections, False)

        return

    def createPath(self, roomFrom, roomTo, localConnections = []):
        doorFrom =0
        doorTo = 0
        putDoorX = randint(0,1)
        if putDoorX == 1:
            if roomFrom.x - roomTo.x < 0:
                doorFrom = roomFrom.getDoor("right")
                doorTo = roomTo.getDoor("left")
            elif roomFrom.x - roomTo.x > 0:
                doorFrom = roomFrom.getDoor("left")
                doorTo = roomTo.getDoor("right")
            else:
                randomSide = randint(0,1)
                if randomSide == 1:
                    doorFrom = roomFrom.getDoor("right")
                    doorTo = roomTo.getDoor("right")
                else:
                    doorFrom = roomFrom.getDoor("left")
                    doorTo= roomTo.getDoor("left")
        else:
            if roomFrom.y - roomTo.y < 0:
                doorFrom = roomFrom.getDoor("bottom")
                doorTo = roomTo.getDoor("top")
            elif roomFrom.y - roomTo.y > 0:
                doorFrom = roomFrom.getDoor("top")
                doorTo = roomTo.getDoor("bottom")
            else:
                randomSide = randint(0,1)
                if randomSide == 1:
                    doorFrom = roomFrom.getDoor("top")
                    doorTo = roomTo.getDoor("top")
                else:
                    doorFrom = roomFrom.getDoor("bottom")
                    doorTo= roomTo.getDoor("bottom")

        if doorFrom[0] < 0 or doorFrom[0] >= tilesX or doorFrom[1] < 0 or doorFrom[1] >= tilesY:
            print("FROM:  broken coordinates", "doorX: ", doorFrom[0], "doorY:", doorFrom[1], "tilesX: ", tilesX, "tilesY:", tilesY)
        startX = doorFrom[0]
        startY = doorFrom[1]

        if doorTo[0] < 0 or doorTo[0] >= tilesX or doorTo[1] < 0 or doorTo[1] >= tilesY:
            print("TO:  broken coordinates", "doorX: ", doorTo[0], "doorY:", doorTo[1], "tilesX: ", tilesX, "tilesY:", tilesY)
        endX = doorTo[0]
        endY = doorTo[1]

        self.map[startY][startX] = 11
        self.map[endY][endX] = 11

        path = astar(self.map, (startX, startY), (endX, endY), False)
        if path is None:
            return

        print("has a path")
        for point in path:
            self.map[point[1]][point[0]] = randint(2,9)
            Map.connected(self, point[0], point[1], localConnections)

        self.map[startY][startX] = 11
        self.map[endY][endX] = 11

        #
        # slopeX = abs(startX - endX)
        # slopeY = abs(startY - endY)
        #

        #
        # #print(endX, endY)
        # moveX = randint(0,1)
        # currX = startX
        # currY = startY
        # while not (endX, endY) in localConnections:
        #     #visitedBackground = []
        #     if  moveX == True:
        #         if slopeX >0:
        #             currX = currX + dx
        #             self.map[currY][currX] = randint(2,9)
        #             slopeX = slopeX - 1
        #             Map.connected(self, currX, currY, localConnections)
        #         else:
        #             moveX = False
        #
        #     elif moveX == False:
        #         if slopeY > 0:
        #             currY = currY + dy
        #             self.map[currY][currX] = randint(2,9)
        #             slopeY = slopeY - 1
        #             Map.connected(self, currX, currY, localConnections)
        #         else:
        #             moveX = True

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

    def getRoom(self, localConnections, connected = True):
        roomFound = False
        roomIndex = -1


        for room in self.rooms:
            if connected == True and (room.x, room.y) in localConnections:
                #print("room found in connected equal True")
                roomFound = True
                break
            elif connected == False and not (room.x, room.y) in localConnections:
                roomFound = True
                break
        if roomFound == False:
            #print("for loop found no suitable room for conditions")
            return -1

        roomFound = False
        while roomFound == False:
            roomIndex = randint(0, len(self.rooms) - 1)
            if connected == True and (self.rooms[roomIndex].x, self.rooms[roomIndex].y) in localConnections:
                roomFound = True
            elif connected == False and not (self.rooms[roomIndex].x, self.rooms[roomIndex].y) in localConnections:
                roomFound = True

        #print("returning room")
        return self.rooms[roomIndex]
