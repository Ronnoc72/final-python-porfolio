# Code by : Connor Paxman
# Art by : Connor Paxman
# Music/Sound by : Connor Paxman
# Tutorial taught by: Eric Broadbent
# 3/5/21

# <--- imports --->
import pygame as pg
from pygame.locals import *
import random
import math
import os

pg.mixer.init()


# <--- Game object classes --->
class Bullet(pg.sprite.Sprite):
    """The projectile that the player will shot at the npc"""
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = bullet_img
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image, (5, 10))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * .75 // 2
        if debug:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10
        self.spread = 0

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.spread
        # deletes the bullet when it reaches the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Player(pg.sprite.Sprite):
    """The ship near the bottom of the screen that the user controls."""
    def __init__(self):
        super(Player, self).__init__()
        self.shield = 100
        self.fuel = 100
        self.lives = 3
        self.hidden = False
        self.power_level = 1
        self.power_timer = pg.time.get_ticks()
        self.hide_timer = pg.time.get_ticks()
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * .75 // 2
        if debug:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = int(WIDTH // 2)
        self.rect.bottom = int(HEIGHT - (HEIGHT * 0.05))
        self.speed_x = 0
        self.shoot_delay = 200
        self.last_shot = pg.time.get_ticks()
        self.fuel_power_timer = pg.time.get_ticks()
        self.fuel_power = 1

    def shoot(self):
        now = pg.time.get_ticks()
        if (now - self.last_shot) > self.shoot_delay:
            self.last_shot = now
            if self.power_level == 1:
                b = Bullet(self.rect.centerx, self.rect.top-1)
                all_sprites.add(b)
                bullet_group.add(b)
            elif self.power_level == 2:
                for i in range(2):
                    b = Bullet(self.rect.centerx-((i-.5)*self.rect.width), self.rect.top - 1)
                    all_sprites.add(b)
                    bullet_group.add(b)
            elif self.power_level == 3:
                for i in range(3):
                    b = Bullet(self.rect.centerx-((i-1)*self.rect.width//2), self.rect.top - 1)
                    all_sprites.add(b)
                    bullet_group.add(b)
            elif self.power_level >= 4:
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                b.spread = 2
                all_sprites.add(b)
                bullet_group.add(b)
                b = Bullet(self.rect.right, self.rect.top - 1)
                b.spread = 3
                all_sprites.add(b)
                bullet_group.add(b)
                b = Bullet(self.rect.left, self.rect.top - 1)
                b.spread = -3
                all_sprites.add(b)
                bullet_group.add(b)
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                b.spread = -2
                all_sprites.add(b)
                bullet_group.add(b)
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                all_sprites.add(b)
                bullet_group.add(b)
            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.lives -= 1
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def update_shield(self, r):
        self.shield -= r

    def set_shield(self, new_value):
        self.shield = new_value

    def get_shield(self):
        return self.shield

    def gun_pow(self):
        self.power_level += 1
        self.power_timer = pg.time.get_ticks()

    def fuel_pow(self):
        self.fuel_power = 0
        self.fuel_power_timer = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if self.fuel_power == 0 and now - self.fuel_power_timer > POWER_UP_TIME + 3000:
            self.fuel_power = 1
            self.fuel_power_timer = now
        if self.power_level >= 2 and now - self.power_timer > POWER_UP_TIME:
            self.power_level -= 1
            self.power_timer = now
        if self.hidden and now - self.hide_timer > 2000:
            self.hide_timer = now
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = int(HEIGHT - (HEIGHT * 0.05))
            self.hidden = False
            self.shield = 100
        self.speed_x = 0
        keys = pg.key.get_pressed()
        if keys[K_LEFT]:
            self.speed_x = -5
            self.fuel -= self.fuel_power
        elif keys[K_RIGHT]:
            self.speed_x = 5
            self.fuel -= self.fuel_power
        else:
            self.fuel += 1
            if self.fuel >= 100:
                self.fuel = 100
        if self.fuel <= 0:
            self.speed_x = 0
            self.fuel = 0
        # player shooting
        if keys[K_SPACE] and not self.hidden:
            self.shoot()
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH


# explosions
class Explosions(pg.sprite.Sprite):
    """The animation that plays when an npc is destroyed."""
    def __init__(self, center, size):
        super(Explosions, self).__init__()
        self.size = size
        self.image = animation_database[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if (now - self.last_update) > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(animation_database[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = animation_database[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class NPC(pg.sprite.Sprite):
    """The enemy that is coming at the player that can be exploded and damage the player."""
    def __init__(self):
        super(NPC, self).__init__()
        self.image_orig = npc_img
        self.image_orig.set_colorkey(WHITE)
        self.image_scale = random.randint(30, 75)
        self.image_orig = pg.transform.scale(self.image_orig, (self.image_scale, self.image_scale))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * .75 // 2
        if debug:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randint(self.rect.width, WIDTH - self.rect.width)
        self.rect.top = -self.image_scale + 5
        self.speed_x = random.randint(-2, 2)
        self.speed_y = random.randint(2, 5)
        self.rot = 0
        self.rot_speed = random.randint(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 60:
            self.rot = (self.rot_speed + self.rot) % 360
            self.last_update = now
            # rotating the sprite
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0


class Collectables(pg.sprite.Sprite):
    """The collectable that the player can user when collided with."""
    def __init__(self, center):
        super(Collectables, self).__init__()
        self.type = random.choice(pow_chance)
        self.image = power_up_images[self.type]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()


# <--- Game constants --->
title = "Shump"
creater = "Connor Paxman"
WIDTH = 400
HEIGHT = 700
FPS = 60
debug = False
FONT_NAME = pg.font.match_font("arial")
POWER_UP_TIME = 3000

pow_chance = ["shield", "gun", "shield", "shield", "shield", "gun", "fuel", "fuel"]
pow_types = ["shield", "gun", "fuel"]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# loading in the folders for the assets
game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, "images")
sound_folder = os.path.join(game_folder, "sounds")
text_data_folder = os.path.join(game_folder, "text_data")
ship_folder = os.path.join(image_folder, "ship")
npc_folder = os.path.join(image_folder, "npc")
bullet_folder = os.path.join(image_folder, "bullet")
background_folder = os.path.join(image_folder, "background")
animation_folder = os.path.join(image_folder, "animations")
power_up_folder = os.path.join(image_folder, "power_ups")

# loading in the sounds
shoot_sound = pg.mixer.Sound(os.path.join(sound_folder, "pew.wav"))
shoot_sound.set_volume(0.5)
pg.mixer.music.load(os.path.join(sound_folder, "background-song.wav"))
pg.mixer.music.play(-1)
explosion_sound = []
for snd in ["explosion1.wav", "explosion2.wav"]:
    explosion_sound.append(pg.mixer.Sound(os.path.join(sound_folder, snd)))

shield_sound = pg.mixer.Sound(os.path.join(sound_folder, "shield_pow.wav"))
gun_sound = pg.mixer.Sound(os.path.join(sound_folder, "gun_pow.wav"))
fuel_sound = pg.mixer.Sound(os.path.join(sound_folder, "fuel_pow.wav"))
game_over_sound = pg.mixer.Sound(os.path.join(sound_folder, "game_over.wav"))
shield_sound.set_volume(0.5)
gun_sound.set_volume(0.5)
fuel_sound.set_volume(0.5)


# game functions
def spawn_npc(num=1):
    for i in range(num):
        npc = NPC()
        npc_group.add(npc)
        all_sprites.add(npc)


def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(FONT_NAME, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    surf.blit(text_surf, (x - text_rect.centerx, y))


def draw_bar(surf, x, y, pct, color):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 20
    fill = (pct/100) * bar_length
    outline = pg.Rect(x, y, bar_length, bar_height)
    fill_rect = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surf, WHITE, outline)
    pg.draw.rect(surf, color, fill_rect)


def draw_lives(surf, x, y, image, num_of_lives=3):
    for i in range(num_of_lives):
        img_rect = image.get_rect()
        img_rect.x = x+30 * i
        img_rect.y = y
        surf.blit(image, img_rect)


def game_over_screen():
    pg.init()
    screen.blit(pg.transform.scale(background_img, (WIDTH, HEIGHT)), (0, 0))
    draw_text(screen, title, 64, WIDTH/2, HEIGHT/4, WHITE)
    draw_text(screen, "Created By "+creater, 16, WIDTH/2, HEIGHT/2, WHITE)
    draw_text(screen, "Arrow keys to move, Space bar to fire.", 16, WIDTH/2, HEIGHT*.75, WHITE)
    draw_text(screen, "Press any key to begin.", 16, WIDTH/2, HEIGHT*.87, WHITE)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == KEYUP:
                waiting = False


# <--- Game setup --->
# initialize pygame and create window
pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()
# load images
player_img = pg.image.load(os.path.join(ship_folder, "ship.png")).convert()
player_mini_img = pg.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(WHITE)
npc_img = pg.image.load(os.path.join(npc_folder, "npc.png")).convert()
bullet_img = pg.image.load(os.path.join(bullet_folder, "bullet.png")).convert()
background_img = pg.image.load(os.path.join(background_folder, "starfield.png")).convert()
animation_database = {}
animation_database["lg"] = []
animation_database["sm"] = []
for i in range(9):
    file_name = "regularExplosion0{}.png".format(i)
    img = pg.image.load(os.path.join(animation_folder, file_name)).convert()
    img.set_colorkey(BLACK)
    img_large = pg.transform.scale(img, (125, 125))
    animation_database["lg"].append(img_large)
    img_small = pg.transform.scale(img, (50, 50))
    animation_database["sm"].append(img_small)

power_up_images = {}
for i in range(len(pow_types)):
    power_up_images[pow_types[i]] = pg.image.load(os.path.join(power_up_folder, f"power_up{i}.png")).convert()

# <--- Game loop --->
# game update vars
score = 0
level = 1
diff = 0
playing = True
game_over = True
while playing:
    # handle timing
    if game_over:
        game_over_screen()
        game_over = False
        # sprite groups
        all_sprites = pg.sprite.Group()
        player_group = pg.sprite.Group()
        npc_group = pg.sprite.Group()
        bullet_group = pg.sprite.Group()
        collectables_group = pg.sprite.Group()
        # create game objects
        player = Player()
        for i in range(15):
            npc = NPC()
            npc_group.add(npc)
        # add objects to sprite groups
        player_group.add(player)
        for i in player_group:
            all_sprites.add(i)
        for i in npc_group:
            all_sprites.add(i)
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                playing = False
            if event.key == K_p:
                pg.image.save(screen, "screenshot1.png")
            # if event.key == K_SPACE:
            #     shoot_sound.play()
            #     player.shoot()
    # updates
    # checking for hit between player and enemy.
    hits = pg.sprite.spritecollide(player, npc_group, True, pg.sprite.collide_circle)
    if hits:
        explosion = Explosions(hits[0].rect.center, "sm")
        all_sprites.add(explosion)
        ran_sound = random.choice(explosion_sound)
        ran_sound.play()
        spawn_npc()
        player.update_shield(hits[0].radius * 2)
        if player.get_shield() <= 0:
            exp = Explosions(player.rect.center, "lg")
            all_sprites.add(exp)
            player.hide()
            if player.lives <= 0:
                player.kill()
                game_over_sound.play()
                game_over = True

    collectables_hits = pg.sprite.spritecollide(player, collectables_group, True)
    for hit in collectables_hits:
        if hit.type == "shield":
            player.set_shield(random.randint(20, 35)+player.get_shield())
            shield_sound.play()
            if player.get_shield() >= 100:
                player.set_shield(100)
        if hit.type == "gun":
            player.gun_pow()
            gun_sound.play()
        if hit.type == "fuel":
            player.fuel_pow()
            fuel_sound.play()

    bullet_hits = pg.sprite.groupcollide(bullet_group, npc_group, True, True, pg.sprite.collide_circle)
    for hit in bullet_hits:
        if hit.radius < 2:
            size = "sm"
        else:
            size = "lg"
        explosion = Explosions(hit.rect.center, size)
        all_sprites.add(explosion)
        ran_sound = random.choice(explosion_sound)
        ran_sound.play()
        score += 50 - int(hit.radius)
        if random.random() > 0.9:
            power_up = Collectables(hit.rect.center)
            collectables_group.add(power_up)
            all_sprites.add(power_up)
        spawn_npc()

    all_sprites.update()
    # render
    screen.blit(pg.transform.scale(background_img, (WIDTH, HEIGHT)), (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 16, 40, 5, WHITE)
    draw_bar(screen, WIDTH/1.5, 5, player.get_shield(), RED)
    draw_bar(screen, WIDTH/1.5, 30, player.fuel, GREEN)
    draw_lives(screen, 3, 30, player_mini_img, player.lives)
    pg.display.flip()

pg.quit()
