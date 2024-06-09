import pygame
pygame.init()
from math import *

        

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
    def __init__(self, type, x, y, length, height):
        self.blocks: list[Block] = []
        self.type = type
        self.x = x
        self.y = y
        lengthOffset = 0
        heightOffest = 0
        self.length = length
        self.height = height
        for x in range(self.length):
            for i in range(self.height):
                self.blocks.append(Block(self.type, self.x + lengthOffset,self.y + heightOffest))
                heightOffest += 25
            heightOffest = 0
            lengthOffset += 25

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)
    
class Bounce(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "bounce", x, y, length, height)


class Grass(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "grass", x, y, length, height)

class Dive(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "dive", x, y, length, height)

class Water(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "water", x, y, length, height)

    

        

class Player():
    def __init__(self, x: int, y: int):
        self.Vy = 0
        self.jumpSpeed = -20
        self.gravity = 2
        self.x = x
        self.y = y
        self.image = pygame.image.load("steve.png")
        self.image = pygame.transform.scale(self.image,(25,50))
        

    def draw(self, surface):
        surface.blit(self.image,(self.x,self.y))
    
    def moveRight(self):
        self.x += 10

    def moveLeft(self):
        self.x -= 10

    def collide(self, platforms: list[list[Platform]]):
        playerRect = pygame.Rect(self.x, self.y, 25, 50)
        if platforms == None:
            return False
        for platform in platforms:
            for block in platform.blocks:
                blockRect = pygame.Rect(block.x, block.y, 25, 25)
                if playerRect.colliderect(blockRect):
                    return True
        return False
    
    def grassCollide(self, platform: list[Platform]):
        playerRect = pygame.Rect(self.x, self.y, 25, 40)
        for block in platform:
                blockRect = pygame.Rect(block.x, block.y, self.image.get_width()+25, self.image.get_height())
                if playerRect.colliderect(blockRect):
                    return True
        return False

    
    

class Level():
    def __init__(self, levelNumber: int, playerCoord: tuple[int], bedCoord, grass: list[Grass] = None , bounce: list[Bounce] = None, dive: list[Dive] = None, water: list[Water] = None):
        self.bedSpawn = bedCoord
        self.playerSpawn = playerCoord
        self.level = levelNumber
        self.grass = grass
        self.dive = dive
        self.water = water
        self.bounce = bounce
        self.platforms: dict[str:list[Platform]] = {"grass":self.grass, "bounce":self.bounce, "dive": self.dive, "water":self.water}
        self.platformsDraw: list[list[Platform]] = [self.grass, self.bounce, self.dive, self.bounce, self.water]
        

class Bed():
    def __init__(self, x, y):
        self.image = pygame.image.load("bed.png")
        self.image = pygame.transform.scale(self.image,(75,75))
        self.x = x
        self.y = y
    
    def collide(self, player: Player):
        playerRect = pygame.Rect(player.x, player.y, 25, 50)
        bedRect = pygame.Rect(self.x, self.y, 75, 55)

        if playerRect.colliderect(bedRect):
            return True
        return False
        

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

            

class Game():
    def __init__(self):
        self.surface = pygame.display.set_mode((600, 900))
        self.clock = pygame.time.Clock()
        self.deaths = 0
        self.level = 1
        level1 = Level(
            1, 
            (30, 450),
            (500, 200),
            grass = [Grass(30, 500, 2), Grass(130, 450, 2), Grass(230, 400, 2), Grass(400, 350, 2)],
            water = [Water(0, 800, int(600/25))]
            )
        level2 = Level(
            2,
            (30, 450),
            (500, 200),
            grass = [Grass(30,500, 2), Grass(400, 600, 2)],
            bounce= [Bounce(200, 500, 2), Bounce(500, 450, 2)],
            water = [Water(0, 800,int(600/25)), Water(400, 325,1, 3)]#, Water(1, 400, 325), Water(1, 400, 375)]
        )
        self.levels: list[Level] = [None, level1, level2]
        self.player = Player(self.levels[self.level].playerSpawn[0], self.levels[self.level].playerSpawn[1])
        self.bed = Bed(self.levels[self.level].bedSpawn[0], self.levels[self.level].bedSpawn[1])

    def reset(self):
        self.player.x, self.player.y = self.levels[self.level].playerSpawn
        self.deaths += 1

    def drawAll(self, surface):
        self.player.draw(surface)
        self.bed.draw(surface)
        for platform in self.levels[self.level].platformsDraw:
            if platform != None:
                for block in platform:
                    block.draw(surface) 

    def unSinkPlayer(self):
        while self.player.collide(self.levels[self.level].platforms["grass"]):
            self.player.y -= 1
        self.player.y += 1 #player needs to be barely touchign grass so he can jump

    def gameCollide(self, type):
        return self.player.collide(self.levels[self.level].platforms[type])
    
    def bedCollide(self):
        if self.bed.collide(self.player):
            self.nextLevel()

    def sideGrassCollide(self):
        return self.player.grassCollide(self.levels[self.level].platforms["grass"])
    
    def nextLevel(self):
        self.level += 1
        self.player.x, self.player.y = self.levels[self.level].playerSpawn
        self.bed.x, self.bed.y = self.levels[self.level].bedSpawn


