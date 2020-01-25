

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
            print("Door Added")
            return True
        else:
            print("Door Not Added: ", self.x, self.y, self.width, self.height, doorX, doorY, )
            return False
        return
