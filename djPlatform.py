import pygame

class Platform:
    def __init__(self,game,x,y,size):
        self.x=x
        self.y=y
        self.size=size
        self.game=game
        self.image=pygame.transform.scale(pygame.image.load("platform.png"),self.size)#load this picture in size pixels
        return
        
    def Down(self,speed):
        self.y+=abs(speed*self.game.fps)
        if self.y>=self.game.res[1]:#if get outside of the screen at the bottom
            self.game.platforms.remove(self)#destroy self ???
            self.game.SpawnPlatform()
            return

    def MakeRect(self):
        return pygame.Rect(self.x,self.y,self.size[0],self.size[1])