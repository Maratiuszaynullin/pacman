# coding: utf-8
from map import * # import all static objects and map
import random


def is_solid_wall(x, y):
    return isinstance(MAP.data[int(y)][int(x)], SolidWall)


def is_fragile_wall(x, y):
    return isinstance(MAP.data[int(y)][int(x)], FragileWall)


def is_wall(x, y):
    return is_solid_wall(x, y) or is_fragile_wall(x, y)


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
        direction = 0
        if floor(self.x) == floor(pacman.x):
            for i in range(abs(int(self.y) - int(pacman.y))):
                if self.y > pacman.y:
                    if is_wall(self.x, self.y - i):
                        direction = 0
                        break
                    else: direction = 4
                else:
                    if is_wall(self.x, self.y + i):
                        direction = 0
                        break
                    else: direction = 2       #elif ghost_fear: self.direction = up // else: self.direction == down
        if floor(self.y) == floor(pacman.y):
            for i in range(abs(int(self.x) - int(pacman.x))):
                if self.x > pacman.x:
                    if is_wall(self.x - i, self.y):
                        direction = 0
                        break
                    else: direction = 3
                else:
                    if is_wall(self.x + i, self.y):
                        direction = 0
                        break
                    else: direction = 1
        return direction

    def game_tick(self):
        super(UnblindedGhost, self).game_tick()
        if self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.ghost_AI() != 0: self.direction = self.ghost_AI()

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


pacman = Pacman(5, 8)
blind_ghost = BlindGhost(5, 11)
unblinded_ghost = UnblindedGhost(6, 11)
