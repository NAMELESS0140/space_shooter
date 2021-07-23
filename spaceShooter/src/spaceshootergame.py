# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 11:26:21 2019

@author: J. Tyler McGoffin
"""

import pygame, sys
import numpy as np
from pygame.locals import *
import time

from ship import Ship
from background import Background
from asteroid import Asteroid
from laser import Laser
from enemy import enemyShip

#Set up window and frame rate variables
FPS = 30
WINDOWWIDTH = 500
WINDOWHEIGHT = 700

#Set up some Color variables
BLACK = (0, 0, 0)
NAVYBLUE = (0, 0, 128)
DARKPURPLE = (100, 0, 100)
WHITE = (255, 255, 255)
DARKGRAY = (100, 100, 100)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Start the game
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT #True globals
    
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Space Shooter")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    #setup game
    score = 0
    lives = 3
    levelUp = False
    ships = 0

    
    #Create Game Objects: ship, asteroids, lasers, background
    playerShip = Ship(WINDOWWIDTH,WINDOWHEIGHT)
    leftHeld = False
    rightHeld = False
    upHeld = False
    downHeld = False
    firing = False



    #Lasers
    lasers = initializeObjects(15)
    laserIndex = 0
    laserSpeed = 10
    fireRate = 4 # lasers per second

    #Enemies
    #enemies = initializeObjects(1)
    enemyExist = False
    E_spawnRate = 0.1
    E_shootRate = 2
    #enemyIndex = 0

    #Lasers-Enemy
    lasersE = initializeObjects(10)
    laserEIndex = 0
    laserESpeed = 10

    #Asteroid stuff
    asteroids = initializeObjects(25)
    spawnRate = 1 # on average, we'll spawn 1 asteroid per second
    minAsteroidSpeed = 1
    maxAsteroidSpeed = 6
    asteroidIndex = 0

    backgroundObject = Background("background",WINDOWHEIGHT)
    paralaxObject = Background("paralax",WINDOWHEIGHT)

    #game loop
    while True:
        #event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_a or event.key ==K_LEFT:
                    leftHeld = True
                elif event.key == K_d or event.key ==K_RIGHT:
                    rightHeld = True
                elif event.key == K_w or event.key ==K_UP:
                    upHeld = True 
                elif event.key == K_s or event.key ==K_DOWN:
                    downHeld = True
                elif event.key ==K_SPACE:
                    firing = True                                                                               
            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_LEFT:
                    leftHeld = False
                elif event.key == K_d or event.key == K_RIGHT:
                    rightHeld = False
                elif event.key == K_w or event.key == K_UP:
                    upHeld = False
                elif event.key == K_s or event.key == K_DOWN:
                    downHeld = False
                elif event.key ==K_SPACE:
                    firing  = False
        
        #Increase game difficulty
        if score % 10 == 0 and levelUp:
            minAsteroidSpeed +=2
            maxAsteroidSpeed +=2
            spawnRate += 1
            levelUp = False
        elif score % 10 != 0:
            levelUp = True


        #Spawn asteroids and laserrs
        if firing:
            lasers[laserIndex]=Laser(playerShip.rect,laserSpeed)
            firing = False
            laserIndex += 1
            if laserIndex >= len(lasers):
                laserIndex = 0
        
        # automate asteroid spawning
        if np.random.randint(0,FPS/spawnRate) == 0:
            asteroids[asteroidIndex] = Asteroid(WINDOWWIDTH,WINDOWHEIGHT,np.random.randint(minAsteroidSpeed,maxAsteroidSpeed))
            asteroidIndex += 1
            if asteroidIndex >= 25:
                asteroidIndex = 0

        # spawn enemy
        if np.random.randint(0,FPS/E_spawnRate) == 0 and enemyExist == False:
            enemy = enemyShip(WINDOWWIDTH)
            #enemyIndex += 1
            enemyExist = True
        #if enemyIndex >= 1 and enemyExist == False:
            #enemyIndex = 0    
        
        #enemy firing
        if enemyExist == True and np.random.randint(0,FPS/E_shootRate) == 0:
            lasersE[laserEIndex] = Laser(enemy.rect,laserESpeed)
            laserEIndex += 1
            if laserEIndex >= len(lasersE):
                laserEIndex = 0


        #detect collision
        for currentAsteroidIndex, asteroid in enumerate(asteroids):
            if asteroid != None:
                for currentLaserIndex,laser in enumerate(lasers):
                    if laser != None:
                        if laser.rect.colliderect(asteroid.rect):
                            asteroids[currentAsteroidIndex] = None
                            lasers[currentLaserIndex] = None
                            score += 1
                        if enemyExist == True and laser.rect.colliderect(enemy.rect):
                            enemyExist = False
                            enemy = None
                            ships += 1
                            #lasersE = initializeObjects(10)
                if playerShip.rect.colliderect(asteroid.rect):
                    lives -= 1
                    if lives > 0:
                        playerHit()
                        playerShip.setStartPos()
                        asteroids = initializeObjects(25)
                        lasers = initializeObjects(15)
                        lasersE = initializeObjects(10)
                    else:
                        return
                    break
        #if enemyExist == True:
            for currentLasersEIndex, laserE in enumerate(lasersE):
                if laserE != None:
                    if laserE.rect.colliderect(playerShip.rect):
                        lives -= 1
                        lasersE[currentLasersEIndex] = None
                        if lives > 0:
                            playerHit()
                            playerShip.setStartPos()
                            asteroids = initializeObjects(25)
                            lasers = initializeObjects(15)
                            lasersE = initializeObjects(10)
                            enemyExist = False
                            enemy = None
                        else:
                            return
                        break
        #update state
        playerShip.move(left=leftHeld,right=rightHeld,up=upHeld,down=downHeld)
        backgroundObject.move()
        paralaxObject.move()
        for laser in lasers:
            if laser != None:
                laser.move()
        for asteroid in asteroids:
            if asteroid != None:
                asteroid.move()
        for laserE in lasersE:
            if laserE != None:
                laserE.move_E()
        if enemyExist == True:
            enemy.AImove(playerShip.rect)
            
        
        #draw on screen
        DISPLAYSURF.fill(BLACK)
        draw(backgroundObject.image,backgroundObject.rect)
        draw(paralaxObject.image,paralaxObject.rect)
        draw(imageSurf = playerShip.image,imageRect = playerShip.rect)
        drawAsteroids(asteroids)
        drawLasers(lasers)
        if enemyExist==True:
            draw(enemy.image,enemy.rect)
        drawLasersE(lasersE)
        drawHUD(lives,score,ships)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawHUD(lives,score,ships):
    healthBarSurf = BASICFONT.render("Ships remaining: " + str(lives),True,WHITE)
    healthBarRect = healthBarSurf.get_rect()
    healthBarRect.topleft = (10,10)
    draw(healthBarSurf,healthBarRect)

    scoreSurf = BASICFONT.render("Asteroids destroyed: " + str(score),True,WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH-10,10)
    draw(scoreSurf,scoreRect)

    shipSurf = BASICFONT.render("Enemies destroyed: " + str(ships),True,WHITE)
    shipRect = shipSurf.get_rect()
    shipRect.topright = (WINDOWWIDTH-10,30)
    draw(shipSurf,shipRect)

def draw(imageSurf,imageRect):
    DISPLAYSURF.blit(imageSurf,imageRect)

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 30)
    titleSurf1 = titleFont.render('SPACESHOOTER', True,  WHITE)
    #titleSurf2 = titleFont.render('SPACESHOOTER', True, RED)
    
    #degrees1 = 0
    #degrees2 = 0
    while(True): #looks like a game loop
        DISPLAYSURF.fill(BLACK)
        #rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        surfRect1 = titleSurf1.get_rect()
        surfRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        DISPLAYSURF.blit(titleSurf1, surfRect1)
        
        # rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        # rotatedRect2 = rotatedSurf2.get_rect()
        # rotatedRect2.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        # DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
        
        drawPressKeyMsg()
        
        if checkForKeyPress():
            pygame.event.get() #clear the event cache
            return
        pygame.display.update()
        #FPSCLOCK.tick(FPS)
        #degrees1 += 3
        #degrees2 += 7

def showGameOverScreen():
    gameOverFont = pygame.font.Font("freesansbold.ttf",100)
    gameSurf = gameOverFont.render("Game",True,WHITE)
    overSurf = gameOverFont.render("Over",True,WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH/2,(WINDOWHEIGHT/2)-50)
    overRect.midtop = (WINDOWWIDTH/2,400)

    DISPLAYSURF.blit(gameSurf,gameRect)
    DISPLAYSURF.blit(overSurf,overRect)
    drawPressKeyMsg()

    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def playerHit():
    hitSurf = BASICFONT.render("You've been destroyed!",True,WHITE)
    hitRect = hitSurf.get_rect()
    hitRect.center = (WINDOWWIDTH/2,WINDOWHEIGHT/2)
    draw(hitSurf,hitRect)

    pygame.display.update()
    pygame.time.wait(2000)

def terminate():
    pygame.quit()
    sys.exit()

def initializeObjects(number):
    objects=[]
    for x in range(number):
        objects.append(None)
    return objects

def drawLasers(lasers):
    for laser in lasers:
        if laser != None:
            draw(laser.image,laser.rect)

def drawLasersE(lasersE):
    for laserE in lasersE:
        if laserE != None:
            draw(laserE.image,laserE.rect)

def drawAsteroids(asteroids):
    for asteroid in asteroids:
        if asteroid != None:
            image,rect = asteroid.draw()
            draw(image,rect)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            else:
                return True
    return False

if __name__ == '__main__':
    main()