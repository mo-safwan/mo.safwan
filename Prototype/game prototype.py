import pygame
import random
from pygame import mixer

#initialise pygame
pygame.init()

#create a window
win = pygame.display.set_mode((600,500))

#window title
pygame.display.set_caption("Sasuke vs Kakashi")

#backgoundsound
#mixer.music.load('theme_music.mp3')
#mixer.music.play(-1)


#sasuke
global playery
global playerx
playerimg=pygame.image.load('sasuke1.png')
playerx=10
playery=10
playervel=20
player_hitbox=(playerx, playery, 60, 80)
score=0
health=70
    

#kakashi
global opponenty
global opponentx
opponentimg=pygame.image.load('kakashi1.png')
opponentx=540
opponenty=150
opponentvel=20
opponent_hitbox=(opponentx, opponenty, 60, 120)



#shuriken
global shurikeny
global shurikenstate
global shurikenx
shurikenimg=pygame.image.load('shuriken1.png')
shurikenx=10
shurikeny=playery
shurikenvel=30
shurikenstate="ready"

#kunai
global kunaiy
global kunaix
global kunaistate
kunaiimg=pygame.image.load('kunai1.png')
kunaix=opponentx
kunaiy=opponenty
kunaivel=40
kunaistate="ready"


#score
score_value=0
font = pygame.font.Font('freesansbold.ttf',20)
textx=250
texty=10

#gameover 
over_font = pygame.font.Font('freesansbold.ttf',10)
voice=True

def show_score(x,y):
    score=font.render("Score : "+str(score_value),True,(255,255,255))
    win.blit(score,(x,y))
    
def gameover():
    over_text=font.render("GAME OVER!",True,(255,255,255))
    dialogue1=font.render("Kakashi:You have talent and you are right ",True,(255,255,255))
    dialogue2=font.render("you are different from the others but ",True,(255,255,255))
    dialogue3=font.render("different isnt always better",True,(255,255,255)) 
    win.blit(over_text,(10,150))
    win.blit(dialogue1,(10,170))
    win.blit(dialogue2,(10,190))
    win.blit(dialogue3,(10,210))

def player(current_health):
    win.blit(playerimg,(playerx,playery))
    player_hitbox=(playerx, playery, 60, 80)
    pygame.draw.rect(win ,(0,0,0), player_hitbox ,2)
    pygame.draw.rect(win ,(255,0,0),(playerx,playery+80,current_health,10))
                           
def opponent():
    win.blit(opponentimg,(opponentx,opponenty))
    opponent_hitbox=(opponentx, opponenty, 55, 110)
    pygame.draw.rect(win ,(0,0,0), opponent_hitbox ,2)


def shuriken():
    global shurikenstate
    shurikenstate="thrown"
    win.blit(shurikenimg,(shurikenx+16,shurikeny+10))
    

def kunai():
    global kunaistate
    kunaistate="thrown"
    win.blit(kunaiimg,(kunaix+16,kunaiy+30))    

    
run=True

#main loop

while run:
    pygame.time.delay(50)
    #check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
                     
    #moveset
    if keys[pygame.K_UP] and playery > playervel:
        playery -= playervel
        if shurikenstate is "ready":
            shurikeny=playery
    if keys[pygame.K_DOWN] and playery < 500-80-playervel:
        playery +=playervel
        if shurikenstate is "ready":
            shurikeny=playery
    if keys[pygame.K_SPACE]:
        if shurikenstate is 'ready':
            shuriken()
            shuriken_sound=mixer.Sound('shuriken.wav')
            shuriken_sound.play()
        
        
    win.fill((0,0,0))

    #kakashi movement
    if opponentvel>0:
        if opponenty+opponentvel<400:
            opponenty+=opponentvel
            if kunaistate is "ready":
                kunaiy=opponenty
        else:
            opponentvel=opponentvel*-1
    else:
        if opponenty-opponentvel>20:
            opponenty+=opponentvel
            if kunaistate is "ready":
                kunaiy=opponenty
        else:
            opponentvel=opponentvel*-1

       
    #shriken movement
    if shurikenx>600:
        shurikenx=10
        shurikenstate="ready"
        shurikeny=playery
    if shurikenstate is "thrown":
        shuriken()
        shurikenx += shurikenvel
        
        
    #kunaimovement
    kunai()
    kunaix -= kunaivel
        
    if kunaix<0:
        kunaix=opponentx
        kunaistate="ready"
        kunaiy=opponenty

   #collisions
    if shurikeny+10>=opponenty and shurikeny+10<=opponenty+120 and shurikenx+10>opponentx:
        shadowclone=mixer.Sound('shadowclone.wav')
        shadowclone.play()
        score_value=score_value+1
        opponentx=540
        opponenty=150
        shurikenx=10
        shurikenstate="ready"
        shurikeny=playery
    if kunaiy>=playery and kunaiy<=playery+80 and kunaix<playerx+60:
        health=health-10             
        kunaix=opponentx
        kunaistate="ready"
        kunaiy=opponenty

   #gameover
    if health==0:
        playerx=2000
        shurikenx=2000
        kunaix=2000
        shurikenvel=0
        shurikenstate='thrown'
        opponentvel=0
        opponentx=540
        opponenty=150
        kunaistate='thrown'
        kunaivel=0
        gameover()
        if voice is True:
            dialogue=mixer.Sound('dialogue.wav')
            dialogue.play()
            voice = False
        
        
                     
        
    show_score(textx,texty)    
    player(health)
    opponent()
    pygame.display.update()
pygame.quit()            
            
