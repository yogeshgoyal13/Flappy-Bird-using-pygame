import pygame
import time
import os
import random
import sys
pygame.font.init()

win_width = 500
win_height = 800

pygame.init()



BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))]

# BIRD_IMGS = [(pygame.image.load(os.path.join('imgs','bird1.png'))),(pygame.image.load(os.path.join('imgs','bird2.png'))),(pygame.image.load(os.path.join('imgs','bird3.png')))]

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs','bg.png')),(win_width,win_height))

class Bird :
    IMGS = BIRD_IMGS
    jump_sound = pygame.mixer.Sound(os.path.join('sounds','sfx_wing.wav'))
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 0
        self.height = y
        self.animation_duration = 5
        self.animation_count = 0
        self.img_count = 0
        self.img = self.IMGS[1]
        self.tick = 0
        self.max_rot = 25
        self.rot_vel = 10
        self.angle=0
        self.rotated_image=self.img
        self.soundTimer = 0
        self.soundTimerLim = 7

    def draw(self,win):
        self.move()
        if self.y<self.height and self.vel<0:
            self.angle=25
        elif self.y>self.height:
            self.angle-=self.rot_vel
            self.angle = max(self.angle,-90)
        rot_img = self.rot_center(self.img, self.angle)
        self.rotated_image=rot_img
        win.blit(rot_img,(self.x,self.y))

    def jump(self):
        if(self.soundTimer==0):
            pygame.mixer.Sound.play(self.jump_sound)
            self.soundTimer+=1
        if(self.soundTimer!=0) :
            self.soundTimer = (self.soundTimer+ 1)%self.soundTimerLim
        
        self.vel = -10
        self.height=self.y
        self.tick=0


    def move(self):
        self.tick+=1
        d = self.vel * self.tick + 0.5*self.tick**2
        if d>0 :
            d = max(16,d)
        self.y = self.height+d

        self.img = self.IMGS[(self.tick*self.animation_duration)%3]
 
    def rot_center(self, image, angle):
        """rotate a Surface, maintaining position."""

        loc = image.get_rect().center  #rot_image is not defined 
        rot_sprite = pygame.transform.rotate(image, angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite

    def get_mask(self):
        return pygame.mask.from_surface(self.rotated_image)

class Base :
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))

    def __init__(self):
        self.width = pygame.Surface.get_width(self.IMG)
        self.x1 = 0
        self.x2 = self.width
        self.y=700
        self.vel=5
    
    def move(self):
        self.x1-=self.vel
        self.x2-=self.vel

        if(self.x1+self.width)<0:
            self.x1=self.x2+self.width
            temp=self.x2
            self.x2=self.x1
            self.x1=temp

    def draw(self,win):
        self.move()
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
        
class Pipe:
    IMG_bottom = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
    IMG_top = pygame.transform.flip(pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png'))),False,True)
    IMG_height = pygame.Surface.get_height(IMG_bottom)
    IMG_width = pygame.Surface.get_width(IMG_bottom)
    

    def __init__(self):
        self.x=win_width
        self.y_bottom=0
        self.y_top=0
        self.gap = 200
        self.initcords()
        self.vel=5
        self.passed=False

    def initcords(self):
        self.y_bottom=random.randrange(200,win_width+self.gap)
        self.y_top=self.y_bottom-self.gap-self.IMG_height

    def move(self):
        self.x-=self.vel

    def draw(self,win):
        self.move()
        win.blit(self.IMG_bottom,(self.x,self.y_bottom))
        win.blit(self.IMG_top,(self.x,self.y_top))
    
    def collide(self,bird):
        bird_mask = bird.get_mask()
        toppipe_mask = pygame.mask.from_surface(self.IMG_top)
        bottompipe_mask = pygame.mask.from_surface(self.IMG_bottom)

        offset_top = (self.x-bird.x,self.y_top - round(bird.y))
        offset_bottom = (self.x-bird.x,self.y_bottom - round(bird.y))

        col_top = bird_mask.overlap(toppipe_mask,offset_top)
        col_bottom = bird_mask.overlap(bottompipe_mask,offset_bottom)

        if col_top or col_bottom:
            return True

        return False

class Score :
    pointsound = pygame.mixer.Sound(os.path.join('sounds','sfx_point.wav'))
    def __init__(self):
        self.val=0
    def inc(self):
        pygame.mixer.Sound.play(self.pointsound)
        self.val+=1

    def draw(self,win,font):
        text = font.render("Score - " + str(self.val),1,(255,255,255))
        win.blit(text,(win_width-200,50))

def pauseScreen(win,bird,score,pipes):
    die_sound = pygame.mixer.Sound(os.path.join('sounds','sfx_die.wav'))
    pygame.mixer.Sound.play(die_sound)
    run=True
    currentScore = largeFont.render('Score: '+ str(score.val),1,(255,255,255))
    instruction = smallFont.render("Press mouse button to play again",1,(255,255,255))
    print(score.val)
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        # win.blit(BG_IMG,(0,0))   
        win.blit(currentScore, (win_width/2 - currentScore.get_width()/2, 240))
        win.blit(instruction, (win_width/2 - instruction.get_width()/2 , 240 - 2*instruction.get_height()))
        pygame.display.update() 

    score = Score()
    bird = Bird(100,200)
    pipes= []

    return Score(),Bird(100,200),[]    
        
        

def win_draw(win,bird,base,pipes,score,font):
    win.blit(BG_IMG,(0,0)) #Background Image
    for pipe in pipes :
        pipe.draw(win)
    score.draw(win,font)
    base.draw(win)
    bird.draw(win) #Drawing Bird
    pygame.display.update() #Updating screen


def main():
    global largeFont, smallFont
    #Frame Rate 30FPS
    
    #Initalising window 
    win = pygame.display.set_mode((win_width,win_height))
    run=True
    #Initilaising moving floor
    base = Base()

    #Initiasling Bird Object
    bird = Bird(100,100)

    #Score
    font = pygame.font.SysFont('helvetica',30)
    largeFont = pygame.font.SysFont('helvetica', 80)
    smallFont = pygame.font.SysFont('helvetica', 20)

    score=Score()

    #pipestuff
    pipeTimer = 0
    pipeTimerLim = 90
    pipes = []

    pause=False
    clock = pygame.time.Clock()

    #Main Game Loop
    while run:
        clock.tick(60)
        # pygame.time.delay(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

        if pause :
            score,bird,pipes = pauseScreen(win,bird,score,pipes)
            pause=False
        
        if(pipeTimer==0):
            pipes.append(Pipe())
        pipeTimer=(pipeTimer+1)%pipeTimerLim

        for pipe in pipes:
            if pipe.x+pipe.IMG_width<bird.x and pipe.passed==False:
                score.inc()
                pipe.passed=True
            if pipe.collide(bird) or bird.y>700:
                pause=True
                # print("Collie bhai")
        
        keys = pygame.key.get_pressed()

        #Game Logic
        if keys[pygame.K_SPACE]:
            bird.jump()

        win_draw(win,bird,base,pipes,score,font)

main()

pygame.quit()