import pygame
from settings import *

class Sprite:
    def __init__(self, filename):
        self.size = spriteSize
        self.zoom = zoom
        self.filename = filename
        self.art = pygame.image.load(filename).convert()
        self.originalArt = self.art #used to keep a copy of the original so when scaling we do not have to reload the image
    def draw(self, window, pos):
        window.blit(self.art, pos)

    # This will be used for zoom (we only hav to resize sprites every time zoom happens)
    def resize(self, size):
        self.size = size
        # if size == 32:
        #     self.art = self.originalArt
        # else:
        #     #self.art = pygame.image.load(self.filename).convert() # loading everytime seems to help with image quality since we arent scaling an already scaled image again now
        #     self.art = pygame.transform.scale(self.originalArt, (self.size, self.size))
        self.art = pygame.transform.scale(self.originalArt, (self.size, self.size))
        return
