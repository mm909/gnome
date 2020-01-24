
import pygame
import time
import math
from map import *
from random import *
from settings import *

class GameHandler:


    def __init__(self):
        self.dt = 0
        self.previousTime = time.time()
        self.spriteSize = spriteSize

        pygame.init()

        self.background_colour = (0,0,0)

        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Gnome Dungeon")
        self.win.fill(self.background_colour)

        self.map = Map()

        pygame.display.flip()

        self.running = True

        self.gameLoop()

    def update(self):
        self.win.fill(self.background_colour)
        self.map.draw(self.win)
        pygame.display.flip()
        return

    def pygameEventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    self.map.createBackground()
                if event.key == pygame.K_F2:
                    self.map.debugToggle()
                if event.key == pygame.K_f:
                    self.map.switchWallStatus = not map.switchWallStatus
                if event.key == pygame.K_h:
                    self.map.connectRooms()

            if event.type == pygame.MOUSEBUTTONDOWN:
                spriteResized = False
                if event.button == 4:
                    self.spriteSize = min(self.spriteSize + 2, 64)
                    spriteResized = True
                if event.button == 5:
                    self.spriteSize = max(self.spriteSize - 2, 2)
                    spriteResized = True
                if spriteResized == True: #just making it easier if for some reason we have to add more function calls we dont just copy and paste lines
                    print(self.spriteSize)
                    self.map.setSpriteSize(self.spriteSize)

            if pygame.mouse.get_pressed()[0]:
                self.map.switchWall()
        return

    def CameraMovement(self):
        #makes it so if you move diagonally then you dont get a speed boost by moving the same speed along the x and y axis (completing the triangle)
        cameraVel = [0,0]
        if pygame.key.get_pressed()[pygame.K_w]:
            #self.map.cameraOffsetY += cameraSpeed * self.dt
            cameraVel[1] += cameraSpeed * self.dt
        if pygame.key.get_pressed()[pygame.K_s]:
            #self.map.cameraOffsetY -= cameraSpeed * self.dt
            cameraVel[1] -= cameraSpeed * self.dt
        if pygame.key.get_pressed()[pygame.K_a]:
            #self.map.cameraOffsetX += cameraSpeed * self.dt
            cameraVel[0] += cameraSpeed * self.dt
        if pygame.key.get_pressed()[pygame.K_d]:
            #self.map.cameraOffsetX -= cameraSpeed * self.dt
            cameraVel[0] -= cameraSpeed * self.dt

            if cameraVel[0] != 0  and cameraVel[1] != 0:
                cameraMag = cameraVel[0]*cameraVel[0] + cameraVel[1]*cameraVel[1]
                if cameraMag >0:
                    cameraMag = math.sqrt(cameraMag)
                    cameraVel[0] *= (cameraSpeed * self.dt) / cameraMag
                    cameraVel[1] *= (cameraSpeed * self.dt) / cameraMag

        self.map.cameraOffsetX += cameraVel[0]
        self.map.cameraOffsetY += cameraVel[1]
        return

    def gameLoop(self):
        while self.running:

            currentTime = time.time()
            self.dt = currentTime - self.previousTime
            self.previousTime = currentTime

            self.pygameEventHandle()
            self.CameraMovement()

            self.update()

        pygame.quit()
        return
