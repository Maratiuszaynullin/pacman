# coding: utf-8
from map import *


def is_solid_wall(x, y):
    return isinstance(MAP.data[int(x)][int(y)], SolidWall)


def is_fragile_wall(x, y):
    return isinstance(MAP.data[int(x)][int(y)], FragileWall)


def is_wall(x, y):
    return isinstance(MAP.data[int(x)][int(y)], FragileWall or SolidWall)


def ghost_wall_react(x, y, v):
    wall_cords = {1:[x + v, y], 2:[x, y + v], 3:[x - v], 4:[x, y - v]}
    direction = 0
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                if is_wall(wall_cords[i], wall_cords[i]) and is_wall(wall_cords[j], wall_cords[j]) and is_wall(wall_cords[k], wall_cords[k]):
                    #временное решение, но тоже норм
                    ii = wall_cords[i]
                    jj = wall_cords[j]
                    kk = wall_cords[k]
                    if ii == jj:
                        if ii == kk: del ii
                        else: del ii, kk
                    elif jj == kk: del ii, jj
                    else: del ii, jj, kk
                    direction = random.choice(wall_cords)
                #else: direction = 0
    return direction


class DynamicObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * tile_size, floor(y) * tile_size, tile_size, tile_size)

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class BlindGhost(DynamicObject):
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.blind_ghost, x, y)
        self.direction = 1
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(BlindGhost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)
        print(self.tick)
        self.direction = ghost_wall_react(self.x, self.y, self.velocity)
        if self.direction == 1:
            self.x += self.velocity
        if self.direction == 2:
            self.y += self.velocity
        if self.direction == 3:
            self.x -= self.velocity
        if self.direction == 4:
            self.y -= self.velocity
        self.set_coord(self.x, self.y)


class UnblindedGhost(DynamicObject):
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.unblinded_ghost, x, y)


class Pacman(DynamicObject):
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.pacman, x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if type(MAP.get(int(self.x + self.velocity), int(self.y))) != SolidWall:
                self.x += self.velocity
            if self.x >= map_size - 1:
                self.x = map_size - 1
        elif self.direction == 2:
            if type(MAP.get(int(self.x), int(self.y + self.velocity))) != SolidWall:
                self.y += self.velocity
            if self.y >= map_size - 1:
                self.y = map_size - 1
        elif self.direction == 3:
            if type(MAP.get(int(self.x - self.velocity), int(self.y))) != SolidWall:
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if type(MAP.get(int(self.x), int(self.y - self.velocity))) != SolidWall:
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        # self.eat_food()
        # self.crush_wall()
        # self.set_direction_image(self.direction)
        self.set_coord(self.x, self.y)
