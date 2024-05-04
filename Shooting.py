import random
import time
import pygame

# pygame setup
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.Font(None, 36)  # Define font for displaying score
target_position = [random.randint(0, 1200), random.randint(0, 700)]
target_texture = pygame.image.load("res/target.png")
background_texture = pygame.image.load("res/wall.png")
handgun_texture = pygame.image.load("res/hand.png")

background_texture = pygame.transform.scale(background_texture,(SCREEN_WIDTH, SCREEN_HEIGHT))
target_texture = pygame.transform.scale(target_texture, (60, 60))
handgun_texture = pygame.transform.scale(handgun_texture,(100,100))
i = 0
player_streak = 0
clip = 12
reload_time = 1000
RELOAD_EVENT = pygame.USEREVENT + 1

def reload_gun():
    global clip
    clip = "Reloading..."
    pygame.time.set_timer(RELOAD_EVENT, reload_time)





while running:
    screen.blit(background_texture,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if shooting_target.collidepoint(event.pos):
                    if clip == 0:
                        print("No more ammo")
                        reload_gun()
                    else:
                        clip -= 1
                        player_streak += 1
                        print("Hit!")
                        target_position = [random.randint(30, 1150), random.randint(30, 680)]

                else:
                    if clip == 0:
                        print("No more ammo")
                        reload_gun()
                    else:
                        clip -= 1
                        player_streak = 0
                        print('Missed!')

            elif event.button == 3:
                reload_gun()
        elif event.type == RELOAD_EVENT:
            clip = 12
            pygame.time.set_timer(RELOAD_EVENT, 0)

    shooting_target = target_texture.get_rect(center=target_position)
    screen.blit(target_texture, shooting_target.topleft)
    pygame.mouse.set_cursor()

    score_text = font.render("Score: " + str(player_streak), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    ammo_count = font.render("Ammo: " + str(clip), True, (0, 0, 0))
    screen.blit(ammo_count, (9, 30))


    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
