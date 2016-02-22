import sys
import pygame
from pygame.locals import *
from math import floor
import random


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))

"""
class MovingObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)"""


class Ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Ghost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if type(map.get(self.x + self.velocity, self.y)) != Immortal_wall and type(map.get(self.x + self.velocity, self.y)) != Wall:
                self.x += self.velocity
            else:
                self.direction = random.randint(1, 4)

            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)

        elif self.direction == 2:
            if type(map.get((self.x), (self.y + self.velocity))) != Immortal_wall and type(map.get((self.x), (self.y + self.velocity))) != Wall:
                self.y += self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)

        elif self.direction == 3:
            if type(map.get((self.x - self.velocity), (self.y))) != Immortal_wall and type(map.get((self.x - self.velocity), (self.y))) != Wall:
                self.x -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)

        elif self.direction == 4:
            if type(map.get((self.x), (self.y - self.velocity))) != Immortal_wall and type(map.get((self.x), (self.y - self.velocity))) != Wall:
                self.y -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)