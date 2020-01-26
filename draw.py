import pygame

def rect(window, spriteSize, fill, details):
    x = details[0] * spriteSize + details[2] + details[4] * (spriteSize / 32)
    y = details[1] * spriteSize + details[3] + details[5] * (spriteSize / 32)
    width = details[6] * (spriteSize / 32)
    height = details[7] * (spriteSize / 32)
    pygame.draw.rect(window, fill, (x,y,width,height))
    return

def line(window, spriteSize, fill, details):
    x1 = details[0] * spriteSize + details[2] + details[4] * (spriteSize / 32)
    y1 = details[1] * spriteSize + details[3] + details[5] * (spriteSize / 32)
    x2 = details[6] * spriteSize + details[2] + details[4] * (spriteSize / 32)
    y2 = details[7] * spriteSize + details[3] + details[5] * (spriteSize / 32)
    pygame.draw.line(window, fill, (x1,y1), (x2,y2), 2)

    return
