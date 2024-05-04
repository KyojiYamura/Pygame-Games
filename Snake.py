import random

import pygame

pygame.init()
game_over = False

game_score = 0
score_increment = 10

x1 = 300
y1 = 300
x1_change = 0
y1_change = 0
random_x = random.randint(20, 1180)
random_y = random.randint(20, 780)

snake_speed = 35

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
enchanted = (255, 0, 0)

font = pygame.font.Font(None, 36)
dis = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_List = []
Length_of_snake = 1




def spawn_food():
    return random.randint(20, 1180), random.randint(20, 780)


foods = [spawn_food() for _ in range(3)]


def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(dis, black, [segment[0], segment[1], 20, 20])


def check_collision_with_self(snake_list):
    head = snake_list[0]
    for segment in snake_list[1:]:
        if head[0] == segment[0] and head[1] == segment[1]:
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if x1_change != 10:
                    x1_change = -10
                    y1_change = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if x1_change != -10:
                    x1_change = 10
                    y1_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if y1_change != 10:
                    y1_change = -10
                    x1_change = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if y1_change != -10:
                    y1_change = 10
                    x1_change = 0

    x1 += x1_change
    y1 += y1_change
    x1 = x1 % 1200
    y1 = y1 % 800

    dis.fill(white)
    pygame.draw.rect(dis, black, [x1, y1, 25, 25])

    snake_Head = []
    snake_Head.append(x1)
    snake_Head.append(y1)
    snake_List.append(snake_Head)

    if len(snake_List) > Length_of_snake:
        del snake_List[0]

    if check_collision_with_self(snake_List):
        game_over = True

    draw_snake(snake_List)
    snake_head = pygame.Rect(x1, y1, 25, 25)
    pygame.draw.circle(dis, enchanted, [random_x, random_y], 15)
    food_circle_enchanted = pygame.Rect(random_x, random_y, 30, 30)
    for food in foods:
        pygame.draw.rect(dis, green, [food[0], food[1], 20, 20])
        food_rect = pygame.Rect(food[0], food[1], 20, 20)
        if snake_head.colliderect(food_rect):
            game_score += score_increment
            Length_of_snake += 1
            foods.remove(food)
            foods.append(spawn_food())
    if snake_head.colliderect(food_circle_enchanted):
        game_score += score_increment + 25
        Length_of_snake += 5
        random_x = random.randint(20, 1180)
        random_y = random.randint(20, 780)
        snake_speed += 1
        clock.tick(snake_speed)






    score_text = font.render(f'Score: {game_score}', True, (255, 50, 255))
    dis.blit(score_text, (10, 10))
    pygame.display.update()

    clock.tick(snake_speed)

# Game Over handling...
game_over_text = font.render('Game Over', True, red)
score_text = font.render(f'Final Score: {game_score}', True, red)
dis.blit(game_over_text, (dis.get_width() // 2 - game_over_text.get_width() // 2, 300))
dis.blit(score_text, (dis.get_width() // 2 - score_text.get_width() // 2, 350))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            quit()

