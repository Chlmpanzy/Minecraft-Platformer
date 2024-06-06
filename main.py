from Classes import*
import pygame
pygame.init()
from math import *
surface = pygame.display.set_mode((600, 900))
grass = [Grass(5, 100, 500)]
bounce = [Bounce(2, 300, 500)]
dive = [Dive(4,300,300)]
water = [Water(int(600/25), 0, 800)]
player = Player(100,450)
clock = pygame.time.Clock()
x = True
game = Game()


def redraw():
    surface.fill((0,0,0))
    game.drawAll(surface, [grass, bounce, dive, water])
    player.draw(surface)
    pygame.display.update()

while x == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] and player.collide(grass):
            player.Vy = player.jumpSpeed

    if keys[pygame.K_LEFT] and player.x > 0:
        player.moveLeft()

    if keys[pygame.K_RIGHT] and player.x < 800:
        player.moveRight()
    
    if player.collide(bounce):
         player.Vy = -30
        
    if player.collide(dive):
         player.Vy = 30

    if player.collide(water):
         game.reset(player)
         pass
        
    player.Vy += player.gravity
    player.y += player.Vy

    if player.collide(grass):
        player.gravity = 0
        player.Vy = 0
    else:
         player.gravity = 2

    redraw()
    clock.tick(30)
    
    #if player.collide(grass, bounce, dive) == "fall":
     #   player.y -= 10
