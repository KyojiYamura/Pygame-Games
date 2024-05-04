import time

import pygame

pygame.init()

screen_width = 1200
screen_height = 800
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
background = pygame.image.load('res/bg.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))


class Player:
    def __init__(self, x, y, side, player):
        self.hp = 5
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.width = 70
        self.height = 100
        self.jumping_height = 200
        self.step = 3
        self.velocity_y = 0
        self.velocity_x = 0
        self.gravity = 0.3
        self.is_jumping = False
        self.last_side_p = side
        self.last_shot_time = 0
        self.attack_cooldown = 0.5
        self.death = False
        self.texture_pack = player

        self.texture_R_1 = pygame.image.load("res/player_1_r.png ")
        self.texture_L_1 = pygame.image.load("res/player_1_l.png")
        self.texture_R_1 = pygame.transform.scale(self.texture_R_1, (self.width, self.height))
        self.texture_L_1 = pygame.transform.scale(self.texture_L_1, (self.width, self.height))

        self.texture_R_2 = pygame.image.load("res/player_2_r.png")
        self.texture_L_2 = pygame.image.load("res/player_2_l.png")
        self.texture_R_2 = pygame.transform.scale(self.texture_R_2, (self.width, self.height))
        self.texture_L_2 = pygame.transform.scale(self.texture_L_2, (self.width, self.height))

        self.texture_R_3 = pygame.image.load("res/player_3_r.png")
        self.texture_L_3 = pygame.image.load("res/player_3_l.png")
        self.texture_R_3 = pygame.transform.scale(self.texture_R_3, (self.width, self.height))
        self.texture_L_3 = pygame.transform.scale(self.texture_L_3, (self.width, self.height))

        self.texture_R_4 = pygame.image.load("res/player_4_r.png")
        self.texture_L_4 = pygame.image.load("res/player_4_l.png")
        self.texture_R_4 = pygame.transform.scale(self.texture_R_4, (self.width, self.height))
        self.texture_L_4 = pygame.transform.scale(self.texture_L_4, (self.width, self.height))

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -10
            self.is_jumping = True

    def move_right(self):
        self.velocity_x = self.step

    def move_left(self):
        self.velocity_x = -self.step

    def shoot(self, projectiles):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.attack_cooldown:
            projectiles.append(Projectile(self.x, self.y + self.height // 2, self.last_side_p))
            self.last_shot_time = current_time

    def update(self):
        on_ground = self.y + self.height >= screen_height

        if not on_ground:
            self.velocity_y += self.gravity

        self.y += self.velocity_y
        self.x += self.velocity_x

        self.rect.topleft = (self.x, self.y)

        if self.y + self.height >= screen_height:
            self.x = self.spawn_x
            self.y = self.spawn_y
            self.is_jumping = False

        if self.hp <= 0:
            self.death = True
        else:
            self.death = False

    def draw_L(self, surface):
        if self.texture_pack == 1:
            surface.blit(self.texture_L_1, (self.x, self.y))
        if self.texture_pack == 2:
            surface.blit(self.texture_L_2, (self.x, self.y))
        if self.texture_pack == 3:
            surface.blit(self.texture_L_3, (self.x, self.y))
        if self.texture_pack == 4:
            surface.blit(self.texture_L_4, (self.x, self.y))

    def draw_R(self, surface):
        if self.texture_pack == 1:
            surface.blit(self.texture_R_1, (self.x, self.y))
        if self.texture_pack == 2:
            surface.blit(self.texture_R_2, (self.x, self.y))
        if self.texture_pack == 3:
            surface.blit(self.texture_R_3, (self.x, self.y))
        if self.texture_pack == 4:
            surface.blit(self.texture_R_4, (self.x, self.y))

    def check_collision(self, projectiles):
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.hp -= projectile.dmg
                projectiles.remove(projectile)


class Projectile:
    def __init__(self, x, y, side):
        self.dmg = 1
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.speed = 10
        self.side = side

        self.texture_r = pygame.image.load("res/projectile_R.png")
        self.texture_r = pygame.transform.scale(self.texture_r, (self.width, self.height))
        self.rect = self.texture_r.get_rect(center=(x, y))
        self.texture_l = pygame.image.load("res/projectile_L.png")
        self.texture_l = pygame.transform.scale(self.texture_l, (self.width, self.height))
        self.rect = self.texture_l.get_rect(center=(x, y))

    def update(self):
        if self.side == 'right':
            self.x += self.speed
            self.rect.center = (self.x + 85, self.y)
        elif self.side == 'left':
            self.x -= self.speed
            self.rect.center = (self.x - 35, self.y)

    def draw(self, surface):
        if self.side == 'right':
            surface.blit(self.texture_r, self.rect)
        else:
            surface.blit(self.texture_l, self.rect)


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.texture = pygame.image.load("res/brick-wall.png")
        self.texture= pygame.transform.scale(self.texture, (width, height))

    def draw(self, surface):
        surface.blit(self.texture, self.rect)


window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jumping")

player1 = Player(150, screen_height - 150, "right", 4)
player2 = Player(screen_width - 220, screen_height - 150, 'left', 2)

projectiles = []

platforms = [
    Platform(0, screen_height - 30, 300, 50),
    Platform(screen_width-300, screen_height - 30, 300, 50),
    Platform(screen_width / 3 + 50, screen_height - 200, screen_width / 4, 30),
    Platform(0, screen_height - 180, 65, 30),
    Platform(screen_width-65, screen_height - 180, 65, 30),
    Platform(0, screen_height - 440, 65, 30),
    Platform(screen_width-65, screen_height - 440, 65, 30),
    Platform(200, screen_height - 600, 300, 30),
    Platform(700, screen_height - 600, 300, 30),
    Platform(screen_width-275, screen_height - 280, 65, 30),
    Platform(245, screen_height - 280, 65, 30),
    Platform(screen_width/2-15, screen_height - 200, 30, 150),

]

font = pygame.font.Font(None, 36)
game_over_text = font.render('Game Over', True, red)
player1_wins = font.render('player1 wins', True, red)
player2_wins = font.render('player2 wins', True, red)


def draw_player(player, surface):
    if player.last_side_p == 'left':
        player.draw_L(surface)
    elif player.last_side_p == 'right':
        player.draw_R(surface)


def draw_player1_hp(player1, player2, surface):
    x = 30
    x1 = screen_width - 65
    heart = pygame.image.load('res/hearths.png')
    heart = pygame.transform.scale(heart, (30, 30))
    for _ in range(player1.hp):
        surface.blit(heart, (x, 30))
        x += 35
    for _ in range(player2.hp):
        surface.blit(heart, (x1, 30))
        x1 -= 35


Running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if Running:
            # player_1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.jump()
                if event.key == pygame.K_a:
                    player1.last_side_p = 'left'
                    player1.move_left()
                if event.key == pygame.K_d:
                    player1.last_side_p = 'right'
                    player1.move_right()
                if event.key == pygame.K_w and pygame.key.get_pressed()[pygame.K_a]:
                    player1.last_side_p = 'left'
                    player1.move_left()
                    player1.jump()
                if event.key == pygame.K_w and pygame.key.get_pressed()[pygame.K_d]:
                    player1.last_side_p = 'right'
                    player1.move_right()
                    player1.jump()
                if event.key == pygame.K_SPACE:
                    player1.shoot(projectiles)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player1.velocity_x = 0

            # player_2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2.jump()
                if event.key == pygame.K_LEFT:
                    player2.last_side_p = 'left'
                    player2.move_left()
                if event.key == pygame.K_RIGHT:
                    player2.last_side_p = 'right'
                    player2.move_right()
                if event.key == pygame.K_UP and pygame.key.get_pressed()[pygame.K_LEFT]:
                    player2.last_side_p = 'left'
                    player2.move_left()
                    player2.jump()
                if event.key == pygame.K_UP and pygame.key.get_pressed()[pygame.K_RIGHT]:
                    player2.last_side_p = 'right'
                    player2.move_right()
                    player2.jump()
                if event.key == pygame.K_KP_ENTER:
                    player2.shoot(projectiles)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player2.velocity_x = 0
        else:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player1.death = False
                    player1.x = 150
                    player2.x = screen_width - 220
                    player1.y= screen_height - 150
                    player2.y= screen_height - 150
                    player1.hp = 5

                    player2.death = False
                    player2.hp = 5
                    Running = True

    if Running:
        window.blit(background, (0, 0))
        draw_player(player1, window)
        draw_player(player2, window)
        draw_player1_hp(player1, player2, window)

        player1.update()
        player2.update()

        for platform in platforms:
            platform.draw(window)
            if player1.rect.colliderect(
                    platform.rect) and player1.rect.bottom > platform.rect.top and player1.velocity_y >= 0:
                player1.y = platform.rect.top - player1.height
                player1.velocity_y = 0
                player1.is_jumping = False
            if player1.rect.colliderect(
                    platform.rect) and player1.rect.top < platform.rect.bottom and player1.velocity_y < 0:
                player1.y = platform.rect.bottom
                player1.velocity_y = 0
            if player1.rect.colliderect(platform.rect) and player1.rect.left < platform.rect.left < player1.rect.right:
                player1.x = platform.rect.left
                player1.velocity_x = 0  # Stop horizontal movement



            if player2.rect.colliderect(platform.rect) and player2.rect.bottom > platform.rect.top:
                player2.y = platform.rect.top - player2.height
                player2.velocity_y = 0
                player2.is_jumping = False
            if player2.rect.colliderect(
                    platform.rect) and player2.rect.top < platform.rect.bottom and player2.velocity_y < 0:
                player2.y = platform.rect.bottom
                player2.velocity_y = 0

        for projectile in projectiles:
            projectile.update()
            for platform in platforms:
                if not projectile.rect.colliderect(platform.rect):
                    projectile.draw(window)
                else:
                    projectiles.remove(projectile)

        for player in [player1, player2]:
            player.update()
            player.check_collision(projectiles)

        if player1.death or player2.death:
            Running = False



    else:
        if player1.death:
            window.blit(game_over_text, (window.get_width() // 2 - game_over_text.get_width() // 2, 300))
            window.blit(player2_wins, (window.get_width() // 2 - player2_wins.get_width() // 2, 350))
            pygame.display.update()
        else:
            window.blit(game_over_text, (window.get_width() // 2 - game_over_text.get_width() // 2, 300))
            window.blit(player1_wins, (window.get_width() // 2 - player1_wins.get_width() // 2, 350))
            pygame.display.update()

    pygame.time.Clock().tick(60)
    pygame.display.update()
