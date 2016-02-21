import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')


<<<<<<< HEAD
class Map:
    def __init__(self, filename):
=======
class map:
    #opisivaet klass karti
    def __init__(self, filename):
        #schitivaet kartu iz filename
>>>>>>> 93129f8d74e1f59a450f9803ed3ed15849ee9445
        self.map = []
        f = open(filename, 'r')
        txt = f.readlines()
        f.close()
<<<<<<< HEAD

        for line in txt:
            for symbol in line:
                if symbol == "-":
                    self.map.append(Wall(x, y))
                elif symbol == ".":
                    self.map.append(Food(x, y))
                elif symbol == "X":
                    self.map.append(Immortal_wall(x, y))
                else:
                    self.map.append(None)
    def count_walls(self, walls_number = 0):
        for line in self.map:
            for symbol in line:
                if symbol == 'X':
                    walls_number += 1
        return walls_number
=======
        for line in txt:        #perebiraet txt
            for symbol in line:
                if symbol == "-":
                    self.map.append(Wall(x, y))         #tut budet stena
                elif symbol == ".":
                    self.map.append(Food(x, y))         #tut budet edaaaaa
                elif symbol == "x":
                    self.map.append(Immortal_wall(x, y))        #tut budet nerazrushimaya stena
                else:
                    self.map.append(None)           #tut nichego ne budet





>>>>>>> 93129f8d74e1f59a450f9803ed3ed15849ee9445


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
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
        elif self.direction == 4:
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

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.set_coord(self.x, self.y)


class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0


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
    #map = Map(map) #zdes' dolgen but' 2mernuy massiv is obyectov
    ghost = Ghost(0, 0, tile_size, map_size)
    pacman = Pacman(5, 5, tile_size, map_size)
    wall1 = Wall(6, 6, tile_size, map_size) #test
    wall2 = Wall(6, 7, tile_size, map_size)
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        ghost.game_tick()
        pacman.game_tick()
        draw_background(screen, background)
        #for line in map:
        #    for symbol in line:
        #        symbol.draw(screen)
        pacman.draw(screen)
        ghost.draw(screen)
        wall1.draw(screen)
        wall2.draw(screen)
        pygame.display.update()

