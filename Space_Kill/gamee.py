import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
background = pygame.image.load('background.png')
#background IMg

#sound
mixer.music.load('background.wav')
mixer.music.play()


#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship-icon-vector.png')
pygame.display.set_icon(icon)


#player 
playerImg = pygame.image.load('002-spaceship.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (100, 100))
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    temp = pygame.image.load('001-monster.png').convert_alpha()
    temp = pygame.transform.scale(temp, (110, 110))
    enemyImg.append(temp)
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
#ready state you can't see the bullet on the screen
#fire the bullet is moving
bullet_state = "ready"

# score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10
 
#game over
over_font = pygame.font.Font('freesansbold.ttf',64)
final_score = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Dhruv Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER ",True,(255,255,255))
    final_text = final_score.render("Dhruv Score is " + str(score_value),True,(255,255,255))
    screen.blit(over_text,(200,250))
    screen.blit(final_text,(200,300))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))  

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10)) 



def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))   
    if distance < 27:
        return True
    else:
        return False     

# Game Loop
running = True
while running:

    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # if keystroke is pressed check weather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)    
        if event.type == pygame.KEYUP:        
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0   



    playerX +=playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >736:
        playerX=736   

    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] +=enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i]  += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3  
            enemyY[i]  += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)    
        if collision:
            exp_sound = mixer.Sound('explosion.wav')
            exp_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)  

        enemy(enemyX[i],enemyY[i],i)

    #bullet mmovement
    if bulletY <=0:
        bulletY =480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change   

    

    player(playerX,playerY)
    show_score(textX,textY) 
    pygame.display.update()

