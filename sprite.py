import pygame
from settings import *

class Sprite:
    def __init__(self, filename):
        self.size = spriteSize
        self.filename = filename

        self.art = pygame.image.load(filename).convert()
        self.originalArt = self.art

    def draw(self, window, pos):
        window.blit(self.art, pos)

    def resize(self, size):
        self.size = size
        self.art = pygame.transform.scale(self.originalArt, (self.size, self.size))
        return
