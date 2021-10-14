import time
import pygame
import numpy
from balle import Bullet

class Doodle:
    def __init__(self,game):
        self.game=game
        self.size=(96,105)
        self.x=0
        self.minX=-round(self.size[0]*0.66)#go to other side when 33% of doodle is displayed
        self.maxX=self.game.res[0]-(self.size[0]-abs(self.minX))#adjust automatically
        self.y=0
        self.lookRight=True
        self.maxYSpeed=1200
        self.velY=0
        self.image=pygame.transform.scale(pygame.image.load("moodle.png"),self.size)#load this picture in size pixels
        self.imgFlip=pygame.transform.flip(self.image,True,False)#load this picture in size pixels(self.image,True,False)
        self.speed=20
        self.left=False
        self.right=False
        self.mbtn=False
        self.mbtnAlreadyTrue=False
        self.mouseX=0
        self.bullets=[]
        self.bulletSize=(20,20)
        self.bulletTime=0#for picture switch test

    def Tick(self):
        if (self.left==True and self.right==True)or(self.left==False and self.right==False):#don't move
            pass
        elif self.left==True:
            self.lookRight=False
            self.x=max(self.x-(1*self.speed),self.minX)#cannot exit window left
            if self.x==self.minX:#go to other side
                self.x=self.maxX
        else:
            self.lookRight=True
            self.x=min(self.x+(1*self.speed),self.maxX)#cannot exit window right
            if self.x==self.maxX:#go to other side
                self.x=self.minX

                #####BULLETS#####
        if self.mbtn==True and self.mbtnAlreadyTrue==False:
            if self.mouseX<self.game.res[0]//3:#mouse in left part of screen
                self.SpawnBullet(0)
                print("left")
            elif self.mouseX>self.game.res[0]//3*2:#mouse in right part of screen
                self.SpawnBullet(2)
                print("right")
            else:#mouse in middle part of screen
                self.SpawnBullet(1)
                print("middle")
            self.mbtnAlreadyTrue=True

        if self.bulletTime!=0 and time.time()>=self.bulletTime+0.5:#if doodle shooted a bullet 0.5 seconds before
            self.image=pygame.transform.scale(pygame.image.load("moodle.png"),self.size)
            self.imgFlip=pygame.transform.flip(self.image,True,False)
            self.bulletTime=0#reset "timer"

        for b in self.bullets:#updates all bullets position
            b.Tick()

        self.Gravity()
        if self.velY>=0:#gravity downward
            self.game.SearchCollisions()
        return
    
    def render(self):
        if self.lookRight==True:
            return self.image
        else:
            return self.imgFlip
            
    def Gravity(self):
        self.velY=numpy.clip(self.velY+50,-self.maxYSpeed,self.maxYSpeed)
        if self.y>=self.game.res[1]/2 or self.velY>=0:#only apply gravity if player is in the bottom part of the screen or downward gravity
            self.y+=self.velY*self.game.fps#same movement at any framerate
        #print(self.velY)
        return
    
    def SpawnBullet(self,state):#change doodle picture depending on area clicked (and updates flipped version too)
        if state==0:
            self.bullets.append(Bullet(self.game,self.x+(self.size[0]//2)-(self.bulletSize[0]//2),self.y-self.bulletSize[1],self.bulletSize,(-0.5,-1)))#to the left
            self.image=pygame.transform.scale(pygame.image.load("moodleRight.png"),self.size)
            self.image=pygame.transform.flip(self.image,True,False)#update flipped version
        elif state==1:
            self.bullets.append(Bullet(self.game,self.x+(self.size[0]//2)-(self.bulletSize[0]//2),self.y-self.bulletSize[1],self.bulletSize,(0,-1)))#to middle
            self.image=pygame.transform.scale(pygame.image.load("moodleUp.png"),self.size)
        elif state==2:
            self.bullets.append(Bullet(self.game,self.x+(self.size[0]//2)-(self.bulletSize[0]//2),self.y-self.bulletSize[1],self.bulletSize,(0.5,-1)))#to the right
            self.image=pygame.transform.scale(pygame.image.load("moodleRight.png"),self.size)
        else:
            raise ValueError("bullet state must be 0,1 or 2")
        self.imgFlip=pygame.transform.flip(self.image,True,False)#update flipped version
        self.bulletTime=time.time()
        return
            
    def MakeRect(self):
        return pygame.Rect(self.x,self.y,self.size[0],self.size[1])