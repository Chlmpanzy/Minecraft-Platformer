import pygame
pygame.init()
from math import *


class Game():
    def __init__(self):
        self.surface = pygame.display.set_mode((600, 900))
        self.level = 1

    def reset(self, player):
        player.x = 100
        player.y = 450

    def drawAll(self, surface, platforms):
        for platform in platforms:
            for block in platform:
                block.draw(surface) 
        pass
        

class Block():
    def __init__(self, type, x,y):
        self.type = type
        self.image = pygame.image.load(self.type+".png")
        self.image = pygame.transform.scale(self.image,(25,25))
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Platform():
    def __init__(self,type, length, x, y):
        self.blocks = []
        self.type = type
        self.x = x
        self.y = y
        offset = 0
        self.length = length
        for x in range(self.length):
            self.blocks.append(Block(self.type, self.x + offset,self.y))
            offset += 25

    def draw(self,surface):
        for block in self.blocks:
            block.draw(surface)
    
class Bounce(Platform):
    def __init__(self, length, x, y):
        Platform.__init__(self, "bounce", length, x, y)


class Grass(Platform):
    def __init__(self, length, x, y):
        Platform.__init__(self, "grass", length, x, y)

class Dive(Platform):
    def __init__(self, length, x, y):
        Platform.__init__(self, "dive", length, x, y)

class Water(Platform):
    def __init__(self, length, x, y):
        Platform.__init__(self, "water", length, x, y)

    

        

class Player():
    def __init__(self, x, y):
        self.Vy = 0
        self.jumpSpeed = -20
        self.gravity = 2

        self.x = x
        self.y = y
        self.image = pygame.image.load("steve.png")
        self.image = pygame.transform.scale(self.image,(25,50))
        

    def draw(self, surface):
        surface.blit(self.image,(self.x,self.y))

    def jump(self):
        self.y -= 20
    
    def moveRight(self):
        self.x += 10

    def moveLeft(self):
        self.x -= 10

    def collide(self, platforms):
        player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        for platform in platforms:
            for block in platform.blocks:
                block_rect = pygame.Rect(block.x, block.y, block.image.get_width(), block.image.get_height())
                if player_rect.colliderect(block_rect):
                    return True
        return False
    

    class Level():
        def __init__(self, levelNumber):
            self.level = levelNumber

            


