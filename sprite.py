import pygame
from settings import *

class Sprite:
    def __init__(self, filename):
        self.size = spriteSize
        self.filename = filename

        self.art = pygame.image.load(filename).convert()
        self.originalArt = self.art

        # self.addons = []

    def draw(self, window, pos):
        window.blit(self.art, pos)

    def resize(self, size):
        self.size = size
        self.art = pygame.transform.scale(self.originalArt, (self.size, self.size))
        return

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
