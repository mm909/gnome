

class Room:

    def __init__(self, x, y, w, h):

        self.x = x
        self.y = y
        self.width = w
        self.height = h

        return

    def isInside(self,x,y):
        if x >= self.x and x < self.x + self.width:
            if y >= self.y and y < self.y + self.height:
                return True
        return False
