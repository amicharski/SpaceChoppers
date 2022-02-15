import os

import pygame

pygame.font.init()
pygame.mixer.init()

SCORE_FONT = pygame.font.SysFont("comicsans", 40)

GAME_TIME = 30

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BORDER = pygame.Rect(WIDTH / 2, 0, 10, HEIGHT)
FPS = 150
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3


def check_winner(red_score, yellow_score):
    if red_score > yellow_score:
        return "RED"  # red won
    elif yellow_score > red_score:
        return "YELLOW"  # yellow won
    else:
        return "DRAW"  # draw


def draw_winner(red_score, yellow_score):
    WIN.fill(BLACK)
    winner_text = SCORE_FONT.render(check_winner(red_score, yellow_score) +
                                    " WINS THE GAME! " + str(yellow_score) + " - " + str(red_score), True, WHITE)
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2,
                           HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_score, yellow_score, timer):
    WIN.fill(BLACK)

    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    red_score_text = SCORE_FONT.render("SCORE: " + str(red_score), True, WHITE)
    yellow_score_text = SCORE_FONT.render("SCORE: " + str(yellow_score), True, WHITE)
    timer_text = SCORE_FONT.render("TIME: " + str(timer), True, WHITE)
    WIN.blit(timer_text, (WIDTH - timer_text.get_width() - 10, HEIGHT - timer_text.get_height() - 10))
    WIN.blit(red_score_text, (WIDTH - red_score_text.get_width() - 10, 10))
    WIN.blit(yellow_score_text, (10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < HEIGHT:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(700, 225, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(200, 225, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_score, yellow_score = 0, 0

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    run = True
    while run:
        seconds = GAME_TIME - (pygame.time.get_ticks() - start_ticks) // 1000
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                yellow_score += 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                red_score += 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_score, yellow_score, seconds)

        if seconds == 0:
            break

    draw_winner(red_score, yellow_score)
    pygame.event.clear()
    main()


if __name__ == "__main__":
    main()
