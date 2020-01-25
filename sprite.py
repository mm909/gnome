import pygame
from settings import *

class Sprite:
    def __init__(self, filename):
        self.size = spriteSize
        self.filename = filename

        self.art = pygame.image.load(filename).convert_alpha()
        self.originalArt = self.art

        # self.addons = []

    def draw(self, window, pos):
        window.blit(self.art, pos)
        return

    def drawAlpha(self, window, pos, alpha):
        Sprite.blit_alpha(window, self.art, pos, alpha)

    def resize(self, size):
        self.size = size
        self.art = pygame.transform.scale(self.originalArt, (self.size, self.size))
        return

    def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    # # Fill is a tuple eg. (255,255,255)
    # def rect(self, x, y, width, height, fill):
    #     key = (1, x, y, width, height, fill)
    #     if not key in self.addons:
    #         self.addons.append(key)
    #     return
    #
    # def clearAddons():
    #     self.addons = []
    #     return
