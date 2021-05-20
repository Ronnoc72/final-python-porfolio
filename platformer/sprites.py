# Sprites for platformer game.
import pygame
from pygame.locals import *
import random
from settings import *
from colors import Colors
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    """The main player that can be moved by the user."""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.image.set_colorkey(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = (x, y)
        self.spawn_rect = pygame.Rect(x, y, 1, 1)
        self.jumping = False
        self.double_jumping = False
        self.side_jump = False
        self.side = 0
        self.air_timer = 0
        self.jump_timer = pygame.time.get_ticks()
        self.start_timer = pygame.time.get_ticks()
        self.cam_drag = 20

    def check_collision(self):
        """moves the player according to the collisions."""
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.vel.x
        hit_list = pygame.sprite.spritecollide(self, self.game.walls, False)
        for tile in hit_list:
            if self.vel.x > 0:
                self.rect.right = tile.rect.left
                collision_types['right'] = True
            elif self.vel.x < 0:
                self.rect.left = tile.rect.right
                collision_types['left'] = True
        self.rect.y += self.vel.y
        hit_list = pygame.sprite.spritecollide(self, self.game.walls, False)
        for tile in hit_list:
            if self.vel.y >= 0:
                self.rect.bottom = tile.rect.top
                collision_types['bottom'] = True
            elif self.vel.y < 0:
                self.rect.top = tile.rect.bottom
                collision_types['top'] = True
        return collision_types

    def jump(self):
        """function that controls all the jumping actions, double, and wall jumping."""
        if not self.double_jumping and self.air_timer > 20:
            self.game.jump_snd.play()
            self.double_jumping = True
            self.acc.y = -JUMP_FORCE/1.5
        if not self.jumping and self.air_timer < 20:
            self.game.jump_snd.play()
            self.jumping = True
            self.acc.y = -JUMP_FORCE
        now = pygame.time.get_ticks()
        if self.side_jump and self.jump_timer <= now-250:
            self.jump_timer = now
            self.side_jump = False
            self.jumping = True
            self.acc.y = -JUMP_FORCE
            self.acc.x += self.side

    def change_spawn_point(self, x, y):
        """changing where the player will spawn"""
        self.spawn_rect.x = x
        self.spawn_rect.y = y

    def reset(self):
        """Reseting the player after death."""
        self.game.death_snd.play()
        self.acc.x = 0
        self.vel = vec(0, 0)
        self.cam_drag = 1
        self.rect.center = (self.spawn_rect.x, self.spawn_rect.y)
        self.start_timer = pygame.time.get_ticks()

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.reset()
        # if the player is falling out of the map.
        if self.rect.y >= 433:
            self.reset()
        # a condition in order for the player not to move (for a short time) if spawned in.
        if pygame.time.get_ticks()-200 >= self.start_timer:
            keys = pygame.key.get_pressed()
            self.acc.x = 0
            self.vel = vec(0, 0)
            if keys[K_LEFT]:
                self.acc.x = -PLAYER_SPEED
            if keys[K_RIGHT]:
                self.acc.x = PLAYER_SPEED
            if keys[K_UP]:
                self.jump()
            if keys[K_DOWN] and self.side_jump:
                self.acc.y = PLAYER_SPEED//2
            self.vel.x += self.acc.x
            self.vel.y += self.acc.y
            self.acc.y += GRAVITY
            if self.acc.y > 11:
                self.acc.y = 11
        collision = self.check_collision()
        # resets the players settings when hits the ground.
        if collision['bottom']:
            self.vel.y = 0
            self.jumping = False
            self.double_jumping = False
            self.side_jump = False
            self.air_timer = 0
        else:
            self.jumping = True
            self.air_timer += 1
        # if there is a collision on the top of the player.
        if collision['top']:
            self.acc.y += GRAVITY*2
        # if there is a collision with the side of the player.
        if (collision['left'] or collision['right']) and not collision['bottom']:
            self.acc.y = 0
            self.vel.y = 0
            self.side_jump = True
            # identifies the side that the player was hit.
            if collision['left']:
                self.side = 15
            else:
                self.side = -15
        else:
            self.side_jump = False
        # updates the camera and the spawn_location of the player.
        x = -self.rect.centerx+int(WIDTH/2)
        y = -self.rect.centery+int(HEIGHT/2)
        if int(x) == int(self.rect.x)-(WIDTH//2-self.rect.width//2) and int(y) == int(self.rect.y)-(HEIGHT//2-self.rect.height//2):
            self.cam_drag = 20
        self.game.camera.update(x+(self.vel.x*-30), y, self.cam_drag)
        self.rect = self.game.camera.apply_rect(self.rect)
        self.spawn_rect = self.game.camera.apply_rect(self.spawn_rect)


class Wall(pygame.sprite.Sprite):
    """The obstacle that the player can't pass through"""
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.image.set_colorkey(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect = self.game.camera.apply_rect(self.rect)


class Environment(pygame.sprite.Sprite):
    """An object that the player can go through."""
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.environment
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.image.set_colorkey(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect = self.game.camera.apply_rect(self.rect)


class EndPoint(pygame.sprite.Sprite):
    """The point that the player goes to for the next level."""
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.image.set_colorkey(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect = self.game.camera.apply_rect(self.rect)
        # if there is a collision with the player.
        if self.game.player.rect.colliderect(self.rect):
            self.game.complete_snd.play()
            self.game.clear_level()
            self.game.load_level()


class Enemy(pygame.sprite.Sprite):
    """Hositle to the player and will send the player back to the start if hit."""
    def __init__(self, game, x, y, vector, image):
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.image.set_colorkey(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = vec(*vector)
        self.timer = 0
        self.rect.width = self.rect.width//2

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        self.rect = self.game.camera.apply_rect(self.rect)
        now = pygame.time.get_ticks()
        # if the player collides with an enemy path.
        for rect in self.game.enemy_paths:
            if rect.colliderect(self.rect) and self.timer <= now-250:
                self.timer = now
                self.vel.x *= -1
                self.vel.y *= -1
                self.image = pygame.transform.flip(self.image, True, False)


class CheckPoint(pygame.sprite.Sprite):
    """Where the player's spawn locations will be changed if the player collides with it."""
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.checkpoints
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.image.set_colorkey(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect = self.game.camera.apply_rect(self.rect)
        if self.rect.colliderect(self.game.player.rect):
            self.game.player.change_spawn_point(self.rect.centerx, self.rect.centery)


class Camera:
    """The view that the user sees, moves the walls and objects accordingly."""
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Gets access to the rect of a sprite and moves it according to the target in the update."""
        return entity.rect.move(self.camera.topleft)

    def update(self, x, y, drag=20):
        self.camera = pygame.Rect(int(x/drag), int(y/drag), self.width, self.height)

    def apply_rect(self, rect):
        """Moves the rect of something according to the current position."""
        return rect.move(self.camera.topleft)


class Spritesheet:
    """Loads a spritesheet and get different images from the larger image."""
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        """Extracts an image from the sprite sheet."""
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), pygame.Rect(x, y, width, height))
        return image
