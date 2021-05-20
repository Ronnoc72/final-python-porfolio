# Connor Paxman
# 4/14/21
# P 4/5th
# KidsCanCode - Game Development with Pygame video series
# Tile-based game
import pygame
import sys
from colors import Colors
from settings import *
from sprites import *
from os import path
from tilemap import *
from random import random


# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = Colors.GREEN
    elif pct > 0.3:
        col = Colors.YELLOW
    else:
        col = Colors.RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, Colors.WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        img_folder = path.join(self.game_folder, "imgs")
        sound_folder = path.join(self.game_folder, "sounds")
        snd_folder = path.join(sound_folder, 'snd')
        music_folder = path.join(sound_folder, "music")
        self.font = pygame.font.match_font('arial')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 120))
        self.player_image = pygame.image.load(path.join(img_folder, PLAYER_IMAGE)).convert_alpha()
        self.wall_image = pygame.image.load(path.join(img_folder, WALL_IMAGE)).convert_alpha()
        self.wall_image = pygame.transform.scale(self.wall_image, (TILESIZE, TILESIZE))
        self.mob_img = pygame.image.load(path.join(img_folder, MOB_IMAGE)).convert_alpha()
        self.bullet_imgs = {}
        self.bullet_imgs["lg"] = pygame.image.load(path.join(img_folder, BULLET_IMAGE)).convert_alpha()
        self.bullet_imgs["sm"] = pygame.transform.scale(self.bullet_imgs["lg"], (10, 10))
        self.splat = pygame.Surface((64, 64))
        self.splat.fill(Colors.GREEN)
        # sound loading
        pygame.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for effect in EFFECTS_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[effect]))
            s.set_volume(0.2)
            self.effects_sounds[effect] = s
        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for snd in WEAPON_SOUNDS_GUN:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.weapon_sounds['gun'].append(s)
        self.zombie_maon_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.1)
            self.zombie_maon_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.player_hit_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_hit_sounds.append(s)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        map_folder = path.join(self.game_folder, "maps")
        self.map = TiledMap(path.join(map_folder, "tile_based_game.tmx"))
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        for tile_objects in self.map.tmx_data.objects:
            obj_center = vec(tile_objects.x + tile_objects.width/2, tile_objects.y + tile_objects.height/2)
            if tile_objects.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_objects.name == "zombie":
                Mob(self, obj_center.x, obj_center.y)
            if tile_objects.name == "wall":
                Obstacle(self, tile_objects.x, tile_objects.y, tile_objects.width, tile_objects.height)
            if tile_objects.name in ["health", "shotgun"]:
                Item(self, obj_center, tile_objects.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.render()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over screen
        if len(self.mobs) == 0:
            self.playing = False
        # player hits items
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == "shotgun":
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.weapon = 'shotgun'
        # player gets hit
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, (0, y), (WIDTH, y))

    def render(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, Colors.BLUE, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, Colors.BLUE, self.camera.apply_rect(wall.rect), 1)
        # HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text("Zombies: {}".format(len(self.mobs)), self.font, 16, Colors.WHITE, WIDTH-10, 10, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, 105, Colors.RED, WIDTH/2, HEIGHT/2, align="center")
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(Colors.BLACK)
        self.draw_text("Game Over", self.font, 75, Colors.RED, WIDTH/2, HEIGHT/2, align="center")
        self.draw_text("Press A key to start", self.font, 30, Colors.WHITE, WIDTH/2, HEIGHT*3/4, align="center")
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False


# creating the game object.
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
