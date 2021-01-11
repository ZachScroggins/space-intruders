import pygame
import os
import time

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Intruders')

FPS = 60
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 45

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

PLAYER_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
PLAYER = pygame.transform.rotate(pygame.transform.scale(
    PLAYER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

ENEMY_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
ENEMY = pygame.transform.scale(
    ENEMY_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))


def draw_window(player, enemies):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(PLAYER, (player.x, player.y))
    for enemy in enemies:
        WIN.blit(ENEMY, (enemy.x, enemy.y))
    pygame.display.update()


def handle_player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x - VEL > 0:
        player.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and player.x + VEL + player.width < WIDTH:
        player.x += VEL


def handle_enemy_movement(enemies, direction):
    for enemy in enemies:
        # if direction == 'right' and enemy.x + enemy.width + VEL//3 < WIDTH:
        if direction == 'right':
            enemy.x += VEL//3
        if direction == 'left':
            enemy.x -= VEL//3


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


def main():
    player = pygame.Rect(WIDTH/2 - SPACESHIP_WIDTH//2, 650,
                         SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    enemies = []
    create_enemies(enemies)
    direction = 'right'

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        handle_player_movement(keys_pressed, player)

        for enemy in enemies:
            if enemy.x + enemy.width + VEL//3 > WIDTH:
                direction = 'left'
                for every in enemies:
                    every.y += every.height//4
            if enemy.x - VEL//3 < 0:
                direction = 'right'
                for every in enemies:
                    every.y += every.height//4

        handle_enemy_movement(enemies, direction)

        draw_window(player, enemies)


if __name__ == '__main__':
    main()
