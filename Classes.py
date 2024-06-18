import pygame
pygame.init()
from math import *

        

class Block():
    def __init__(self, type, x,y):
        #initialize block
        self.type = type
        self.image = pygame.image.load(self.type+".png")
        self.image = pygame.transform.scale(self.image,(25,25))
        self.x = x
        self.y = y

    def draw(self, surface: pygame.Surface):
        '''
        Draws a block of the corresponding type on given surface
        (pygame.Surface) -> None
        '''
        surface.blit(self.image, (self.x, self.y))


class Platform():
    def __init__(self, type, x, y, length, height):
        #initialize Platform
        self.blocks: list[Block] = []
        self.type = type
        self.x = x
        self.y = y
        lengthOffset = 0
        heightOffest = 0
        self.length = length
        self.height = height
        for i in range(self.length):
            for j in range(self.height):
                self.blocks.append(Block(self.type, self.x + lengthOffset,self.y + heightOffest))
                heightOffest += 25 #since each block is 25x25 we need to move the next block by 25 to create a continous collum
            heightOffest = 0 #reset heigh offset back to 0 once done a collum
            lengthOffset += 25 #same logic as height offset

    def draw(self, surface):
        '''
        Draws every block in the platform on given surface
        (pygame.Surface) -> None
        '''
        for block in self.blocks:
            block.draw(surface)
    
class Bounce(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "bounce", x, y, length, height)
        #Init a Platform and give it type "bounce"


class Grass(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "grass", x, y, length, height)
        #Init a Platform and give it type "grass"

class Dive(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "dive", x, y, length, height)
        #Init a Platform and give it type "dive"

class Lava(Platform):
    def __init__(self, x, y, length = 1, height = 1):
        Platform.__init__(self, "lava", x, y, length, height)
        #Init a Platform and give it type "lava"

class Player():
    def __init__(self, x: int, y: int):
        #initialize player
        self.facing = 'right'
        self.Vy = 0
        self.jumpSpeed = -20
        self.gravity = 2
        self.x = x
        self.y = y
        self.frame = 0
        self.frames = []
        self.inAir = False

        for x in range(10):
            #Each frame for mario
            self.frames.append(pygame.transform.scale(pygame.image.load("mario"+str(x)+".png"), (25,50)))

        #Frame Sequences
        self.nextRightPic = [4, 4, 4, 4, 5, 6, 7, 5, 4, 4]
        self.nextLeftPic = [1, 2, 3, 1, 1, 1, 1, 1, 1, 1]
  

    def draw(self, surface: pygame.Surface):
        '''
        Draws player on given surface
        (pygame.Surface) -> None
        '''
        surface.blit(self.frames[self.frame],(self.x,self.y))
    
    def moveRight(self, change = True):
        '''
        Moves player 10 pixels right
        (Bool) -> None
        '''
        self.x += 10
        if change:
            self.facing = 'right'

    def moveLeft(self, change = True):
        '''
        Moves player 10 pixels left
        (Bool) -> None
        '''
        self.x -=10
        if change:
            self.facing = 'left'

    def collide(self, platforms: list[Platform]):
        '''
        Returns wether or not the player is colliding with any platforms
        (list[Platforms]) -> Bool
        '''
        playerRect = pygame.Rect(self.x, self.y, 25, 50)
        if platforms == None: #Level may not have a type of platform
            return False
        for platform in platforms:
            for block in platform.blocks:
                blockRect = pygame.Rect(block.x, block.y, 25, 25)
                if playerRect.colliderect(blockRect):
                    return True
        return False
    
    def grassCollide(self, platforms: list[Platform]):
        '''
        Returns wether or not the player collides on the side of a grass platform
        (list[Platform]) -> Bool
        '''
        playerRect = pygame.Rect(self.x, self.y, 25, 45) 
        if platforms == None: #Level May not have grass Platforms
            return False
        for platform in platforms:
            for block in platform.blocks:
                blockRect = pygame.Rect(block.x, block.y, 25, 25)
                if playerRect.colliderect(blockRect):
                    return True
        return False
    
    def headCollide(self, platforms: list[Platform]):
        if self.inAir:
            playerRect = pygame.Rect(self.x+2.5, self.y, 20, 20)
            if platforms == None:
                return False
            for platform in platforms:
                for block in platform.blocks:
                    blockRect = pygame.Rect(block.x, block.y, 25, 25)
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
        self.dayCycle = 45
        
        self.day = (106,206,255)
        self.night = (0,0,102)
        self.startMiddle = True
        self.winImage = pygame.transform.scale(pygame.image.load("MarioSleep.png"), (200,200))
        self.loseImage = pygame.transform.scale(pygame.image.load("MarioSad.png"), (200,200))

        self.info = False
        self.start = False
        self.WIDTH = 600
        self.HEIGHT = 900
        self.WHITE = (255,255,255)
        self.RED = (255, 0, 0)
        self.over = False
        self.won = False
        self.walkCount = 500
        self.divePlayed = self.bouncePlayed = False

        self.lives = 10
        self.nightsTook = 0
        self.level = 1
        
        
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
                (30, 451), (500, 200),
                grass = [Grass(30, 500, 2), Grass(130, 450, 2), Grass(230, 400, 2), Grass(400, 350, 2)],
                lava = [Lava(0, 800, 24, 4)]
                ),
            Level(
                2,
                (30,751), (500,100),
                grass = [Grass(0, 800, 24, 4), Grass(80,775)],
                bounce = [Bounce(100, 650, 2), Bounce(270, 500, 2), Bounce(440, 350, 2)],
                dive = [Dive(185, 525, 2), Dive(355, 375, 2)],
                lava = [Lava(105, 775,21)]
            ),
            Level(
                3,
                (30, 451), (500, 200),
                grass = [Grass(30,500, 2), Grass(400, 600, 2)],
                bounce= [Bounce(200, 500, 2), Bounce(500, 450, 2)],
                lava = [Lava(0, 800,24,4), Lava(400, 325,1, 3)]
            ),
            Level(
                4, #This is called the "Ms G Level" Good Luck! :) (because you always complain my games aren't hard enough)
                (30, 451), (500, 450),
                grass = [Grass(30,500, 2), Grass(230,500,1), Grass(405, 500, 2)],
                bounce = [Bounce(80,500,6)],
                dive = [Dive(255,500,6)],
                lava = [Lava(0, 700, 24, 4), Lava(0,200,24,4)],
                playLava = True
            ),
            Level(
                5,
                (30, 451), (450, 450),
                grass = [Grass(30,500, 2), Grass(30, 400, 2)],
                bounce = [Bounce(150,575,2), Bounce(300,575,2), Bounce(400, 575, 2)],
                dive = [Dive(225,375,2), Dive(350, 375, 2), Dive(425, 375, 2)],
                lava = [Lava(0, 600, 24, 4), Lava(0,275,24,4)],
                playLava=True
            ),
            Level(
                6,
                (30,751), (500, 725),
                grass = [Grass(0, 800, 24, 4)],
                bounce = [Bounce(105, 775, 3), Bounce(355, 775, 3)],
                dive = [Dive(255,550,1)],
                lava = [Lava(105, 600, 3), Lava(230, 525,3), Lava( 355, 600, 3)]
            ),
            Level(
                7,
                (30, 801), (30, 100),  
                grass=[Grass(30, 850, 3), Grass(30, 550, 3), Grass(200, 450, 2), Grass(275, 375, 2)],
                bounce=[Bounce(150, 700, 2), Bounce(150, 200, 2), Bounce(400,650,2), Bounce(400, 300, 2), Bounce(525, 475,2)],
                dive = [Dive(275,200, 2)],
                lava=[Lava(0, 875, 24), Lava(150, 225, 9), Lava(375, 225, height=5 )],
                playLava=True
            ),
            Level(
                8,
                (30, 101), (500, 100),
                grass=[Grass(30, 150, 2), Grass(130, 600), Grass(350, 700)],
                bounce = [Bounce(230, 700, 2), Bounce(500,600,2), Bounce(420, 450, 2), Bounce(500, 300, 2)],
                dive = [Dive(325,550,2)],
                lava = [Lava(0, 800,24,4), Lava(250, 100, 5, 18), Lava(500, 425,2), Lava(420, 275,2)],
                playLava = True
            )
        ]
        self.currentLevel = self.levels[self.level]
        self.player = Player(self.currentLevel.playerSpawn[0], self.currentLevel.playerSpawn[1])
        self.bed = Bed(self.currentLevel.bedSpawn[0], self.currentLevel.bedSpawn[1])
    def starting(self):
        '''
        This function starts counters, so that they arent going before they actully start the game
        (self) -> None
        '''
        self.cycleStartTime = pygame.time.get_ticks()/1000
        self.newCycle = pygame.time.get_ticks()/1000
        self.start = True

    def reset(self):
        '''
        This Functions resets player to his spawn coord when they die dies
        (self) -> None
        '''
        self.player.x, self.player.y = self.currentLevel.playerSpawn
        self.lives -= 1
        self.player.inAir = False
        self.player.Vy = 0
        if self.lives == 0:
            self.gameOver()

    def playAgain(self):
        '''
        This Functions resets all necessary game values so that player can play again
        () -> None
        '''
        self.lives = 10
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
        '''
        This function draws the intro screen
        () -> None
        '''
        text = self.fonts["Title"].render("Press SPACE to Continue",1,self.RED)
        title = self.fonts["Title"].render("Mario Slumber Party: ", 1, self.WHITE)
        subtitle = self.fonts["Medium"].render("Help Mario get some well deserved rest!", 1, self.WHITE)
        info = self.fonts["Medium"].render("Press i for the Games Instructions", 1, self.WHITE)
        self.surface.blit(self.introBg, (0,0))
        self.surface.blit(text, (45, 700))
        self.surface.blit(title, (80, 550))
        self.surface.blit(subtitle, (90,620))
        self.surface.blit(info, (110, 650))

    def gameOver(self):
        '''
        Draws the Game Over screen
        () -> None
        '''
        self.over = True
        self.surface.fill((0,0,0))
        if self.won:
            text = self.fonts["Title"].render("YOU WON!!", 1, self.RED)
            image = self.winImage
        else:
            image = self.loseImage
            text = self.fonts["Title"].render("YOU LOST!", 1, self.RED)
        
        marioSleepy = self.fonts["Medium"].render("Nights Missed: " + str(self.nightsTook), 1, self.WHITE)
        text1 = self.fonts["Title"].render("Press SPACE to Play Again",1,self.WHITE)
        text2 = self.fonts["Medium"].render("Press ESC to leave", 1, self.WHITE)

        self.surface.blit(image, (self.WIDTH//2-100, 100))
        self.surface.blit(marioSleepy, (self.WIDTH//2-75, self.HEIGHT//2-15))
        self.surface.blit(text, (self.WIDTH//2-100, self.HEIGHT//2-125))
        self.drawLives(self.HEIGHT//2-75)
        self.surface.blit(text1, (self.WIDTH//2-250, self.HEIGHT//2+20))
        self.surface.blit(text2, (self.WIDTH//2-85, self.HEIGHT//2+95))
        pygame.display.update()
        

    def drawBg(self):
        '''
        Draws the day cycle as well as the moving sun and moon
        () -> None
        '''
        starSpeed = ((self.WIDTH+2*30)/self.dayCycle) * 2 #Make sure stars move at a speed that will get them across the screen in 1 cycle


        timePassed = pygame.time.get_ticks()/1000 - self.cycleStartTime
        curCycle = pygame.time.get_ticks()/1000 - self.newCycle
        pos = (timePassed % self.dayCycle) / self.dayCycle # gives us a number between [0,1] to represent where we are on the sign function
        transition = (sin(pos * pi * 2 - pi / 2) + 1) / 2 #this of the sun and moon like a sign wave going up and down, where the top of the function is the sun out and the bottome it the moon out)
        
        #interpolation
        r = int(self.day[0] * (1 - transition) + self.night[0] * transition)
        g = int(self.day[1] * (1 - transition) + self.night[1] * transition) #we then calculate are new rgb values using the base colours for night and day we defined before as guidlines
        b = int(self.day[2] * (1 - transition) + self.night[2] * transition)
        self.surface.fill((r,g,b))
 

        if self.dayTime: #draw sun
            if self.startMiddle:
                sunX = self.WIDTH//2 - starSpeed * curCycle
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

    def drawLives(self, y: int):
        '''
        Draw Marios lives left
        (int) -> None
        '''
        offset = 0
        for i in range(self.lives):
            self.surface.blit(self.livesImage, (self.WIDTH//2-(self.lives*32//2) + offset, y))
            offset += 35 #spacing between each life

    def infoScreen(self):
        '''
        Draws the info screen
        () -> None
        '''
        self.surface.fill((0,0,0))
        text1 = self.fonts["Medium"].render("Help Mario go to sleep by getting to the bed each level",1,self.WHITE)
        text2 = self.fonts["Medium"].render("You'll need to traverse through a variety of plataforms", 1, self.WHITE)
        Grass(100,700,2).draw(self.surface)
        grassText = self.fonts["Small"].render("1. Grass block, safe to land and jump from", 1, self.WHITE)
        Bounce(200, 700, 2).draw(self.surface)
        bounceText = self.fonts["Small"].render("2. Bounce block, will propel you up when landed on, regardless of", 1, self.WHITE)
        bounceText2 = self.fonts["Small"].render("wether or not you jump", 1, self.WHITE)
        Dive(300, 700, 2).draw(self.surface)
        diveText = self.fonts["Small"].render("3. Dive block, will propel you down when landed on, notice how the", 1, self.WHITE)
        diveText2 = self.fonts["Small"].render("dots on the dive differ from the bounce to tell them apart", 1, self.WHITE)
        Lava(400, 700, 2).draw(self.surface)
        lavaText = self.fonts["Small"].render("4. Lava block, not safe to land on, you'll reset the level and lose a life", 1, self.WHITE)
        self.drawLives(190)
        lives = self.fonts["Small"].render("You start with 10 lives, once all lives are lost you'll have to restart the game", 1, self.WHITE)

        self.surface.blit(text1, (30, 100))
        self.surface.blit(text2, (30, 150))
        self.surface.blit(lives, (20, 250))
        self.surface.blit(grassText, (30, 400))
        self.surface.blit(bounceText, (30, 450))
        self.surface.blit(bounceText2, (30, 470))
        self.surface.blit(diveText, (30, 520))
        self.surface.blit(diveText2, (30, 540))
        self.surface.blit(lavaText, (30, 590))
        

    def drawAll(self):
        '''
        Uses all of the Game draw function and draws the entire game
        () -> None
        '''
        if not self.start:
            if self.info:
                self.infoScreen()
            else:
                self.introScreen()
        else:
            self.drawBg()
            self.drawLives(5)
            self.player.draw(self.surface)
            self.bed.draw(self.surface)
            for platforms in self.currentLevel.platformsDraw:
                if platforms != None:
                    for platform in platforms:
                        platform.draw(self.surface) 

    def unSinkPlayer(self):
        '''
        This functions ensures player dont sink into platforms when gravity get really fast
        () -> None
        '''
        while self.player.collide(self.currentLevel.platforms["grass"]):
            self.player.y -= 1
        self.player.y += 1 #player needs to be barely touchign grass so he can jump

    def sinkPlayer(self):
        '''
        This functions ensures player cant jump through platforms, by sinking them if there heads collide with one
        () -> None
        '''
        while self.player.collide(self.currentLevel.platforms["grass"]):
            self.player.y += 1

    

    def gameCollide(self, type):
        '''
        Returns wether or not there is a collisions betweren the player and platforms
        (str) -> Bool
        '''
        return self.player.collide(self.currentLevel.platforms[type])
    
    def bedCollide(self):
        '''
        Checks for collisions between the player and the bed
        () -> None
        '''
        if self.bed.collide(self.player):
            self.nextLevel()

    def sideGrassCollide(self):
        '''
        Return wether or not the player is colliding with the side of a grass platform
        () -> Bool
        '''
        return self.player.grassCollide(self.currentLevel.platforms["grass"])
    
    def headGrassCollide(self):
        '''
        Return wether or not a players head is colliding with the bottom of a grass platform
        () -> Bool
        '''
        return self.player.headCollide(self.currentLevel.platforms['grass'])
    
    def nextLevel(self):
        '''
        Increments Level, also ends game if final level reached
        () -> None
        '''
        if self.level != len(self.levels)-1:
            self.level += 1
            self.player.Vy = 0
            self.currentLevel = self.levels[self.level] #update current level
            self.player.x, self.player.y = self.currentLevel.playerSpawn
            self.bed.x, self.bed.y = self.currentLevel.bedSpawn
            if self.currentLevel.playLava:
                self.lava.play()
        else:
            self.won = True
            self.gameOver()
    
        


