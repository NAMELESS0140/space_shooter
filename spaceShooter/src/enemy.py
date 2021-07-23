import pygame

class enemyShip:

    def __init__(self,WINDOWWIDTH):
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("ArtAssets7/ship.png"),(80,80)),False,True)
        self.rect = self.image.get_rect()

        self.moveSpeed = 3

        self.leftLimit = 10
        self.rightLimit = WINDOWWIDTH - 10
        self.topLimit = 40
        self.bottomLimit =  40
        
        self.setStartPos()
    
    def AImove(self,shipRect):
        if shipRect.left<=self.rect.left and self.rect.left >= self.leftLimit:
            self.rect.left -= self.moveSpeed
        if shipRect.right>=self.rect.right and self.rect.right <= self.rightLimit:
            self.rect.right += self.moveSpeed

        

    def setStartPos(self):
        xCoord = (self.rightLimit + self.leftLimit)/2
        yCoord = self.topLimit

        self.rect.center = (xCoord,yCoord)