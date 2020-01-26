
import pygame
import time
import math
from map import *
from random import *
from settings import *
from gnome import *

def distance(pt1, pt2):
    dist = math.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
    #print("distance: ", dist)
    return dist

class GameHandler:


    def __init__(self):
        pygame.init()
        self.dt = 0
        self.previousTime = time.time()
        self.spriteSize = spriteSize



        self.background_colour = (0,0,0)

        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Gnome Dungeon")
        self.win.fill(self.background_colour)

        self.map = Map()
        startPos = self.map.getOpenPos(True)
        self.player = Gnome(startPos)

        pygame.display.flip()

        self.running = True

        self.gameLoop()

    def update(self):
        self.win.fill(self.background_colour)
        self.map.draw(self.win)
        self.player.draw(self.win, self.map.cameraOffsetX, self.map.cameraOffsetY, self.map.spriteSize)
        if self.map.new:
            self.player.AStar(self.map)
            self.map.new = False
        if(self.map.debug):
            self.player.drawPath(self.win, self.map.spriteSize, self.map.cameraOffsetX, self.map.cameraOffsetY)
            pygame.draw.rect(self.win, (255,255,255), (width/2-2,height/2-2,4,4))
        self.player.moveWithPath(self.dt)
        pygame.display.flip()
        return

    def pygameEventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_F1:
                    self.map.createBackground()
                    startPos = self.map.getOpenPos(True)
                    self.player = Gnome(startPos)
                    self.player.resize(self.spriteSize)
                if event.key == pygame.K_F2:
                    self.map.debugToggle()
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    self.map.placingSprite += 1
                    if self.map.placingSprite >= len(self.map.sprites):
                        self.map.placingSprite = len(self.map.sprites) - 1
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.map.placingSprite -= 1
                    if self.map.placingSprite < 0:
                        self.map.placingSprite = 0
                if event.key == pygame.K_h:
                    self.map.connectRooms()

            if event.type == pygame.MOUSEBUTTONDOWN:
                spriteResized = False
                if event.button == 4:
                    # if(self.spriteSize != 64):
                    #     self.map.cameraOffsetX -= 64 # - somthing extra....
                    #     self.map.cameraOffsetY -= 48 #* (self.spriteSize / 32)
                    #     print(self.map.cameraOffsetX, self.map.cameraOffsetY)
                    self.spriteSize = min(self.spriteSize + 4, 64)
                    spriteResized = True
                if event.button == 5:
                    # if(self.spriteSize != 8):
                    #     self.map.cameraOffsetX += 64 # I feel like map should handle the cameraOffset stuff in its sprite resize function
                    #     self.map.cameraOffsetY += 48
                    #     print(self.map.cameraOffsetX, self.map.cameraOffsetY)
                    self.spriteSize = max(self.spriteSize - 4, 8)
                    spriteResized = True
                    # self.map.cameraOffsetX -= (width * (4/32)) / 2
                    # self.map.cameraOffsetY -= (height * (4/32)) / 2
                if spriteResized == True: #just making it easier if for some reason we have to add more function calls we dont just copy and paste lines
                    self.map.setSpriteSize(self.spriteSize)
                    self.player.resize(self.spriteSize)

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

        # if cameraVel[0] != 0:
        #     print(self.map.cameraOffsetX)
        # if cameraVel[1] != 0:
        #     print(self.map.cameraOffsetY)
        return

    def gameLoop(self):
        while self.running:

            currentTime = time.time()
            self.dt = currentTime - self.previousTime
            self.previousTime = currentTime

            self.pygameEventHandle()
            self.CameraMovement()

            self.update()

            if(distance(self.player.pos, self.map.exit) < 0.1):
                self.map.createBackground()
                startPos = self.map.getOpenPos(True)
                self.player = Gnome(startPos)
                self.player.resize(self.map.spriteSize)

        pygame.quit()
        return
