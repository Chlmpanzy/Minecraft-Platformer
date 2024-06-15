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

class Lava(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "lava", x, y, length, height)

    

        

class Player():
    def __init__(self, x: int, y: int):
        self.facing = 'right'
        self.Vy = 0
        self.jumpSpeed = -20
        self.gravity = 2
        self.x = x
        self.y = y
        self.frame = 0
        self.frames = []

        for x in range(10):
            self.frames.append(pygame.transform.scale(pygame.image.load("mario"+str(x)+".png"), (25,50)))

        self.nextRightPic = [4, 4, 4, 4, 5, 6, 7, 5, 4, 4]
        self.nextLeftPic = [1, 2, 3, 1, 1, 1, 1, 1, 1, 1]

        self.jumped = False
        self.inAir = False
        

    def draw(self, surface):
        surface.blit(self.frames[self.frame],(self.x,self.y))
    
    def moveRight(self, change = True):
        self.x += 10
        if change:
            self.facing = 'right'

    def moveLeft(self, change = True):
        self.x -= 10
        if change:
            self.facing = 'left'

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
        if platform == None:
            return False
        for block in platform:
                blockRect = pygame.Rect(block.x, block.y, 50, 25)
                if playerRect.colliderect(blockRect):
                    return True
        return False
    
    def headCollide(self, platform: list[Platform]):
        if self.jumped:
            playerRect = pygame.Rect(self.x+2.5, self.y, 20, 10)
            if platform == None:
                return False
            for block in platform:
                    blockRect = pygame.Rect(block.x, block.y, 75, 25)
                    if playerRect.colliderect(blockRect):
                        self.y -= 1
                        return True
        return False

    
    

class Level():
    def __init__(self, levelNumber: int, playerCoord: tuple[int], bedCoord, grass: list[Grass] = None , bounce: list[Bounce] = None, dive: list[Dive] = None, lava: list[Lava] = None, playLava = False):
        self.bedSpawn = bedCoord
        self.playerSpawn = playerCoord
        self.level = levelNumber
        self.grass = grass
        self.dive = dive
        self.lava = lava
        self.bounce = bounce
        self.playLava = playLava
        self.platforms: dict[str:list[Platform]] = {"grass":self.grass, "bounce":self.bounce, "dive": self.dive, "lava":self.lava}
        self.platformsDraw: list[list[Platform]] = [self.grass, self.bounce, self.dive, self.bounce, self.lava]
        

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
        self.dayTime = True
        self.dayCycle = 60
        self.cycleStartTime = pygame.time.get_ticks()/1000
        self.newCycle = pygame.time.get_ticks()/1000
        self.day = (106,206,255)
        self.night = (0,0,102)
        self.startMiddle = True

        self.start = False
        self.WIDTH = 600
        self.HEIGHT = 900
        self.WHITE = (255,255,255)
        self.RED = (255, 0, 0)
        self.over = False
        self.won = False
        self.walkCount = 500

        self.lives = 5
        self.nightsTook = 0
        self.level = 3
        
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.livesImage = pygame.image.load("lives.png")
        self.livesImage = pygame.transform.scale(self.livesImage,(25,50))

        pygame.mixer.music.load("Intro.wav")
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play(-1)

        self.burned = pygame.mixer.Sound("burned.wav")
        self.burned.set_volume(0.2)
        self.lava = pygame.mixer.Sound("lava.wav")
        self.lava.set_volume(0.5)
        self.jumpSound = pygame.mixer.Sound("bounce.wav")
        self.jumpSound.set_volume(0.2)
        self.landSound = pygame.mixer.Sound("land.wav")
        self.landSound.set_volume(0.2)
        self.walkingSound = pygame.mixer.Sound("walking.wav")
        self.walkingSound.set_volume(0.2)

        self.introImage = pygame.image.load("introBg.png")
        self.introBg = pygame.transform.scale(self.introImage,(self.WIDTH,self.HEIGHT))
        self.fonts = {"Big":pygame.font.SysFont("Ariel Black",40),
                "Small":pygame.font.SysFont("Ariel Black",24),
                "Medium":pygame.font.SysFont("Ariel Black",30),
                "Title":pygame.font.SysFont("impact",50)
                     }

        
        
        self.levels: list[Level] = [
            None, #so that we can index using the self.level
            Level(
                1, 
                (30, 450),
                (500, 200),
                grass = [Grass(30, 500, 2), Grass(130, 450, 2), Grass(230, 400, 2), Grass(400, 350, 2)],
                lava = [Lava(0, 800, 24, 4)]
                ),
            Level(
                2,
                (30, 450),
                (500, 200),
                grass = [Grass(30,500, 2), Grass(400, 600, 2)],
                bounce= [Bounce(200, 500, 2), Bounce(500, 450, 2)],
                lava = [Lava(0, 800,24,4), Lava(400, 325,1, 3)]
            ),
            Level(
                3,
                (30, 800),
                (30, 100),  
                grass=[Grass(30, 850, 3), Grass(30, 550, 3), Grass(200, 450, 2), Grass(275, 375, 2)],
                bounce=[Bounce(150, 700, 2), Bounce(150, 200, 2), Bounce(400,650,2), Bounce(400, 300, 2), Bounce(525, 475,2)],
                dive = [Dive(275,200, 2)],
                lava=[Lava(0, 900, 24, 4), Lava(150, 225, 9), Lava(375, 225, height=5 )]
            ),
            Level(
                4,
                (30, 100),
                (500, 100),
                grass=[Grass(30, 150, 2), Grass(130, 600), Grass(350, 700)],
                bounce = [Bounce(230, 700, 2), Bounce(500,600,2), Bounce(420, 450, 2), Bounce(500, 300, 2)],
                dive = [Dive(325,550,2)],
                lava = [Lava(0, 800,24,4), Lava(250, 100, 5, 18), Lava(500, 425,2), Lava(420, 275,2)],
                playLava = True
            )
        ]
        
        self.player = Player(self.levels[self.level].playerSpawn[0], self.levels[self.level].playerSpawn[1])
        self.bed = Bed(self.levels[self.level].bedSpawn[0], self.levels[self.level].bedSpawn[1])

    def reset(self):
        self.player.x, self.player.y = self.levels[self.level].playerSpawn
        self.lives -= 1
        self.player.jumped = False
        if self.lives == 0:
            self.gameOver()

    def playAgain(self):
        self.lives = 5
        self.nightsTook = 0
        self.won = False
        self.over = False
        self.walkCount = 500
        self.dayTime = True
        self.cycleStartTime = pygame.time.get_ticks()/1000
        self.newCycle = pygame.time.get_ticks()/1000
        self.startMiddle = True

        self.level = 0
        self.nextLevel()
        
        
    def introScreen(self):
        text = self.fonts["Title"].render("Press SPACE to Continue",1,self.RED)
        title = self.fonts["Title"].render("Mario Slumber Party: ", 1, self.WHITE)
        subtitle = self.fonts["Medium"].render("Help Mario get some well deserved rest!", 1, self.WHITE)
        self.surface.blit(self.introBg, (0,0))
        self.surface.blit(text, (45, 700))
        self.surface.blit(title, (80, 550))
        self.surface.blit(subtitle, (90,620))

    def gameOver(self):
        self.over = True
        self.surface.fill((0,0,0))
        if self.won:
            text = self.fonts["Title"].render("YOU WON!!", 1, self.RED)
        else:
            text = self.fonts["Title"].render("YOU LOST!", 1, self.RED)
        
        marioSleepy = self.fonts["Medium"].render("Nights Missed: " + str(self.nightsTook), 1, self.WHITE)
        text1 = self.fonts["Title"].render("Press SPACE to Play Again",1,self.WHITE)
        text2 = self.fonts["Medium"].render("Press ESC to leave", 1, self.WHITE)

        self.surface.blit(marioSleepy, (self.WIDTH//2-75, self.HEIGHT//2-15))
        self.surface.blit(text, (self.WIDTH//2-100, self.HEIGHT//2-125))
        self.drawLives(self.HEIGHT//2-75)
        self.surface.blit(text1, (self.WIDTH//2-250, self.HEIGHT//2+20))
        self.surface.blit(text2, (self.WIDTH//2-85, self.HEIGHT//2+95))
        pygame.display.update()
        


        pass

    def drawBg(self):
        starSpeed = ((self.WIDTH+2*30)/self.dayCycle) * 2
        timePassed = pygame.time.get_ticks()/1000 - self.cycleStartTime
        curCycle = pygame.time.get_ticks()/1000 - self.newCycle
        pos = (timePassed % self.dayCycle) / self.dayCycle
        transition = (sin(pos * pi * 2 - pi / 2) + 1) / 2
        r = int(self.day[0] * (1 - transition) + self.night[0] * transition)
        g = int(self.day[1] * (1 - transition) + self.night[1] * transition)
        b = int(self.day[2] * (1 - transition) + self.night[2] * transition)
        self.surface.fill((r,g,b))
 

        if self.dayTime: #draw sun
            if self.startMiddle:
                sunX = self.WIDTH//2 + 30 - starSpeed * curCycle
            else:
                sunX = self.WIDTH + 30 - starSpeed * curCycle
            pygame.draw.circle(self.surface, (255, 255, 0), (int(sunX), 100), 30)
            if sunX <= -30 and self.dayTime:
                self.startMiddle = False
                self.dayTime = False

                self.newCycle = pygame.time.get_ticks()/1000
        else: #draw moon
            moonX = self.WIDTH + 30 - starSpeed * curCycle
            pygame.draw.circle(self.surface, (150, 150, 150), (int(moonX), 100), 30)
            if moonX <= -30 and not self.dayTime:
                self.nightsTook += 1
                self.dayTime = True
                moonX = self.WIDTH + 30
                self.newCycle = pygame.time.get_ticks()/1000

    def drawLives(self, y):
        offset = 0
        for i in range(self.lives):
            self.surface.blit(self.livesImage, (self.WIDTH//2-(self.lives*32//2) + offset, y))
            offset += 35
        offset = 0

    def drawAll(self):
        if not self.start:
            self.introScreen()
        else:
            self.drawBg()
            self.drawLives(5)
            self.player.draw(self.surface)
            self.bed.draw(self.surface)
            for platform in self.levels[self.level].platformsDraw:
                if platform != None:
                    for block in platform:
                        block.draw(self.surface) 

    def unSinkPlayer(self):
        while self.player.collide(self.levels[self.level].platforms["grass"]):
            self.player.y -= 1
        self.player.y += 1 #player needs to be barely touchign grass so he can jump

    def sinkPlayer(self):
        while self.player.collide(self.levels[self.level].platforms["grass"]):
            self.player.y += 1

    

    def gameCollide(self, type):
        return self.player.collide(self.levels[self.level].platforms[type])
    
    def bedCollide(self):
        if self.bed.collide(self.player):
            self.nextLevel()

    def sideGrassCollide(self):
        return self.player.grassCollide(self.levels[self.level].platforms["grass"])
    
    def headGrassCollide(self):
        return self.player.headCollide(self.levels[self.level].platforms['grass'])
    
    def nextLevel(self):
        if self.level != len(self.levels)-1:
            self.level += 1
            self.player.x, self.player.y = self.levels[self.level].playerSpawn
            self.bed.x, self.bed.y = self.levels[self.level].bedSpawn
            if self.levels[self.level].playLava:
                self.lava.play()
        else:
            self.won = True
            self.gameOver()
        


