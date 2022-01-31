import time
import random
from doodle import Doodle
from djPlatform import Platform
from monstre import Monstre
import pygame

#60
class Jeu:
    def __init__(self,fps,resolution):
        if fps<1:
            raise ValueError("please set fps to at least 1")
        else:
            self.fps=1/fps#fps to frequence
        self.res=resolution

        pygame.init()
        pygame.display.set_icon(pygame.image.load("logo.jpg"))
        pygame.display.set_caption("Moodle Jump officiel")
        self.screen= pygame.display.set_mode((self.res[0],self.res[1]))
        
        self.score=0
        self.doodle=Doodle(self)
        self.doodle.x,self.doodle.y=self.res[0]/2-self.doodle.size[0]/2,self.res[1]/2
        self.background=self.TestImagePath("background.jpg")
        self.platformSize=(100,20)
        self.monsterSize=(100,100)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        self.monsters=[]
        
        self.platforms=[Platform(self,self.doodle.x,self.doodle.y+self.doodle.size[1],self.platformSize)]#spawn first platform under doodle
        for i in range(1,self.res[1],200): #space between platforms
            self.SpawnPlatform(self.res[1]-i)#spawn platforms
        
        while True:#game loop
            time.sleep(self.fps)
            
            #####VIDEO#####

            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.doodle.render(),(self.doodle.x,self.doodle.y))
            for p in self.platforms:
                self.screen.blit(p.image,(p.x,p.y))
            for m in self.monsters:
                self.screen.blit(m.image,(m.x,m.y))
            for b in self.doodle.bullets:
                self.screen.blit(b.image,(b.x,b.y))
            self.score=round(self.score)#round score before displaying
            self.screen.blit(self.myfont.render("SCORE:" + str(self.score), True, (0,0,0)),(120,0))
            pygame.display.update()
            
            #####OTHERS#####
            #for p in platforms:
                #delete if < screenRes
            self.Inputs()          
            self.doodle.Tick()#update doodle
            if self.doodle.y<self.res[1]/2:
                for p in self.platforms:
                    p.Down(self.doodle.velY)
                    self.score+=0.1
                for m in self.monsters:
                    m.Down(self.doodle.velY)
            elif self.doodle.y>self.res[1]:
                print("death")
                self.doodle=None
                self.doodle.y=0#insert death anim 
            
    def TestImagePath(self,imagePath):
        if not isinstance(imagePath,str):
            raise ValueError("please enter a correct image path")
        else:
            return pygame.image.load(imagePath)
            
    def Inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.doodle.left=True
                if event.key == pygame.K_RIGHT:
                    self.doodle.right=True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.doodle.left=False
                if event.key == pygame.K_RIGHT:
                    self.doodle.right=False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.doodle.mouseX,Null=pygame.mouse.get_pos()
                self.doodle.mbtn=True
            if event.type == pygame.MOUSEBUTTONUP:
                self.doodle.mbtn=False
                self.doodle.mbtnAlreadyTrue=False#do once
        return
                    
    def MakeCollidersList(self):
        temp=[]
        for p in self.platforms:
            temp.append(p.MakeRect())
        return temp
    
    def MakeMonstersList(self):
        temp=[]
        for m in self.monsters:
            temp.append(m.MakeRect())
        return temp

    def SearchCollisions(self):
        collisionIndex=self.doodle.MakeRect().collidelist(self.MakeCollidersList())
        monsterIndex=self.doodle.MakeRect().collidelist(self.MakeMonstersList())
        #print(collisionIndex)
        if self.doodle.y+self.doodle.size[1]<=self.platforms[collisionIndex].y+50:#collision 50 is for error treshold due to movement between frames ,no need to check if collision Index !=-1 fsr
            self.doodle.velY=-self.doodle.maxYSpeed#jump again
            #print("collision")
        if monsterIndex!=-1:
            self.doodle=None
        return
    
    def SpawnPlatform(self,y=0):   
        self.platforms.append(Platform(self,random.randint(0,self.res[0]-self.platformSize[0]),y,self.platformSize))#200 is platform X size, to change later
        if random.uniform(0,1)<=0.1:#10% luck
            self.monsters.append(Monstre(self,random.randint(0,self.res[0]-self.platformSize[0]),y,self.monsterSize))
        return
    
    
    


jeu=Jeu(60,(506,900))#607*1080 / 506*900 / 9*16 ratio
exitonclick()