import pygame as pg
from pygame.color import THECOLORS as colors

import random
import math

pg.init()

# Draw screen
screen = pg.display.set_mode((800, 600))

# Background
background = pg.image.load('images/background.png')

# Title and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load('images/spaceship.png')
pg.display.set_icon(icon)

# Player
playerImg = pg.image.load('images/spaceship.png')
playerImg = pg.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerDX = 0
playerSpeed = 5

# Enemy
enemyImg = pg.image.load('images/alien.png')
enemyX = random.randint(0, 735)
enemyY = random.randint(50, 150)
enemySpeed = 3
enemyDX = enemySpeed
enemyDY = 32

# Bullet
bulletImg = pg.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletSpeed = 7
bulletDY = bulletSpeed
bullet_state = "ready"

# Score
score = 0
font = pg.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    scoreRender = font.render("Score: " + str(score), True, colors['white'])
    screen.blit(scoreRender, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    return distance < 27

# Game Loop
running = True
while running:

    # Draw background
    screen.fill(colors['lightblue'])

    screen.blit(background, (0, 0))

    #  Check for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerDX = -playerSpeed
            if event.key == pg.K_RIGHT:
                playerDX = playerSpeed
            if event.key == pg.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, playerY)
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                playerDX = 0
            if event.key == pg.K_RIGHT:
                playerDX = 0
    
    # Draw player
    playerX += playerDX
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    # Draw enemy
    enemyX += enemyDX
    if enemyX <= 0:
        enemyDX = enemySpeed
        enemyY += enemyDY
    elif enemyX >= 736:
        enemyDX = -enemySpeed
        enemyY += enemyDY
    enemy(enemyX, enemyY)

    # Draw fired bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletDY

    # Collision detection
    if isCollision(enemyX, enemyY, bulletX, bulletY):
        bulletY = 480
        bullet_state = "ready"
        score += 1
        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)
    
    show_score(textX, textY)

    # End loop
    pg.display.update()