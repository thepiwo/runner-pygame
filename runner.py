import pygame
from pygame.locals import *
from random import randint


class Spielfigur(pygame.sprite.Sprite):
    def __init__(self, initial_position, size):

        global overall_speed
        global ground_height
        global screen_height

        pygame.sprite.Sprite.__init__(self)
        self.go_state = 1
        self.anim_speed = 5
        self.anim_cooldown = self.anim_speed
        self.image = pygame.image.load('etc/spielfigur_' + str(self.go_state) + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.size = size
        self.jumping = False
        self.jumpheight = 250
        self.anim_air = False
        self.speed = 5 * overall_speed

    def update(self):

        global boden
        global player_slow_time
        global player_goodie_anim

        if player_slow_time > 0:
            self.speed = overall_speed
        else:
            self.speed = 5 * overall_speed

        self.anim_cooldown -= 1

        # jumping up
        if self.jumping:
            if self.rect.top >= screen_height - self.jumpheight:
                self.rect.top -= self.speed
            else:
                self.jumping = False

        # always falling down
        colide = False
        if pygame.sprite.collide_rect(self, boden):
            colide = True

        if (not self.jumping) & (not colide):
            self.rect.top += self.speed
            self.anim_air = False

        if self.anim_cooldown < 0:
            self.go_state += 1
            if self.go_state > 4:
                self.go_state = 1

            if self.anim_air:
                if player_goodie_anim > 0:
                    self.image = spielfigur_jump_goodie
                else:
                    self.image = spielfigur_jump
            else:
                if player_goodie_anim > 0:
                    if self.go_state == 1:
                        self.image = spielfigur_1_goodie
                    if self.go_state == 2:
                        self.image = spielfigur_2_goodie
                    if self.go_state == 3:
                        self.image = spielfigur_3_goodie
                    if self.go_state == 4:
                        self.image = spielfigur_4_goodie
                else:
                    if self.go_state == 1:
                        self.image = spielfigur_1
                    if self.go_state == 2:
                        self.image = spielfigur_2
                    if self.go_state == 3:
                        self.image = spielfigur_3
                    if self.go_state == 4:
                        self.image = spielfigur_4

            self.anim_cooldown = self.anim_speed

    def jump(self):
        if not self.jumping:
            self.anim_air = True
            self.jumping = True


class Boden(pygame.sprite.Sprite):
    def __init__(self, groundcolor, initial_position, size):
        global goodies
        global obstacles
        global screen_width
        global screen_height
        global ground_height
        global spielfigur_size
        global overall_speed
        global clouds

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(groundcolor)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 3 * overall_speed

    def update(self):
        global obstacle_cooldown

        goodies.update()
        obstacles.update()
        clouds.update()

        obstacle_cooldown -= 1

        # add clouds
        if randint(0, 100) == 0:
            cloud_initial_pos = (screen_width, screen_height - ground_height - randint(200, screen_height))
            clouds.add(Cloud(cloud_initial_pos, self.speed))

        # add goodies
        if randint(0, 60) == 0:
            goodie_typ = randint(1, 4)
            goodie_initial_pos = (screen_width, screen_height - ground_height - goodie2_size - 5 - randint(0, 200))
            goodies.add(Goodie(goodie_typ, goodie_initial_pos, self.speed))

        # add obstacles
        if (obstacle_cooldown < 0) & (randint(0, 50) == 0):
            obstacle_size = (randint(30, 80), randint(30, 80))
            obstacle_initial_pos = (screen_width, screen_height - ground_height - obstacle_size[1])
            obstacle = Obstacle(obstacle_initial_pos, obstacle_size, self.speed)
            if not pygame.sprite.spritecollideany(obstacle, goodies):
                obstacles.add(obstacle)
            else:
                obstacle.kill()
            obstacle_cooldown = 60 / overall_speed


class Goodie(pygame.sprite.Sprite):
    def __init__(self, typ, initial_position, speed):
        global background_color
        global goodie1_color
        global goodie2_color
        global goodie3_color
        global goodie4_color
        global goodie1_size
        global goodie2_size

        pygame.sprite.Sprite.__init__(self)

        if typ == 1:
            self.image = pygame.Surface((goodie1_size, goodie1_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, goodie1_color, (goodie1_size / 2, goodie1_size / 2), goodie1_size / 2, 0)
        if typ == 2:
            self.image = pygame.Surface((goodie2_size, goodie2_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, goodie2_color, (goodie2_size / 2, goodie2_size / 2), goodie2_size / 2, 0)
        if typ == 3:
            self.image = pygame.Surface((goodie1_size, goodie1_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, goodie3_color, (goodie1_size / 2, goodie1_size / 2), goodie1_size / 2, 0)
        if typ == 4:
            self.image = pygame.Surface((goodie1_size, goodie1_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, goodie4_color, (goodie1_size / 2, goodie1_size / 2), goodie1_size / 2, 0)

        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.typ = typ
        self.speed = speed

    def update(self):

        if (self.rect.left + goodie2_size) < 0:
            self.kill()

        global score
        global spielfigur
        global pling1
        global pling2
        global pling3
        global pling4
        global player_invincible_time
        global player_slow_time
        global player_goodie_anim

        self.rect.left -= self.speed
        if pygame.sprite.collide_rect(self, spielfigur):

            if self.typ == 1:
                player_goodie_anim = 0.5 * fps * overall_speed
                pling1.play()
                score += 1
            if self.typ == 2:
                player_goodie_anim = 1 * fps * overall_speed
                pling3.play()
                score += 5
            if self.typ == 3:
                player_slow_time = 4 * fps * overall_speed
                pling2.play()
            if self.typ == 4:
                player_invincible_time = 2 * fps * overall_speed
                pling4.play()

            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, initial_position, size, speed):
        global obstacle_color

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(obstacle_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = speed
        self.size = size

    def update(self):

        if (self.rect.left + self.size[0]) < 0:
            self.kill()

        global game_over
        global game_over_sound
        global player_invincible_time
        global game_over_anim
        global game_over_rect
        global game_over_rect_center

        self.rect.left -= self.speed
        if (player_invincible_time < 0) & pygame.sprite.collide_rect(self, spielfigur):
            game_over_sound.play()
            game_over_anim = 1 * fps * overall_speed
            game_over_rect = self
            game_over_rect_center = self.rect.center
            game_over = True


class Cloud(pygame.sprite.Sprite):
    def __init__(self, initial_position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('etc/wolke' + str(randint(1, 2)) + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = speed

    def update(self):
        if (self.rect.left + self.image.get_width()) < 0:
            self.kill()

        self.rect.left -= self.speed


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Best-Runner")

# static values

overall_speed = 1.5

screen_width = 1000
screen_height = 400
goodie1_size = 25
goodie2_size = 40
ground_height = 25
spielfigur_size = (25, 50)

score = 0

background_color = (133, 182, 226)
ground_color = (60, 137, 112)
goodie1_color = (241, 179, 193)  # 1pt
goodie2_color = (241, 100, 111)  # 5pts
goodie3_color = (0, 0, 0)  # slow player
goodie4_color = (255, 255, 255)  # invincible
obstacle_color = (211, 100, 59)

fps = 60
game_over = False
game_started = False

myfont = pygame.font.SysFont("monospace", 30)
startendfont = pygame.font.SysFont("monospace", 60)
game_over_sound = pygame.mixer.Sound("etc/game_over.wav")
pling1 = pygame.mixer.Sound("etc/pling1.wav")
pling2 = pygame.mixer.Sound("etc/pling2.wav")
pling3 = pygame.mixer.Sound("etc/pling3.wav")
pling4 = pygame.mixer.Sound("etc/pling4.wav")

screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

spielfigur_jump = pygame.image.load('etc/spielfigur_jump.png').convert_alpha()
spielfigur_jump_goodie = pygame.image.load('etc/spielfigur_jump_goodie.png').convert_alpha()
spielfigur_1 = pygame.image.load('etc/spielfigur_1.png').convert_alpha()
spielfigur_1_goodie = pygame.image.load('etc/spielfigur_1_goodie.png').convert_alpha()
spielfigur_2 = pygame.image.load('etc/spielfigur_2.png').convert_alpha()
spielfigur_2_goodie = pygame.image.load('etc/spielfigur_2_goodie.png').convert_alpha()
spielfigur_3 = pygame.image.load('etc/spielfigur_3.png').convert_alpha()
spielfigur_3_goodie = pygame.image.load('etc/spielfigur_3_goodie.png').convert_alpha()
spielfigur_4 = pygame.image.load('etc/spielfigur_4.png').convert_alpha()
spielfigur_4_goodie = pygame.image.load('etc/spielfigur_4_goodie.png').convert_alpha()

####################

space_cooldown = 0
obstacle_cooldown = 0
game_over_anim = 0
player_invincible_time = 0
player_slow_time = 0
player_goodie_anim = 0
game_over_rect = None
game_over_rect_center = None

spielfigur = Spielfigur(
    ((screen_width / 2) - (spielfigur_size[0] / 2), screen_height - spielfigur_size[1] - ground_height),
    spielfigur_size)

boden = Boden(ground_color, (0, screen_height - ground_height), (screen_width, ground_height))

goodies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
clouds = pygame.sprite.Group()

clock = pygame.time.Clock()

while True:
    time_passed = clock.tick(fps)
    keys = pygame.key.get_pressed()
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    if keys[K_ESCAPE]:
        exit()

    game_over_anim -= 1

    if game_over_anim > 0:

        game_over_rect.image = pygame.Surface(((game_over_rect.rect.width + 10), (game_over_rect.rect.height + 10)))
        game_over_rect.image.fill(obstacle_color)
        game_over_rect.rect = game_over_rect.image.get_rect()
        game_over_rect.rect.center = game_over_rect_center

        screen.blit(boden.image, boden.rect)
        clouds.draw(screen)

        screen.blit(spielfigur.image, spielfigur.rect)

        goodies.draw(screen)
        obstacles.draw(screen)

    else:
        if game_started & (not game_over):

            space_cooldown -= 1
            player_invincible_time -= 1
            player_slow_time -= 1
            player_goodie_anim -= 1

            if keys[K_SPACE] & (space_cooldown < 0):
                spielfigur.jump()
                space_cooldown = 70 / overall_speed

            boden.update()
            screen.blit(boden.image, boden.rect)
            clouds.draw(screen)

            spielfigur.update()
            screen.blit(spielfigur.image, spielfigur.rect)

            goodies.draw(screen)
            obstacles.draw(screen)

            screen.blit(myfont.render("Score: " + str(score), 1, obstacle_color), (screen_width - 320, 0))

            if player_slow_time > 0:
                screen.blit(myfont.render("SLOW: " + str(player_slow_time), 1, goodie3_color), (screen_width - 320, 25))
            if player_invincible_time > 0:
                screen.blit(myfont.render("INVINCIBLE: " + str(player_invincible_time), 1, goodie4_color),
                            (screen_width - 320, 50))
        else:
            if game_over:

                screen.fill(obstacle_color)

                screen.blit(startendfont.render("Game Over", 1, background_color), (80, (screen_height / 2) - 100 - 40))
                screen.blit(startendfont.render("Score: " + str(score), 1, background_color),
                            (80, (screen_height / 2) - 40))
                screen.blit(startendfont.render("Press ENTER for new game", 1, background_color),
                            (80, (screen_height / 2) + 100 - 40))
                if keys[K_RETURN]:
                    obstacles.empty()
                    goodies.empty()
                    score = 0
                    space_cooldown = 0
                    obstacle_cooldown = 0
                    player_invincible_time = 0
                    player_slow_time = 0
                    player_goodie_anim = 0
                    game_over = False

            if not game_started:
                screen.blit(startendfont.render("ENTER to start", 1, obstacle_color), (120, (screen_height / 2) - 80))
                screen.blit(startendfont.render("SPACE for jumping", 1, obstacle_color),
                            (120, (screen_height / 2) + 20))
                if keys[K_RETURN]:
                    game_started = True

    pygame.display.update()
