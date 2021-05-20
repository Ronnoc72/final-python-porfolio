# Connor Paxman
# platformer
# 4/29/21

# imports
import pygame
from pygame.locals import *
from os import path
import random
from settings import *
from colors import Colors
from sprites import *


class Game(object):
    """The main game that controls everything."""
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.camera = Camera(WIDTH, HEIGHT)
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.game_dir = path.dirname(__file__)
        self.rects = []
        self.load_sounds()

    def clear_level(self):
        """clears all the game objects on a certain level, to load the next level."""
        for sprite in self.all_sprites:
            sprite.kill()
        self.enemy_paths = []

    def load_level(self):
        """Loads a level according to the level index."""
        # saves the fastest times per level.
        if self.timer:
            file = open(path.join(self.game_dir, "data.txt"), 'r')
            data = file.read()
            data = data.split(',')
            if not data[0]:
                del data[0]
            if self.level_index >= len(data):
                data.append(str(self.timer))
            else:
                if int(data[self.level_index]) > self.timer:
                    data[self.level_index] = str(self.timer)
            data = ",".join(data)
            file.close()
            file = open(path.join(self.game_dir, "data.txt"), 'w')
            file.write(data)
        self.level_index += 1
        if self.level_index >= 5:
            self.playing = False
            self.display_go_screen()
            return
        self.timer = 0
        # gets the level from the dir.
        level = path.join(self.level_dir, f"level{self.level_index}.txt")
        file = open(level, 'r')
        text = file.read()
        game = text.split('\n')
        # where the game looks for certain keys to load the map.
        for i in range(len(game)):
            for j in range(len(game[i])):
                if game[i][j] == 'D':
                    Wall(self, j*TILE_SIZE, i*TILE_SIZE, self.sprite_sheet.get_image(0, 0, TILE_SIZE, TILE_SIZE))
                elif game[i][j] == 'd':
                    Wall(self, j*TILE_SIZE, i*TILE_SIZE, self.sprite_sheet.get_image(34, 0, TILE_SIZE, TILE_SIZE))
                elif game[i][j] == 'r':
                    Wall(self, j*TILE_SIZE, i*TILE_SIZE, self.sprite_sheet.get_image(68, 0, TILE_SIZE, TILE_SIZE))
                elif game[i][j] == 'l':
                    Wall(self, j*TILE_SIZE, i*TILE_SIZE, self.sprite_sheet.get_image(0, 34, TILE_SIZE, TILE_SIZE))
                elif game[i][j] == 'v':
                    Environment(self, j * TILE_SIZE, i * TILE_SIZE, self.sprite_sheet.get_image(34, 34, TILE_SIZE, TILE_SIZE))
                elif game[i][j] == 'e':
                    EndPoint(self, j*TILE_SIZE, i*TILE_SIZE, self.sprite_sheet.get_image(0, 68, TILE_SIZE, TILE_SIZE))
                elif game[i][j] == 'c':
                    CheckPoint(self, j*TILE_SIZE, i*TILE_SIZE, self.sprite_sheet.get_image(34, 68, TILE_SIZE, TILE_SIZE))
                elif game[i][j] == 'p':
                    self.player = Player(self, j*TILE_SIZE, i*TILE_SIZE)
                elif game[i][j] == 'm':
                    Enemy(self, j*TILE_SIZE, i*TILE_SIZE, (-ENEMY_SPEED, 0), self.enemy_img)
                elif game[i][j] == 'k':
                    Enemy(self, j*TILE_SIZE, i*TILE_SIZE, (0, -ENEMY_SPEED), self.flying_enemy_img)
                elif game[i][j] == 'M':
                    self.enemy_paths.append(pygame.Rect(j*TILE_SIZE-TILE_SIZE//2, i*TILE_SIZE, TILE_SIZE//2, TILE_SIZE))
        file.close()

    def load_images(self):
        """loads all the images for the game."""
        img_dir = path.join(self.game_dir, 'images')
        self.sprite_sheet = Spritesheet(path.join(img_dir, 'tile_set.png'))
        self.player_img = pygame.image.load(path.join(img_dir, 'player.png')).convert()
        self.enemy_img = pygame.image.load(path.join(img_dir, 'enemy.png')).convert()
        self.flying_enemy_img = pygame.image.load(path.join(img_dir, 'flying_enemy.png')).convert()

    def load_sounds(self):
        """Loads all the sounds for the game."""
        snd_dir = path.join(self.game_dir, 'sounds')
        self.jump_snd = pygame.mixer.Sound(path.join(snd_dir, 'jump.wav'))
        self.death_snd = pygame.mixer.Sound(path.join(snd_dir, 'death.wav'))
        self.select_snd = pygame.mixer.Sound(path.join(snd_dir, 'selection.wav'))
        self.complete_snd = pygame.mixer.Sound(path.join(snd_dir, 'complete.wav'))
        pygame.mixer.music.load(path.join(snd_dir, 'playformer_song.wav'))
        pygame.mixer.music.play(-1)

    def new(self):
        """sets up all the game objects."""
        self.level_dir = path.join(self.game_dir, 'maps')
        self.load_images()
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.enemy_paths = []
        self.timer = 0
        self.prev = 0
        self.load_level()
        self.run()

    def run(self):
        """starts the main game loop."""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.render()

    def events(self):
        """checks for all the events for the main game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                elif event.key == pygame.K_p:
                    self.pause_menu()

    def update(self):
        self.all_sprites.update()
        # the speed run timer.
        now = pygame.time.get_ticks()
        if now-1000 >= self.prev:
            self.prev = now
            self.timer += 1
        for i in range(len(self.enemy_paths)):
            self.enemy_paths[i] = self.camera.apply_rect(self.enemy_paths[i])

    def render(self):
        """draws all the objects on the screen"""
        self.screen.fill(Colors.LIGHT_BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.timer), 16, Colors.BLACK, WIDTH//2, 10)
        pygame.display.update()

    def display_level_selection(self):
        """creates all the buttons for the level select and waits for the key."""
        file = open(path.join(self.game_dir, "data.txt"), 'r')
        data = file.read()
        data = data.split(",")
        self.screen.fill(Colors.WHITE)
        # displays all the buttons fro the level select.
        for j in range(5):
            btn = self.draw_button(15*j+(j*TILE_SIZE*2+WIDTH//4), HEIGHT//3,
                TILE_SIZE*2, TILE_SIZE*2, j+1, Colors.CORNFLOWER_BLUE)
            self.rects.append(btn)
        # displays all the fastest times that the user has gotten below each level.
        for i in range(len(data)):
            self.draw_text(data[i], 16, Colors.ORANGE, 15*(i%5)+((i%5)*TILE_SIZE*2+WIDTH//4), HEIGHT//2.3)
        file.close()
        pygame.display.update()
        self.wait_for_key()

    def display_start_screen(self):
        """The first thing to be displayed when the game is started."""
        self.screen.fill(Colors.WHITE)
        self.draw_text("Platformer", 32, Colors.BLUE, WIDTH//2, HEIGHT//2)
        self.draw_text("WASD to move", 24, Colors.CORNFLOWER_BLUE, WIDTH//2, HEIGHT//1.5)
        self.draw_text("Get through the game from left the right", 24, Colors.CORNFLOWER_BLUE, WIDTH//2, HEIGHT//1.3)
        self.draw_text("You can double jump, hold onto walls, and slide down walls", 
            24, Colors.CORNFLOWER_BLUE, WIDTH//2, HEIGHT//1.1)
        pygame.display.update()
        self.wait_for_key(True)

    def display_go_screen(self):
        """The last thing to be displayed when the game is ended."""
        self.screen.fill(Colors.WHITE)
        self.draw_text("The END", 32, Colors.BLUE, WIDTH // 2, HEIGHT // 2)
        pygame.display.update()
        self.wait_for_key(end=True)

    def wait_for_key(self, special_case=False, end=False):
        """Waits for a key to be pressed on a waiting screen before the game starts."""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    self.running = False
                if event.type == KEYUP:
                    if special_case:
                        waiting = False
                if event.type == MOUSEBUTTONDOWN:
                    # checking for special cases so I don't have to repeat code.
                    if special_case or end:
                        waiting = False
                        self.running = False
                        self.playing = False
                        break
                    mouse = pygame.mouse.get_pos()
                    mouse_rect = pygame.Rect(mouse[0], mouse[1], 2, 2)
                    for i in range(len(self.rects)):
                        if self.rects[i].colliderect(mouse_rect):
                            file = open(path.join(self.game_dir, "data.txt"), 'r')
                            data = file.read()
                            text = data.split(',')
                            file.close()
                            if not text[0]:
                                del text[0]
                            self.level_index = i-1
                            # checking to see if the player has completed the 
                            # previous level in order to move on.
                            if len(text) > self.level_index:
                                self.select_snd.play()
                                self.new()
                                waiting = False

    def draw_text(self, text, font_size, color, x, y):
        """Can simply draw text onto the screen."""
        font = pygame.font.Font(self.font_name, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, x, y, width, height, index, color):
        """Creates a button, used for the level section screen."""
        font = pygame.font.Font(self.font_name, 32)
        btn_font = font.render(str(index), True, Colors.BLACK)
        btn = pygame.Surface((width, height))
        btn.fill(color)
        btn_rect = btn.get_rect()
        btn_rect.midtop = (x, y)
        self.screen.blit(btn, btn_rect)
        self.screen.blit(btn_font, btn_rect.move(btn_rect.width//4, btn_rect.height//4))
        return btn_rect

    def pause_menu(self):
        """When the player presses the p key the game will pause and the 
        level selection button will pop up."""
        self.paused = True
        self.screen.fill(Colors.WHITE)
        self.draw_text("PAUSED", 32, Colors.BLUE, WIDTH//2, HEIGHT//2)
        btn_rects = []
        btn = self.draw_button(WIDTH//2, HEIGHT//1.5, TILE_SIZE*12, TILE_SIZE*2, "Level Selection", Colors.CORNFLOWER_BLUE)
        btn_rects.append(btn)
        pygame.display.update()
        while self.paused:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.playing = False
                    self.paused = False
                    self.running = False
                if event.type == KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                if event.type == MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    mouse_rect = pygame.Rect(mouse[0], mouse[1], 2, 2)
                    for i in range(len(btn_rects)):
                        if btn_rects[i].colliderect(mouse_rect):
                            self.select_snd.play()
                            self.paused = False
                            self.level_index = 0
                            self.display_level_selection()


# where the game is made.
game = Game()
game.display_start_screen()
game.display_level_selection()
if game.running:
    game.new()

pygame.quit()
