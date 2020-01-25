import pygame
from settings import *
from sprite import *

class Gnome:
    def __init__(self,startPos):
        self.art = Sprite("player/pig_form.png")
        self.pos = startPos
        return

    def draw(self, window, ox, oy, ss):
        newPos = (self.pos[0] * ss + ox, self.pos[1] * ss + oy)
        self.art.draw(window, newPos)

    def resize(self, size):
        self.art.resize(size)
        return
