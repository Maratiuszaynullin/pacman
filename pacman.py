import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')


class Map:
    def __init__(self, txt, map_size = 16):
        self.data = [[0]*(len(txt)) for i in range(len(txt))]
        for y in range(len(txt)):
            for x in range(len(txt)):
                if txt[y][x] == 'O':
                    self.data[y][x] = Wall(x, y)
                elif txt[y][x] == ".":
                    self.data[y][x] = Food(x, y)
                elif txt[y][x] == 'X':
                    self.data[y][x] = Immortal_wall(x, y)
                else:
                    self.data[y][x] = None

    def get(self, x, y):
        return self.data[y][x]


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))


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
            if type(map.get(int(self.x + self.velocity), int(self.y))) != Immortal_wall:
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if type(map.get(int(self.x), int(self.y + self.velocity))) != Immortal_wall:
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            if type(map.get(int(self.x - self.velocity), int(self.y))) != Immortal_wall:
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
        elif self.direction == 4:
            if type(map.get(int(self.x), int(self.y - self.velocity))) != Immortal_wall:
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)


class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def eat_food(self):
        if type(map.get(int(self.x), int(self.y))) == Food:
            map.data[int(self.y)][int(self.x)] = None

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if type(map.get(int(self.x + self.velocity), int(self.y))) != Immortal_wall:
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if type(map.get(int(self.x), int(self.y + self.velocity))) != Immortal_wall:
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if type(map.get(int(self.x - self.velocity), int(self.y))) != Immortal_wall:
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if type(map.get(int(self.x), int(self.y - self.velocity))) != Immortal_wall:
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.eat_food()

        self.set_coord(self.x, self.y)


class Wall(GameObject):
    def __init__(self, x, y, tile_size=32, map_size=16):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)


class Immortal_wall(GameObject):
    def __init__(self, x, y, tile_size=32, map_size=16):
        GameObject.__init__(self, './resources/immortal_wall.png', x, y, tile_size, map_size)


class Food(GameObject):
    def __init__(self, x, y, tile_size=32, map_size=16):
        GameObject.__init__(self, './resources/food.png', x, y, tile_size, map_size)


def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0


if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 16
    ghost = Ghost(0, 0, tile_size, map_size)
    pacman = Pacman(5, 5, tile_size, map_size)
    f = open('map', 'r')
    txt = f.readlines()
    f.close()
    map = Map(txt)
    print(type(map.get(0, 0)))
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()
    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        ghost.game_tick()
        pacman.game_tick()
        draw_background(screen, background)
        for y in range(map_size):
            for x in range(map_size):
                if map.get(x, y) != None:
                    map.get(x, y).draw(screen)
        pacman.draw(screen)
        ghost.draw(screen)
        pygame.display.update()

