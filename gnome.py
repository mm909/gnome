import pygame
from settings import *
from sprite import *
from astar import *
from draw import *

class Gnome:
    def __init__(self,startPos):
        self.art = Sprite("player/pig_form.png")
        self.pos = startPos
        self.path = []
        return

    def draw(self, window, ox, oy, ss):
        newPos = (self.pos[0] * ss + ox, self.pos[1] * ss + oy)
        self.art.draw(window, newPos)

    def resize(self, size):
        self.art.resize(size)
        return

    def AStar(self,map):
        self.path = astar(map.map, self.pos, map.exit)
        return

    def drawPath(self, win, spriteSize, cameraOffsetX, cameraOffsetY):
        if(self.path):
            for i, point in enumerate(self.path):
                if i + 1 < len(self.path):
                    line(win, spriteSize, (255,255,255),
                        (point[0], point[1], cameraOffsetX, cameraOffsetY, 15, 15, self.path[i + 1][0], self.path[i + 1][1]))

                    # pygame.draw.line(win, (255,255,255), (point[0] * 32 + 15 * (spriteSize / 32) , point[1] * 32 + 15 * (spriteSize / 32)), (self.path[i + 1][0] * 32 + 15 * (spriteSize / 32), self.path[i + 1][1] * 32 + 15 * (spriteSize / 32)), 2)
                pass
