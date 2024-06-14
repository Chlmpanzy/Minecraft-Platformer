from Classes import*
import pygame
pygame.init()
from math import *
sunk = False
x = True
game = Game()

def redraw():
    game.surface.fill((0,0,0))
    game.drawAll()
    pygame.display.update()

while x == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x = False
        if not game.start and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.start = True
                    
    if game.start:
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and game.gameCollide("grass"):
                
                game.player.Vy = game.player.jumpSpeed

        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and game.player.x > 0:
            if not game.sideGrassCollide():
                game.player.moveLeft()
                if game.gameCollide("grass"):
                    if game.walkCount >= 500:
                        game.walkingSound.play()
                        game.walkCount = 0
                if game.gameCollide("grass"):
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
                if game.gameCollide("grass"):
                    game.player.frame = game.player.nextRightPic[game.player.frame]
            while game.sideGrassCollide():
                game.player.moveLeft(False)

        elif game.gameCollide("grass"):
            if game.player.facing == 'right':
                game.player.frame = 4
            else:
                game.player.frame = 0
        
        if game.gameCollide("bounce"):
            game.player.Vy = -30
            game.jumpSound.play()
            
        if game.gameCollide("dive"):
            game.player.Vy = 30
            game.jumpSound.play()

        if game.gameCollide("lava"):
            game.player.Vy = 0
            game.burned.play()
            game.reset()
            
            
        game.player.Vy += game.player.gravity
        game.player.y += game.player.Vy

        if game.gameCollide("grass"):
            if game.player.jumped:
                game.landSound.play()
                game.player.jumped = False
            game.player.gravity = 0
            game.player.Vy = 0
            if sunk:
                game.unSinkPlayer()
                sunk = False
        else:
            game.player.jumped = True
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
