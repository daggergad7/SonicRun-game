import pygame,os,sys,math,random
from pygame.locals import *     #USEREVENT
from f import *
from inputname import *
import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="book")
    #usrrname,password,db name
mycursor=mydb.cursor()
playerName=inpt()
print(playerName)
pygame.init()
bgc=1

bulletSound = pygame.mixer.Sound('music/bullet.wav')   #Sound supports only wavformat
hitSound=pygame.mixer.Sound('music/hit.wav')  #to play hitSound.play()       #hit enemy sound
dieSound=pygame.mixer.Sound('music/die.wav')
music=pygame.mixer.music.load('music/music1.mp3')
pygame.mixer.music.play(-1)   #-ve 1 to play continuously even if song ends

W, H = 800, 400
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')
bg=pygame.image.load('bg.png').convert()
bgX = 0
bgX2 = bg.get_width()               
clock = pygame.time.Clock()
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)

class player(object):
    run = [pygame.image.load('sonic1/'+str(x)+'.png') for x in range(1,9)]    
    jump = [pygame.image.load(os.path.join('sonic1/jump', str(x) + '.png')) for x in range(1,9)]
    slide = [pygame.image.load('sonic1/slide/'+str(x)+'.png') for x in range(1,12)]
    fall=pygame.image.load('sonic1/die22.png')
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        
        self.slideUp = False
        self.falling=False
        self.hitbox=(x,y,width,height)

    def draw(self, win):
        if self.falling:
            win.blit(self.fall,(self.x,self.y))

        elif self.jumping:                             #jump
            self.y -= self.jumpList[self.jumpCount] * 1.2           
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox=(self.x,self.y,self.width-24,self.height-10)          
        
        elif self.sliding or self.slideUp:       #sliding
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19  
                self.sliding = False
                self.slideUp = True
            elif self.slideCount>20 and self.slideCount<80:    #character lying down
                self.hitbox=(self.x,self.y+3,self.width-8,self.height-35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox=(self.x+4,self.y,self.width-24,self.height-10)
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))            
            self.slideCount += 1
        
        else:
            if self.runCount > 42:     #run
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox=(self.x+4,self.y,self.width-24,self.height-13)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class Enemy:
    walkLeft = [pygame.image.load('enemy/L'+str(x)+'E.png') for x in range(1,12)]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hitbox=(x,y,width,height)
        self.count=0
        self.walkCount=0
        self.vel=3  
        self.hitbox=(self.x+17,self.y+2,31,57)    #rectangle
        self.health= 10             
        self.visible=True
        self.p=0
        
    def draw(self,win):
        if self.visible:
            if self.walkCount +1 >= 33:
                self.walkCount=0           
            win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))         
            self.walkCount += 1           
        self.hitbox=(self.x+17,self.y+2,31,57)    #rectangle
 
    def collide(self,rect):  #hitbox
        if rect[0]+ rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:   #inside
            if rect[1]+rect[3]>self.hitbox[1]:  
                return True                   
        return False
    def hit(self):
        self.visible=False

class Dragon:    
    walkLeft = [pygame.image.load('sonic1/dragon/'+str(x)+'.png') for x in range(1,12)]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hitbox=(x,y,width,height)
        self.count=0
        self.walkCount=0
        self.vel=3  
        self.hitbox=(self.x,self.y,64,64)    #rectangle
        self.health= 10             
        self.visible=True
        
    def draw(self,win):
        if self.visible:
            if self.walkCount +1 >= 33:
                self.walkCount=0           
            win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))         
            self.walkCount += 1           
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))      #health is red uske upar green
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0],self.hitbox[1]-20,50 - (5*(10-self.health)),10))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        self.hitbox=(self.x,self.y,64,64)    #rectangle
 
    def collide(self,rect):  #hitbox
        if self.visible==True:
            if rect[1] < self.hitbox[1] + self.hitbox[3] and rect[1] + rect[3] > self.hitbox[1]:
                if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                    return True
        return False

    def hit(self):
        if(self.health>0):
        	self.health-=2
        else:
        	self.visible=False

class saw:
    img=[pygame.image.load('images/SAW0.png'),pygame.image.load('images/SAW1.png'),pygame.image.load('images/SAW2.png'),pygame.image.load('images/SAW3.png')]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hitbox=(x,y,width,height)
        self.count=0
        self.visible=True

    def draw(self,win):
        self.hitbox=(self.x,self.y,self.width-30,self.height-30)
        if self.count>=8:
            self.count=0
        win.blit(pygame.transform.scale((self.img[self.count//2]),(40,40)),(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def collide(self,rect):  #hitbox
        if rect[0]+ rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:   #inside
            if rect[1]+rect[3]>self.hitbox[1]: # weknow character cannot go below  saw bcoz it cannot go lower 
                return True                   #check whether his feet is below the top of saw
        return False

class spike(saw):
    img=pygame.image.load("images/spike.png")
    def draw(self,win):
        self.hitbox=(self.x+10,self.y,28,315)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):  #rect is hitbox of  player send self.hitbox is of object saw
        if rect[0]+ rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:   #inside
            if rect[1]<self.hitbox[3]:  #y coordinate of player cannot be above spike since player cannot jumphigh
                return True         #check if y coordinate of player is gr8er than height of spike
        return False

class Ring:
    ri=pygame.image.load('sonic1/rin5.png')
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height   
        self.hitbox=(self.x,self.y+2,45,45)    #rectangle                   
        self.visible=True
    def draw(self,win):
        win.blit(pygame.transform.scale((self.ri),(250,60)),(self.x,self.y))
        self.hitbox=(self.x,self.y,45,45)    #rectangle 
    def collide(self,rect):  #hitbox
        global score
        if rect[0]+ rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:   #inside
            if rect[1]+rect[3]>self.hitbox[1]:
                score+=5 
                self.visible=False
        return False


class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text       #a buttton with text
    def draw(self,win,outline=None):     #outline border
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)          
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0) 
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))) #centre text in middle of button
    def isOver(self, pos):      #mouse is overbutton and pos is coordinates
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:               #inside rectangle
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class Projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=5*facing
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)   

co=3
def redrawGameWindow():
    global co    
    win.blit(bg, (bgX, 0))  # draws our first bg image
    win.blit(bg, (bgX2, 0))  # draws the second bg image
    runner.draw(win)
    for x in objects:
    	if (x.visible):
        	x.draw(win)
    font=pygame.font.SysFont('comicsans',30)   #30 big
    text=font.render('Score: '+str(score),1,white)
    win.blit(text,(700,10))
    text=font.render('High Score: '+str(highscores[0][1]),1,white)
    win.blit(text,(500,10))
    for bullet in bullets:
        bullet.draw(win)    
    pygame.display.update()   #refresh

def redrawInstruction():
    win.fill(black)
    font=pygame.font.SysFont('comicsans',30)   #30 big
    text=font.render("Instructions:",1,white)
    win.blit(text,(10,10))
    text=font.render("1.Use f key to fire enemies  ",1,white)
    win.blit(text,(10,30))
    font=pygame.font.SysFont('comicsans',30)   #30 big
    text=font.render("2.Use up arrow key or space bar and down arrow key to dodge the obstacles",1,white)
    win.blit(text,(10,50))
    text=font.render("3.Earn points by killing the enemies and collecting rings",1,white)
    win.blit(text,(10,70))
    text=font.render("4.Press Escape key to enter game menu ",1,white)
    win.blit(text,(10,90))

def endScreen():
    global score,pause,objects,speed
    pause=0
    objects=[]
    speed=60
    run=True
    while(run):
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:                
                run=False
        win.blit(bg,(0,0))        
        font=pygame.font.SysFont('comicsans',80)   #30 big
        text=font.render("Game Over",1,black)
        win.blit(text,(W/2-text.get_width()/2,100))
        largeFont=pygame.font.SysFont('comicsans',80)
        newScore=largeFont.render('Current Score:{} '.format(score),1,black)
        win.blit(newScore,(W/2-newScore.get_width()/2,220))
        pygame.display.update()
    score=0
    runner.falling=False
   
BG_COLOR = pygame.Color('gray12')
BLUE = pygame.Color('dodgerblue')
FONT = freetype.Font(None, 24)
def redrawHighScore():
    highscores=load()              #load the json file
    win.fill((30, 30, 50))    
    # Display the high-scores.
    for y, (hi_name, hi_score) in enumerate(highscores):
        FONT.render_to(win, (100, y*30+40), f'{hi_name} {hi_score}', BLUE)

    pygame.display.flip()

bggui=pygame.image.load("sonic1/bggui.jpg")
def redrawWindow():             #draw menu     
    win.blit(bggui,(0,0))   
    greenButton.draw(win,black)     #color of boudary/border
    instructionButton.draw(win,black)
    highscoreButton.draw(win,black)
    quitButton.draw(win,black)

greenButton=button(green,300,30,150,70,'Play')
instructionButton=button(green,250,120,260,70,'Instructions')
highscoreButton=button(green,250,215,250,70,'High Scores')
quitButton=button(green,300,310,150,70,'Quit')

runner=player(200,305,64,64)
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
goblin=Enemy(600,313,64,64) 
drag=Dragon(810,10,64,64)
shootloop=0
bullets=[]
score=0
run = True
speed = 60 # NEW
objects=[]
pause=0
fallSpeed=0

while run:    
    highscores=load()
    pygame.display.update()    
    if shootloop>0:
        shootloop+=1    
    if shootloop > 3:
        shootloop=0    

    for bullet in bullets:

         #COLLISION if bullet is inside rectangle  #above bottom of rectangle        #below of top of rectangle
        print(bullet.x)
        if(goblin.visible):
            if bullet.y-bullet.radius < goblin.hitbox[1]+goblin.hitbox[3] and bullet.y+bullet.radius>goblin.hitbox[1]:
                if bullet.x+bullet.radius > goblin.hitbox[0] and bullet.x-bullet.radius <goblin.hitbox[0]+goblin.hitbox[2]:
                        score+=10
                        hitSound.play()
                        bullets.pop(bullets.index(bullet))    #delete bullets after it hits enemy      
                        goblin.hit()
                             
        if bullet.x<W and bullet.x>0:   #bullet inside screen size
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))    #delete bullets going outside     

        if (drag.visible):
            if bullet.y-bullet.radius < drag.hitbox[1]+drag.hitbox[3] and bullet.y+bullet.radius>drag.hitbox[1]:
                if bullet.x+bullet.radius > drag.hitbox[0] and bullet.x-bullet.radius <drag.hitbox[0]+drag.hitbox[2]:                    
                        score+=10
                        hitSound.play()
                        bullets.pop(bullets.index(bullet))    #delete bullets after it hits enemy
                        drag.hit()
                             
    if pause>0:
        pause+=1
        if pause>fallSpeed*2:            #pause for a second and then show endscreen           
            highscores.append([playerName, score])
            values=(playerName,score)
            sqlQuery="insert into people values(%s,%s)"
            popo=mycursor.execute(sqlQuery,values) 
            mydb.commit()
            
            save(sorted(highscores, key=itemgetter(1), reverse=True))
            endScreen()
    for ob in objects:
        if(ob.visible==True):
            if ob.collide(runner.hitbox):
                runner.falling=True

                dieSound.play()
                if pause==0:
                    fallSpeed=speed
                    pause=1


        ob.x-=1.4
        if ob.x<ob.width*-1:
            objects.pop(objects.index(ob))   #disappear objects when they go out of screen

    bgX -= 1.4  # Move both background images back
    bgX2 -= 1.4
    
    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX2 = bg.get_width()
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            run = False    
            pygame.quit() 
            quit()

        if event.type == USEREVENT+2:
            r = random.randrange(0,5)
            if r == 0:
                objects.append(saw(810, 330, 64, 64))
            elif r == 1:
                objects.append(spike(810, 0, 48, 310))
            
            elif r==3:
                rg=Ring(810,330,120,64)
                objects.append(rg)

            elif r==2:
                goblin=Enemy(810,313,64,64)
                objects.append(goblin)

            elif r==4:
                drag=Dragon(810,160,64,64)
                objects.append(drag)
                
        pos=pygame.mouse.get_pos()        
        if bgc:
            if event.type==pygame.MOUSEBUTTONDOWN:   #click
                if greenButton.isOver(pos):
                    print('clicked the button')
                    bgc=0            
                if quitButton.isOver(pos):
                    run=False
                    print('quit')          
                if highscoreButton.isOver(pos):
                    bgc=3
                if instructionButton.isOver(pos):
                    bgc=2

        if event.type==pygame.MOUSEMOTION:  # we are hovering over top not click on it  
            if greenButton.isOver(pos):
                greenButton.color=red
            else:
                greenButton.color=green              
            if quitButton.isOver(pos):
                quitButton.color=red   
            else:
                quitButton.color=green
            if instructionButton.isOver(pos):
                instructionButton.color=red
            else:
                instructionButton.color=green              
            if highscoreButton.isOver(pos):
                highscoreButton.color=red   
            else:
                highscoreButton.color=green

    keys=pygame.key.get_pressed()  #if user pressmore than 1 key
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not (runner.jumping):    #if runner is not already not jumping then we will allow him to jump
            runner.jumping=True
    if keys[pygame.K_DOWN]:
        if not (runner.sliding):   #if runner is sliding when we hit down arrow them we wont let him slide
            runner.sliding=True
    if keys[pygame.K_f] and shootloop==0:
        bulletSound.play()
        facing=1    
        if len(bullets)<10:  #max 10 bullets
            o=Projectile(round(runner.x +runner.width//2),round(runner.y+runner.height//2),6,(255,165,0),facing)
            bullets.append(o)  #bullets coming from middle of the player
        shootloop=1
    if keys[pygame.K_ESCAPE]:
        score=0
        bgc=1
    if(bgc==1):
        redrawWindow()    #Game menu with play button
    elif(bgc==3):
    	redrawHighScore()
    elif(bgc==2):
        redrawInstruction()
    else:    
        redrawGameWindow()       #Main game bgc=0
    clock.tick(speed)  
#