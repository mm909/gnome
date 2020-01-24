import pygame
from settings import *

class Sprite:
    def __init__(self, filename):
        self.size = spriteSize
        self.art = pygame.image.load(filename).convert()
        return
    def draw(self, window, pos):
        window.blit(self.art, pos)
        return
