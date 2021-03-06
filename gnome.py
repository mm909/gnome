import pygame
import math
from settings import *
from sprite import *
from astar import *
from draw import *
from function import *
from random import *

class Gnome:
    def __init__(self,startPos):
        self.art = Sprite("player/pig_form.png")
        self.pos = startPos
        self.target = startPos
        self.path = []
        self.speed = randint(3,6)
        self.finished = False
        return

    def moveWithPath(self, dt):
        updateWaypoint = False
        if(self.path):
            if(distance(self.target, self.pos) < 0.2 and len(self.path) >= 1):
                del self.path[0]
                updateWaypoint = True

            if len(self.path) == 0:
                return

            if updateWaypoint == True:
                self.pos = self.target
                self.target = self.path[0]


            if self.pos[0] - self.target[0] > 0:
                newpos = (self.pos[0] - self.speed * dt, self.pos[1])
                self.pos = newpos
            if self.pos[0] - self.target[0] < 0:
                newpos = (self.pos[0] + self.speed *dt, self.pos[1])
                self.pos = newpos
            if self.pos[1] - self.target[1] > 0:
                newpos = (self.pos[0], self.pos[1] - self.speed * dt)
                self.pos = newpos
            if self.pos[1] - self.target[1] < 0:
                newpos = (self.pos[0], self.pos[1] + self.speed * dt)
                self.pos = newpos
        return

    def draw(self, window, ox, oy, ss):
        newPos = (self.pos[0] * ss + ox, self.pos[1] * ss + oy)
        self.art.draw(window, newPos)

    def resize(self, size):
        self.art.resize(size)
        return

    def AStar(self,map):
        pos = [int(self.pos[0]), int(self.pos[1])]
        self.path = astar(map.map, pos, map.exit)
        return

    def drawPath(self, win, spriteSize, cameraOffsetX, cameraOffsetY):
        if(self.path):
            for i, point in enumerate(self.path):
                if i + 1 < len(self.path):
                    line(win, spriteSize, (255,255,255),
                        (point[0], point[1], cameraOffsetX, cameraOffsetY, 15, 15, self.path[i + 1][0], self.path[i + 1][1]))

                    # pygame.draw.line(win, (255,255,255), (point[0] * 32 + 15 * (spriteSize / 32) , point[1] * 32 + 15 * (spriteSize / 32)), (self.path[i + 1][0] * 32 + 15 * (spriteSize / 32), self.path[i + 1][1] * 32 + 15 * (spriteSize / 32)), 2)
                pass
