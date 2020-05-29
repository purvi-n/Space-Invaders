import pygame
import random
import math
from pygame import mixer

pygame.init()

#Screen
screen=pygame.display.set_mode((800, 600))

#Title, icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#Background
bg=pygame.image.load("bg.jpg")

#Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#Player
playerImg=pygame.image.load("ship.png")
playerX=370
playerY=480
PchangeX=0
PchangeY=0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
EchangeX=[]
EchangeY=[]
totEs=6
for i in range(totEs):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 15))
    EchangeX.append(2)
    EchangeY.append(30)

#Bullet
#READY ~ can't see bullet on screen
#FIRE ~ bullet moving, visible
bulletImg = pygame.image.load("bullet.png")
bulletX=0
bulletY=480
BchangeX=0
BchangeY=7.5
Bstate="READY!"

scoreVal=0
font=pygame.font.Font('PWDottedFont.ttf', 32)

overFont=pygame.font.Font('PWDottedFont.ttf', 128)

textX, textY = 10, 10

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fireBullet(x, y):
    global Bstate
    Bstate="FIRE"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance<27:
        return True
    else:
        return False

def showScore(x, y):
    score=font.render("Score " + str(scoreVal), True, (255, 255, 10))
    screen.blit(score, (x, y))

def gameOver():
    overFont=font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overFont, (350, 300))


running=True
while running:
    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                PchangeX=-5
            if event.key==pygame.K_RIGHT:
                PchangeX=5
            if event.key==pygame.K_SPACE:
                Bsound=mixer.Sound("laser.wav")
                Bsound.play()
                bulletX = playerX
                fireBullet(bulletX, bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                PchangeX=0
    playerX+=PchangeX
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    for i in range(totEs):

        if(enemyY[i]>200):
            for j in range(totEs):
                enemyY[i]=2000
            gameOver()
            break
        enemyX[i]+=EchangeX[i]
        if enemyX[i]<=0:
            EchangeX[i]=2
            enemyY[i]+=EchangeY[i]
        elif enemyX[i]>=736:
            EchangeX[i]=-2
            enemyY[i]+=EchangeY[i]

        collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            explosion=mixer.Sound("explosion.wav")
            explosion.play()
            bulletY=480
            Bstate="READY"
            scoreVal+=1
            enemyX[i]=random.randint(0, 735)
            enemyY[i]=random.randint(15, 40)
            
        enemy(enemyX[i], enemyY[i], i)

    if bulletY<=0:
        bulletY=480
        Bstate="READY"
    if Bstate == "FIRE":
        fireBullet(bulletX, bulletY)
        bulletY-=BchangeY


    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()