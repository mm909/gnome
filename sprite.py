import pygame
from settings import *

class Sprite:
    def __init__(self, filename):
        self.size = spriteSize
        self.art = pygame.image.load(filename).convert()

    def draw(self, window, pos):
        window.blit(self.art, pos)

    # This will be used for zoom (we only hav to resize sprites every time zoom happens)
    def resize(self, size):
        image = pygame.Surface([size, size]).convert()
        image.blit(self.art, (0, 0), (0, 0, size, size))
        image.set_colorkey((0,0,0))
        self.art = image
