from Classes import*
import pygame
pygame.init()
from math import *
sunk = False
x = True
down = False
game = Game()

def redraw():
    '''
    Draws game
    () -> None
    '''
    if not game.over:
        game.drawAll()
        pygame.display.update()

while x == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x = False
        if event.type == pygame.KEYDOWN:
            if not game.start:
                if event.key == pygame.K_SPACE:
                    game.starting()
                if event.key == pygame.K_i:
                    game.info = True
            if game.over:
                if event.key == pygame.K_SPACE:
                    game.playAgain()
                if event.key == pygame.K_ESCAPE:
                    x = False
                    
    if game.start and not game.over:
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and game.gameCollide("grass") and not down:
                game.player.Vy = game.player.jumpSpeed

        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and game.player.x > 0:
            if not game.sideGrassCollide():
                game.player.moveLeft()  
                if game.gameCollide("grass"):
                    if game.walkCount >= 500:
                        game.walkingSound.play()
                        game.walkCount = 0
                    game.player.frame = game.player.nextLeftPic[game.player.frame]
            while game.sideGrassCollide():
                game.player.moveRight(False)


        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and game.player.x < 570:
            if not game.sideGrassCollide():
                game.player.moveRight()
                if game.gameCollide("grass"):
                    if game.walkCount >= 500:
                        game.walkingSound.play()
                        game.walkCount = 0
                    game.player.frame = game.player.nextRightPic[game.player.frame]
            while game.sideGrassCollide():
                game.player.moveLeft(False)

        elif game.gameCollide("grass"):
            if game.player.facing == 'right':
                game.player.frame = 4
            else:
                game.player.frame = 0
        
        if game.gameCollide("bounce") and not game.bouncePlayed:
            game.player.Vy = -30
            game.jumpSound.play()
            game.bouncePlayed = True
        else:
            game.bouncePlayed = False
            
        if game.gameCollide("dive") and not game.divePlayed:
            game.player.Vy = 30
            game.jumpSound.play()
            game.divePlayed = True
        else:
            game.divePlayed = False

        if game.gameCollide("lava"):
            game.player.Vy = 0
            game.burned.play()
            game.reset()
            
        
        game.player.Vy += game.player.gravity
        game.player.y += game.player.Vy

        if game.player.Vy > 45:
            game.player.Vy = 45 #This is the fastest a player can fall before game starts glitching (Phase through platforms)
        

        if game.headGrassCollide() and game.player.Vy < 0:  #this way it only stops your motion if you arent already falling
            game.player.Vy = 0
            game.sinkPlayer()

                

        if game.gameCollide("grass"):
            if game.player.inAir:
                game.landSound.play()
                game.player.inAir = False
            game.player.gravity = 0
            game.player.Vy = 0
            if sunk:
                game.unSinkPlayer()
                sunk = False
        else:
            game.player.inAir = True
            if game.player.facing == 'right':
                    game.player.frame = 9
            else:
                game.player.frame = 8
            sunk = True
            game.player.gravity = 2

        game.bedCollide()
        game.walkCount += game.clock.get_time()
    

    redraw()
    game.clock.tick(30)
