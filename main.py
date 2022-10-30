import pygame
import random
import math
from pygame import mixer

pygame.init()

# display game
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')

pygame.display.set_icon(icon)

# Score
score_value = 0
scoreX = 10
scoreY = 10

# enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# player
playerImage = pygame.image.load('player.png')
playerX = 368
playerY = 480
playerX_change = 0

# bullet
bulletImage = pygame.image.load('bullet.png')
bulletX = random.randint(0, 736)
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Background
background = pygame.image.load('background.png')

# Bullet
bullet = pygame.image.load('bullet.png')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)


def show_score(x, y):
    font = pygame.font.Font("freesansbold.ttf", 32)
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def show_game_over():
    font = pygame.font.Font("freesansbold.ttf", 64)
    over_text = font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def shoot_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    collision = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if collision < 30:
        return True
    else:
        return False


running = True
# main loop


while running:
    # All the items are rendered over this filled screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    shoot_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            show_game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_state = "ready"
            bulletY = 480
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score_value += 1
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        shoot_bullet(playerX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(scoreX, scoreY)
    pygame.display.update()
