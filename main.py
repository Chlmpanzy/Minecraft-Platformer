from Classes import*
import pygame
pygame.init()
from math import *
surface = pygame.display.set_mode((600, 900))


x = True
game = Game()


def redraw():
    surface.fill((0,0,0))
    game.drawAll(surface)
    pygame.display.update()

while x == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] and game.gameCollide("grass"):
            game.player.Vy = game.player.jumpSpeed

    if keys[pygame.K_LEFT] and game.player.x > 0:
        if not game.grassCollide():
            game.player.moveLeft()
        while game.grassCollide():
             game.player.moveRight()

    if keys[pygame.K_RIGHT] and game.player.x < 570:
       if not game.grassCollide():
            game.player.moveRight()
       while game.grassCollide():
            game.player.moveLeft()
    
    if game.gameCollide("bounce"):
         game.player.Vy = -30
        
    if game.gameCollide("dive"):
         game.player.Vy = 30

    if game.gameCollide("water"):
         game.player.Vy = 0
         game.reset()
         
        
    game.player.Vy += game.player.gravity
    game.player.y += game.player.Vy

    if game.gameCollide("grass"):
        game.player.gravity = 0
        game.player.Vy = 0
    else:
         game.player.gravity = 2

    game.bedCollide()

    redraw()
    game.clock.tick(30)
