import random
import sys
import pygame
import pygame.mixer
from pygame.locals import *
import time

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
msize = 5
size = 20
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
playerx = (screenWidth-(size+20))/2
playery = screenHeight - size
velocityx = 0
mvely = 0
mvelx = 0
misx = playerx+((msize+25)/2)
GAME_SPRITES = {}
misy = screenHeight-size
pygame.display.set_caption("Space Aliens By Talha")
move = 0
bullets = []
alienList = []
# alienx = random.randint(0, 720)
# alieny = 0
# alien = pygame.image.load('sprites/alien.png').convert_alpha()
# alien1 = pygame.transform.scale(alien, (80, 100))
# alien1 = pygame.transform.scale(alien, (80, 100))
# GAME_SPRITES['aliens'] = (
#     pygame.image.load('gallery/sprites/alien.png.png').convert_alpha(),)

# def newBullet(misx, misy):
#     num_bullet = 5
#     for i in range(num_bullet):
#         i = newBullet(screenWidth/2 - 5, screenHeight - size - 20)
#         bullets.append(i)
#     pygame.draw.rect(
#         screen, white, [screenWidth/2 - 5, screenHeight - size - 20, size+20, size])


while True:

    # screen.blit(aliens, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        # elif event.type == KEYDOWN:
        #     alienList.append([random.randint(0, 720), 0])
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            velocityx = 5
            mvelx = 5
        elif event.type == KEYDOWN and event.key == K_LEFT:
            velocityx = -5
            mvelx = -5

        elif event.type == KEYDOWN and event.key == K_SPACE:
            velocityx = 0
            mvelx = 0
        elif event.type == KEYDOWN and event.key == K_UP:
            print(alienList)
            bullets.append([misx, misy])
            mvely = -10
            move += 1

    # alienx = random.randint(0, 720)

    while len(alienList) < 100:
        alienx = random.randint(0, 720)
        alienList.append([alienx, 0])

    playerx += velocityx
    for b in range(len(bullets)):
        bullets[b][1] += mvely

    for bullet in bullets:
        if bullet[1] < 0:
            bullets.remove(bullet)

    for bullet in bullets:
        pygame.draw.rect(
            screen, red, (bullet[0], bullet[1], msize, msize+20))
        pygame.display.update()

    # for i in range(2):
    #     alienx = random.randint(0, 720)
    #     alieny = random.randint(0, 720)
    #     alienList.append([alienx, alieny])
    #     time.sleep(3)

    if misy == (screenHeight - size):
        misx += mvelx
    else:
        pass

    #alienList.append([alienx, alieny])

    # for a in range(len(alienList)):
    #     alienList[a][1] += 1

    # for i in range(2):
    #alienList.append([alienx, alieny])

    # for al in alienList:
    #     screen.blit(alien1, (alienx, alieny))
    #     pygame.display.update()

    for a in range(len(alienList)):
        alienList[a][1] += 0.5

    for alien in alienList:
        pygame.draw.rect(
            screen, red, (alien[0], alien[1], 20, 20))
        pygame.display.update()

    for anya in alienList:
        if anya[0] < misx < (anya[0]+20) and misy == anya[1]+20:
            alienList.remove(anya)

    screen.fill(black)
    pygame.draw.rect(screen, white, [playerx, playery, size+20, size])
    #screen.blit(alien1, (0, 0))
    pygame.display.update()
    fpsClock.tick(fps)
