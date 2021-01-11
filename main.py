import pygame
import os
import time
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Intruders')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 45

HIT = pygame.USEREVENT + 1

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

PLAYER_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
PLAYER = pygame.transform.rotate(pygame.transform.scale(
    PLAYER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

ENEMY_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
ENEMY = pygame.transform.scale(
    ENEMY_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))


def draw_window(player, enemies, bullets):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(PLAYER, (player.x, player.y))
    for enemy in enemies:
        WIN.blit(ENEMY, (enemy.x, enemy.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()


def handle_player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x - VEL > 0:
        player.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and player.x + VEL + player.width < WIDTH:
        player.x += VEL


def handle_enemy_movement(enemies, direction, player):
    for enemy in enemies:
        if direction == 'right':
            enemy.x += VEL/2
        if direction == 'left':
            enemy.x -= VEL/2


def handle_bullets(bullets, enemies):
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        for enemy in enemies:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
        if bullet.y < 0:
            bullets.remove(bullet)


def create_enemies(enemies):
    for i in range(40):
        if i < 10:
            enemies.append(pygame.Rect((i + 1) * (SPACESHIP_WIDTH + 20), 0,
                                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        if i < 20 and i >= 10:
            enemies.append(pygame.Rect((i - 9) * (SPACESHIP_WIDTH + 20), SPACESHIP_HEIGHT + 20,
                                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        if i < 30 and i >= 20:
            enemies.append(pygame.Rect((i - 19) * (SPACESHIP_WIDTH + 20), SPACESHIP_HEIGHT * 2 + 40,
                                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        if i < 40 and i >= 30:
            enemies.append(pygame.Rect((i - 29) * (SPACESHIP_WIDTH + 20), SPACESHIP_HEIGHT * 3 + 60,
                                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT))


def draw_conclusion(message, color):
    text = FONT.render(message, 1, color)
    WIN.blit(text, (WIDTH/2 - text.get_width() /
                    2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    player = pygame.Rect(WIDTH/2 - SPACESHIP_WIDTH//2, 650,
                         SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    enemies = []
    create_enemies(enemies)
    bullets = []

    direction = 'right'

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        player.x + player.width//2, player.y, 5, 10)
                    bullets.append(bullet)

        for enemy in enemies:
            if enemy.x + enemy.width + VEL//3 > WIDTH:
                direction = 'left'
                for every in enemies:
                    every.y += every.height//2
            if enemy.x - VEL//3 < 0:
                direction = 'right'
                for every in enemies:
                    every.y += every.height//2
            if enemy.colliderect(player):
                draw_conclusion('YOU LOST', RED)
                run = False
                pygame.quit()

        if len(enemies) == 0:
            draw_conclusion('YOU WON!', GREEN)
            run = False
            pygame.quit()

        handle_player_movement(keys_pressed, player)

        handle_enemy_movement(enemies, direction, player)

        handle_bullets(bullets, enemies)

        draw_window(player, enemies, bullets)


if __name__ == '__main__':
    main()
