import pygame
import random


screen_width = 800
screen_height = 600
line_width = 10


platform_spawn_x = 20
platform_spawn_y = 250
platform_change_x = 0
platform_change_y = 0


ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_velocity_x = 5
ball_velocity_y = 5

game_score = 0

class Color:
    white = (255, 255, 255)
    red = (255, 0, 0)
    grey = (128,128,128)
    black = (0, 0, 0)


def random_location():
    return random.randint(0, screen_width - 40), random.randint(0, screen_height - 40)

pygame.init()
running = True
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ping Pong')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    """
    danger = pygame.draw.rect(screen, Color.red, (0, 0,30,910 ), 30)
    Box = pygame.draw.rect(screen, Color.white, (-110, 0,910,600), 30)
    platform = pygame.draw.rect(screen, Color.grey, (50, 250, 10, 90), 30)
    ball= pygame.draw.circle(screen , Color.grey, (200, 300), 10)
    """
    font = pygame.font.Font(None, 36)
    screen.fill(Color.black)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    platform_spawn_y += mouse_y

    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    #safe walls
    if ball_x + ball_radius > screen_width-20:
        ball_velocity_x *= -1
    if ball_y - ball_radius < 10 or ball_y + ball_radius > screen_height-20:
        ball_velocity_y *= -1


    if (ball_x + ball_radius >platform_spawn_x and ball_x - ball_radius < platform_spawn_x+10 and
            ball_y + ball_radius > mouse_y and ball_y - ball_radius < mouse_y + 120):
        game_score +=1
        ball_velocity_x *= -1.1
        ball_velocity_y *= +1.1

    if ball_x - ball_radius < 10:
        game_over_text = font.render('Game Over', True, Color.red)
        score_text = font.render(f'Final Score: {game_score}', True, Color.red)
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 300))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 350))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


    platform = pygame.draw.rect(screen, Color.grey, (platform_spawn_x, mouse_y - 50, 10, 120), 30)
    danger = pygame.draw.rect(screen, Color.red, (-25, 0, 30, 900), 20)
    ball =  pygame.draw.circle(screen, Color.grey, (ball_x, ball_y), ball_radius)
    Box = pygame.draw.rect(screen, Color.white, (-50, -10, 860, 620), 30)

    score_text = font.render(f'Score: {game_score}', True, Color.white)
    screen.blit(score_text, (10, 25))
    pygame.display.update()
    pygame.time.Clock().tick(60)
    pygame.display.flip()

pygame.quit()
