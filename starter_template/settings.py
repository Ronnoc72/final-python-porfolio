# Settings for pygame template.
import pygame
import random
from os import path

game_folder = path.dirname(__file__)
image_folder = path.join(game_folder, 'images')
player_file = path.join(image_folder, 'python_logo.png')
sound_folder = path.join(game_folder, 'sounds')
text_data_folder = path.join(game_folder, 'text_data')
# window constants
WIDTH = 360
HEIGHT = 480
FPS = 60
TITLE = "Very Fun Game"
FONT_NAME = "arial"
BG_COLOR = (100, 149, 237)
HS_FILE = "highscore.txt"
SPRITE_SHEET = "spritesheet_jumper.png"
# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_JUMP = 24
PLAYER_GRAVITY = 1
PLATFORM_LIST = [(0, HEIGHT - 60), (WIDTH/1.5, HEIGHT - 150), (WIDTH/3, HEIGHT - 350)]
BOOST_POWER = 60
POW_SPAWN_PCT = 10
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

