# KidsCanCode - Game Dev with Pygame
# Jumpy! (platforming game)
# Connor Paxman
# 4/5th
# Happy Tune by http://opengameart.org/users/syncopika
# Yippww by http://opengameart.org/users/snabisch
import pygame
from pygame.locals import *
import random
from colors import Colors
from settings import *
from sprites import *


class Game(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load the highscore
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "images")
        with open(path.join(self.dir, HS_FILE), 'r') as file:
            try:
                self.highscore = int(file.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITE_SHEET))
        # cloud images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pygame.image.load(path.join(img_dir, f"cloud{i}.png")).convert())
        # loading sounds
        self.snd_dir = path.join(self.dir, "sounds", "platformer sounds")
        self.jump_sound = pygame.mixer.Sound(path.join(self.snd_dir, "Jump33.wav"))
        self.jump_sound.set_volume(0.25)
        self.boost_sound = pygame.mixer.Sound(path.join(self.snd_dir, "Boost16.wav"))
        self.boost_sound.set_volume(0.25)

    def new(self):
        # creating sprite groups
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_group = pygame.sprite.Group()
        self.mob_group = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.cloud_group = pygame.sprite.Group()
        # creating the player
        self.player = Player(self)
        for platform in PLATFORM_LIST:
            Platform(self, *platform)
        self.mob_timer = 0
        # start running the game.
        pygame.mixer.music.load(path.join(self.snd_dir, "Happy Tune.ogg"))
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.render()
        pygame.mixer.music.fadeout(500)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.player.jump()
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    self.player.jump_cut()

    def update(self):
        self.all_sprites.update()
        # spawn a mob
        now = pygame.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        mob_hits = pygame.sprite.spritecollide(self.player, self.mob_group, False, pygame.sprite.collide_mask)
        if mob_hits:
            self.playing = False
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platform_group, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        # if the player hits the top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 10:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.cloud_group:
                cloud.rect.y += max(abs(self.player.vel.y / cloud.scale+1), 2)
            for mob in self.mob_group:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platform_group:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        # if player hits a powerup
        pow_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == "boost":
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
                self.boost_sound.play()
        # if the player dies
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platform_group) == 0:
            self.playing = False

        # spawn new platforms
        while len(self.platform_group) < 4:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width), random.randrange(-75, -30))

    def render(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, Colors.WHITE, WIDTH / 2, 15)
        pygame.display.flip()

    def show_start_screen(self):
        pygame.mixer.music.load(path.join(self.snd_dir, "Yippee.ogg"))
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, Colors.WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move and space to jump", 22, Colors.WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, Colors.WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, Colors.WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        if not self.running:
            return
        pygame.mixer.music.load(path.join(self.snd_dir, "Yippee.ogg"))
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BG_COLOR)
        self.draw_text("Game Over", 48, Colors.WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, Colors.WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, Colors.WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, Colors.WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as file:
                file.write(str(self.highscore))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, Colors.WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    self.running = False
                if event.type == KEYUP:
                    waiting = False

    def draw_text(self, text, font_size, color, x, y):
        font = pygame.font.Font(self.font_name, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_game_over_screen()

pygame.quit()
