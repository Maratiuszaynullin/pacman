# coding: utf-8
from map import * # import all static objects and map
import random


def is_solid_wall(x, y):
    return isinstance(MAP.data[int(y)][int(x)], SolidWall)


def is_fragile_wall(x, y):
    return isinstance(MAP.data[int(y)][int(x)], FragileWall)


def is_wall(x, y):
    return is_solid_wall(x, y) or is_fragile_wall(x, y)


"""def ghost_wall_react(x, y, v):
    wall_cords = [[x + v, y], [x, y + v], [x - v, y], [x, y - v]]
    for i in range(4):
        if is_solid_wall(wall_cords[i][0], wall_cords[i][1]) == 'true':
            print (1231)
            return random.randint(1, 4)
    #return random.randint(1, 4)
    return BlindGhost.direction"""


"""def ghost_wall_react1(x, y, v):
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
    return direction"""


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
        self.direction = 0
        self.velocity = 4.0 / 10.0
        #self.status = 'alive'

    def game_tick(self):
        super(BlindGhost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if not is_wall(self.x + self.velocity, self.y):
                self.x += self.velocity
            else: self.direction = random.choice((2, 3, 4))
            if self.x >= map_size - 1:
                self.x = map_size - 1
                self.direction = random.randint(1, 4)

        if self.direction == 2:
            if not is_wall(self.x, self.y + self.velocity):
                self.y += self.velocity
            else: self.direction = random.choice((1, 3, 4))
            if self.y >= map_size - 1:
                self.y = map_size - 1
                self.direction = random.randint(1, 4)

        if self.direction == 3:
            if not is_wall(self.x - self.velocity, self.y):
                self.x -= self.velocity
            else: self.direction = random.choice((1, 2, 4))
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)

        if self.direction == 4:
            if not is_wall(self.x, self.y - self.velocity):
                self.y -= self.velocity
            else: self.direction = random.choice((1, 2, 3))
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)

        self.set_coord(self.x, self.y)


class UnblindedGhost(DynamicObject):
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.unblinded_ghost, x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0
        #self.status = 'alive'

    def ghost_AI(self):
        if self.x == pacman.x:
            for i in range(int(abs(self.y - pacman.y)) + 1):
                if self.y > pacman.y:
                    if is_wall(self.x, self.y - i): break
                    else: return 'up'
                else:
                    if is_wall(self.x, self.y + i): break
                    else: return 'down'       #elif ghost_fear: self.direction = up // else: self.direction == down
        if self.y == pacman.y:
            for i in range(int(abs(self.x - pacman.x)) + 1):
                if self.x > pacman.x:
                    if is_wall(self.x - i, self.y): break
                    else: return 'left'
                else:
                    if is_wall(self.x + i, self.y): break
                    else: return 'right'

    def game_tick(self):
        super(UnblindedGhost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.ghost_AI(): self.direction = self.ghost_AI()

        if self.direction == 1:
            if not is_wall(self.x + self.velocity, self.y):
                self.x += self.velocity
            else: self.direction = random.choice((2, 3, 4))
            if self.x >= map_size - 1:
                self.x = map_size - 1
                self.direction = random.randint(1, 4)

        if self.direction == 2:
            if not is_wall(self.x, self.y + self.velocity):
                self.y += self.velocity
            else: self.direction = random.choice((1, 3, 4))
            if self.y >= map_size - 1:
                self.y = map_size - 1
                self.direction = random.randint(1, 4)

        if self.direction == 3:
            if not is_wall(self.x - self.velocity, self.y):
                self.x -= self.velocity
            else: self.direction = random.choice((1, 2, 4))
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)

        if self.direction == 4:
            if not is_wall(self.x, self.y - self.velocity):
                self.y -= self.velocity
            else: self.direction = random.choice((1, 2, 3))
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)

        self.set_coord(self.x, self.y)


    
class Pacman(DynamicObject):
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.pacman, x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0
        self.count_food = 0
        self.bonus = None
        self.bonus_time = 0

    def eat(self):
        if isinstance(MAP.data[int(self.y)][int(self.x)], Food):
            MAP.data[int(self.y)][int(self.x)] = None
            self.count_food += 1
        if isinstance(MAP.data[int(self.y)][int(self.x)], Pickaxe):
            MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'pickaxe'
        if isinstance(MAP.data[int(self.y)][int(self.x)], Elixir):
            MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'elixir'
            self.bonus_time = 70
        if isinstance(MAP.data[int(self.y)][int(self.x)], Sword):
            MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'sword'

    def crush_wall(self):
        if is_fragile_wall(self.x, self.y):
            MAP.data[int(self.y)][int(self.x)] = None

    def pacman_with_bonus(self):
        if self.bonus == 'pickaxe':
            if is_solid_wall(self.x, self.y):
                MAP.data[int(self.y)][int(self.x)] = None
                self.bonus = None
        if self.bonus == 'elixir':
            if self.bonus_time != 0:
                self.velocity = 8.0 / 10.0
                self.bonus_time -= 1
            else:
                self.bonus = None
                self.velocity = 4.0 / 10.0
        #if self.bonus == 'sword':
        #    if self.x ==

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if self.bonus == 'pickaxe':
                self.x += self.velocity
            elif not is_solid_wall(self.x + self.velocity, self.y):
                self.x += self.velocity
            if self.x >= map_size - 1:
                self.x = map_size - 1
        elif self.direction == 2:
            if self.bonus == 'pickaxe':
                self.y += self.velocity
            elif not is_solid_wall(self.x, self.y + self.velocity):
                self.y += self.velocity
            if self.y >= map_size - 1:
                self.y = map_size - 1
        elif self.direction == 3:
            if self.bonus == 'pickaxe':
                self.x -= self.velocity
            elif not is_solid_wall(self.x - self.velocity, self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if self.bonus == 'pickaxe':
                self.y -= self.velocity
            elif not is_solid_wall(self.x, self.y - self.velocity):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0


        self.eat()
        self.crush_wall()
        self.pacman_with_bonus()
        #self.set_direction_image(self.direction)
        self.set_coord(self.x, self.y)
