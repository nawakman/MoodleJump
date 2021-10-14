import pygame

class Bullet:
    def __init__(self,game,x,y,size,vector):
        self.game=game
        self.x=x
        self.y=y
        self.size=size
        self.vector=vector
        self.speed=1500
        self.image=pygame.transform.scale(pygame.image.load("balle.png"),self.size)#load this picture in 20*20 pixels
        return
        
    def Tick(self):
        self.x+=self.vector[0]*self.speed*self.game.fps
        self.y+=self.vector[1]*self.speed*self.game.fps
        if self.x<0 or self.x>self.game.res[0] or self.y<0 or self.y>self.game.res[1]:#if get outside of the screen
            self.game.doodle.bullets.remove(self)#destroy self ???
        
    def MakeRect(self):
        return pygame.Rect(self.x,self.y,20,20)

    def collision(self):#wainting group work
        pass