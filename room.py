from random import *
from settings import *

class Room:

    def __init__(self, x, y, w, h):

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.doors = []

        return

    def addDoor(self, doorX, doorY):
        if ((doorX == self.x - 1 or doorX == self.x + self.width) and doorY > self.y - 1 and doorY < self.y + self.height) or ((doorY == self.y - 1 or doorY == self.y + self.height) and doorX != self.x - 1 and doorX != self.x + self.width):
            self.doors.append((doorX, doorY))
            return True
        else:
            print("Door Not Added: ", self.x, self.y, self.width, self.height, doorX, doorY, )
            return False
        return

    def createRandomDoor(self):

        left = right = top = bottom = False
        for door in self.doors:
            if door[0] == self.x-1:
                left = True
            elif door[0] == self.x + self.width:
                right = True
            elif door[1] == self.y-1:
                top = True
            elif door[1] == self.y + self.height:
                bottom = True

        avaliableSides = []
        if left != True and self.x - 1 >= 0:
            avaliableSides.append("left")

        if right != True and self.x + self.width < tilesX:
            avaliableSides.append("right")

        if top != True and self.y - 1 >= 0:
            avaliableSides.append("top")

        if bottom != True and self.y + self.height < tilesY:
            avaliableSides.append("bottom")

        if len(avaliableSides) == 0:
            print("no avaliableSides")
            return (-1, -1)

        choosenSide = randint(0, len(avaliableSides) - 1)

        if avaliableSides[choosenSide] == "left":
            doorX = self.x - 1
            doorY = randint(self.y, self.y + self.height -1)
            self.addDoor(doorX, doorY)
            return (doorX, doorY)

        elif avaliableSides[choosenSide] == "right":
            doorX = self.x + self.width
            doorY = randint(self.y, self.y + self.height -1)
            self.addDoor(doorX, doorY)
            return (doorX, doorY)

        elif avaliableSides[choosenSide] == "top":
            doorX = randint(self.x, self.x + self.width -1)
            doorY = self.y - 1
            self.addDoor(doorX, doorY)
            return (doorX, doorY)

        elif avaliableSides[choosenSide] == "bottom":
            doorX = randint(self.x, self.x + self.width -1)
            doorY = self.y + self.height
            self.addDoor(doorX, doorY)
            return (doorX, doorY)


        return


    def getRandomDoor(self):
        numDoors = len(self.doors)
        if numDoors == 4:
            doorPicker = randint(0, numDoors-1)
            return self.doors[doorPicker]
        else:
            doorPicker = randint(0, numDoors)
            if doorPicker == numDoors:
                return self.createRandomDoor()
            else:
                return self.doors[doorPicker]
        return

    def isInside(self,x,y):
        if x >= self.x and x < self.x + self.width:
            if y >= self.y and y < self.y + self.height:
                return True
        return False
