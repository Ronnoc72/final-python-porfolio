from colors import Colors
import pygame
from os import path
vec = pygame.math.Vector2

# game settings
WIDTH = 1024 // 2
HEIGHT = 768 // 2
FPS = 60
TITLE = "Tile based game"
BGCOLOR = Colors.BROWN

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMAGE = "tile_100.png"
# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_IMAGE = "manBlue_gun.png"
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
# mob settings
MOB_IMAGE = "zoimbie1_hold.png"
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pygame.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400
# weapon settings
ITEM_IMAGES = {'shotgun': 'weapon_machine.png'}
BULLET_IMAGE = "bullet.png"
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12}
# effects
MUZZLE_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0, 255, 25)]
# layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECT_LAYER = 4
ITEM_LAYER = 1
# items
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 20
BOB_SPEED = 0.6
# sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav'}

