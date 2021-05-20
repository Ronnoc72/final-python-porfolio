import pygame
from settings import *
import pytmx


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as file:
            for line in file:
                self.data.append(line.strip())
        self.tile_width = len(self.data[0])
        self.tile_height = len(self.data)
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmx_data = tm

    def render(self, surf):
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surf.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def make_map(self):
        temp_surf = pygame.Surface((self.width, self.height))
        self.render(temp_surf)
        return temp_surf


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        # limit of scrolling
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
