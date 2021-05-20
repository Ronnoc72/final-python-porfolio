# Connor Paxman
# 2/23/21
# Pygame testing and template

import pygame as pg
from pygame.locals import *
import random
import sys
import os
from colors import Colors
import math

game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, 'images')
player_file = os.path.join(image_folder, 'python_logo.png')
sound_folder = os.path.join(game_folder, 'sounds')
text_data_folder = os.path.join(game_folder, 'text_data')

pg.font.init()
font = pg.font.SysFont(None, 24)
mouse_btn_held = False


class NPC(pg.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        self.image = pg.Surface((15, 15))
        self.color = Colors.RED
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 4, HEIGHT / 2)
        self.speed = 7
        self.speed_x = self.speed
        self.speed_y = self.speed
        # circling
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery
        self.angle = 1
        self.radius = 100
        self.circle_speed = 0.25

    def update(self):
        # --- circle movement ---
        # if self.angle <= 6.25:
        #     self.rect.centerx = self.radius * math.sin(self.angle) + self.center_x
        #     self.rect.centery = self.radius * math.cos(self.angle) + self.center_y
        #     self.angle += self.circle_speed

        # self.speed_y = math.sin(self.rect.x / 36) * 25
        # constant movement
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        # --- V MOVEMENT ---
        # if self.rect.center >= (WIDTH/2, HEIGHT/2):
        #     self.speed_x = -self.speed
        # if self.rect.x < 0 and self.rect.y > HEIGHT:
        #     self.speed_x = self.speed
        #     self.rect.center = (-self.rect.width, -self.rect.height)
        #     self.color = Colors.random_color(self.color)
        #     self.image.fill(self.color)
        # --- SQUARE MOVEMENT ---
        # if self.rect.right == WIDTH:
        #     self.speed_x = 0
        #     self.speed_y = -self.speed
        # if self.rect.top == 0:
        #     self.speed_x = -self.speed
        #     self.speed_y = 0
        # if self.rect.left == 0:
        #     self.speed_x = 0
        #     self.speed_y = self.speed
        # if self.rect.bottom == HEIGHT and self.rect.right != WIDTH:
        #     self.speed_x = self.speed
        #     self.speed_y = 0
        # --- BOUNCING ---
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed_x *= -1
            self.color = Colors.random_color(self.color)
            self.image.fill(self.color)
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            self.speed_y *= -1
            self.color = Colors.random_color(self.color)
            self.image.fill(self.color)
        # --- SCREEN WRAPPING ---
        # if self.rect.left > WIDTH:
        #     self.rect.top = HEIGHT
        #     self.rect.centerx = WIDTH / 2
        #     self.speed_x = 0
        #     self.speed_y = -5
        # if self.rect.bottom < 0:
        #     self.rect.right = 0
        #     self.rect.centery = HEIGHT/2
        #     self.speed_x = 5
        #     self.speed_y = 0
        # --- NORMAL SCREEN WRAPPING ---
        # if self.rect.x < 0:
        #     self.rect.x = WIDTH
        # if self.rect.y > HEIGHT:
        #     self.rect.y = -self.rect.height
        # if self.rect.y < 0:
        #     self.rect.y = HEIGHT
        # if self.rect.x > WIDTH:
        #     self.rect.x = WIDTH/2
        #     self.rect.y = HEIGHT
        #     self.speed_x = 0
        #     self.speed_y = -self.speed
        # if self.rect.y < -self.rect.height:
        #     self.rect.y = HEIGHT/2
        #     self.rect.x = -self.rect.height + 0.01
        #     self.speed_y = 0
        #     self.speed_x = self.speed


class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_img
        self.image.set_colorkey(Colors.WHITE)
        # self.color = Colors.CORNFLOWER_BLUE
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 10
        self.health = 3
        self.key_pressed = False
        self.hit = False

    def toggle_pressed(self):
        self.key_pressed = False

    def lose_life(self):
        self.health += -1

    def update(self):
        # mouse movement
        if mouse_btn_held:
            self.rect.center = (mouse_x, mouse_y)
        # grid movement
        # key_state = pg.key.get_pressed()
        # if key_state[K_LEFT] and not self.key_pressed:
        #     self.key_pressed = True
        #     self.rect.centerx += -50
        # if key_state[K_RIGHT] and not self.key_pressed:
        #     self.key_pressed = True
        #     self.rect.centerx += 50
        # if key_state[K_UP] and not self.key_pressed:
        #     self.key_pressed = True
        #     self.rect.centery += -50
        # if key_state[K_DOWN] and not self.key_pressed:
        #     self.key_pressed = True
        #     self.rect.centery += 50
        #
        # if not 1 in key_state:
        #     self.toggle_pressed()

        # flow/basic movement
        # self.speed_x = 0
        # self.speed_y = 0
        # key_states = pg.key.get_pressed()
        # if key_states[K_LEFT] or key_states[K_a]:
        #     self.speed_x += -self.speed
        # if key_states[K_RIGHT] or key_states[K_d]:
        #     self.speed_x += self.speed
        # if key_states[K_UP] or key_states[K_w]:
        #     self.speed_y += -self.speed
        # if key_states[K_DOWN] or key_states[K_s]:
        #     self.speed_y += self.speed
        #
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT


def spawn_player(x, y):
    new_player = Player()
    new_player.rect.center = (x, y)
    new_player.speed_x = random.randint(-10, 10)
    new_player.speed_y = random.randint(-10, 10)
    all_sprites.add(new_player)
    player_group.add(new_player)

# game settings
WIDTH = 480
HEIGHT = 360
FPS = 30
TITLE = "Very Fun Game"

pg.init()
pg.mixer.init()
# screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()
# load in images
player_img = pg.image.load(player_file).convert()
# creates sprite groups
all_sprites = pg.sprite.Group()
npc_group = pg.sprite.Group()
player_group = pg.sprite.Group()
# game objects
npc = NPC()
player = Player()
# adding objects to the sprites
all_sprites.add(player)
player_group.add(player)
all_sprites.add(npc)
npc_group.add(npc)
# Game loop
running = True
while running:
    clock.tick(FPS)
    # process input (event loop)
    mouse_x, mouse_y = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
            pg.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and player.rect.collidepoint((mouse_x, mouse_y)):
            mos = pg.mouse.get_pressed()
            if mos[0]:
                mouse_btn_held = True
            if mos[2]:
                spawn_player(mouse_x, mouse_y)
        if event.type == MOUSEBUTTONUP and mouse_btn_held:
            mouse_btn_held = False
        # if event.type == KEYUP:
        #     if event.key == K_LEFT or event.key == K_RIGHT:
        #         player.toggle_pressed()
        #     if event.key == K_UP or event.key == K_DOWN:
        #         player.toggle_pressed()
        # if event.type == KEYDOWN:
        #     if event.key == K_LEFT:
        #         player.speed_x = -5
        #     if event.key == K_RIGHT:
        #         player.speed_x = 5
        #     if event.key == K_UP:
        #         player.speed_y = -5
        #     if event.key == K_DOWN:
        #         player.speed_y = 5
        # basic grid movement
        #     if event.key == K_UP or event.key == K_w or event.key == K_KP_8:
        #         player.rect.y -= 50
        #     if event.key == K_DOWN or event.key == K_s or event.key == K_KP_2:
        #         player.rect.y += 50
        #     if event.key == K_LEFT or event.key == K_a or event.key == K_KP_4:
        #         player.rect.x -= 50
        #     if event.key == K_RIGHT or event.key == K_d or event.key == K_KP_6:
        #         player.rect.x += 50
        #     if event.key == K_KP_1:
        #         player.rect.x -= 50
        #         player.rect.y += 50
        #     if event.key == K_KP_3:
        #         player.rect.x += 50
        #         player.rect.y += 50
        #     if event.key == K_KP_7:
        #         player.rect.x -= 50
        #         player.rect.y -= 50
        #     if event.key == K_KP_9:
        #         player.rect.x += 50
        #         player.rect.y -= 50
        # if event.type == KEYUP:
        #     if event.key == K_LEFT:
        #         player.speed_x = 0
        #     if event.key == K_RIGHT:
        #         player.speed_x = 0
        #     if event.key == K_UP:
        #         player.speed_y = 0
        #     if event.key == K_DOWN:
        #         player.speed_y = 0

    if player.rect.colliderect(npc.rect):
        if not player.hit:
            player.lose_life()
            if player.health < 1:
                player.health = 3
        player.hit = True
    else:
        player.hit = False

    # make updates
    all_sprites.update()

    # render (draw)
    screen.fill((100, 100, 100))
    screen.blit(font.render(f"Health: {player.health}", True, 16), (0, 0))
    all_sprites.draw(screen)
    # last thing that the loop does.
    pg.display.flip()
