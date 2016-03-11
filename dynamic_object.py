# coding: utf-8
from map import *  # import all static objects and lvl_0
import random
import main as m


def is_solid_wall(x, y):
    return isinstance(m.MAP.data[int(y)][int(x)], SolidWall)


def is_fragile_wall(x, y):
    return isinstance(m.MAP.data[int(y)][int(x)], FragileWall)


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
        DynamicObject.__init__(self, Textures.blind_ghost_right, x, y)
        self.direction = 'stop'
        self.velocity = 4.0 / 10.0
        #self.status = 'alive'

    def game_tick(self):
        super(BlindGhost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 'stop':
            self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.direction == 'right':
            self.image = Textures.blind_ghost_right
            if not is_wall(self.x + self.velocity, self.y):
                self.x += self.velocity
            else: self.direction = random.choice(('down', 'left', 'up'))
            if self.x >= map_size - 1:
                self.x = map_size - 1
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.direction == 'down':
            if not is_wall(self.x, self.y + self.velocity):
                self.y += self.velocity
            else: self.direction = random.choice(('right', 'left', 'up'))
            if self.y >= map_size - 1:
                self.y = map_size - 1
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.direction == 'left':
            self.image = Textures.blind_ghost_left
            if not is_wall(self.x - self.velocity, self.y):
                self.x -= self.velocity
            else: self.direction = random.choice(('right', 'up', 'down'))
            if self.x <= 0:
                self.x = 0
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.direction == 'up':
            if not is_wall(self.x, self.y - self.velocity):
                self.y -= self.velocity
            else: self.direction = random.choice(('right', 'down', 'left'))
            if self.y <= 0:
                self.y = 0
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        self.set_coord(self.x, self.y)


class UnblindedGhost(DynamicObject):
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.unblinded_ghost_right, x, y)
        self.direction = 'stop'
        self.velocity = 4.0 / 10.0
        #self.status = 'alive'

    def ghost_ai(self):
        direction = 'stop'
        if floor(self.x) == floor(pacman.x):
            for i in range(abs(int(self.y) - int(pacman.y))):
                if self.y > pacman.y:
                    if is_wall(self.x, self.y - i):
                        direction = 'stop'
                        break
                    else: direction = 'up'
                else:
                    if is_wall(self.x, self.y + i):
                        direction = 'stop'
                        break
                    else: direction = 'down'       #elif ghost_fear: self.direction = up // else: self.direction == down
        if floor(self.y) == floor(pacman.y):
            for i in range(abs(int(self.x) - int(pacman.x))):
                if self.x > pacman.x:
                    if is_wall(self.x - i, self.y):
                        direction = 'stop'
                        break
                    else: direction = 'left'
                else:
                    if is_wall(self.x + i, self.y):
                        direction = 'stop'
                        break
                    else: direction = 'right'
        return direction

    def game_tick(self):
        super(UnblindedGhost, self).game_tick()
        if self.direction == 'stop':
            self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.ghost_AI() != 'stop': self.direction = self.ghost_AI()

        if self.direction == 'right':
            self.image = Textures.unblinded_ghost_right
            if not is_wall(self.x + self.velocity, self.y):
                self.x += self.velocity
            else: self.direction = random.choice(('down', 'left', 'up'))
            if self.x >= map_size - 1:
                self.x = map_size - 1
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.direction == 'down':
            if not is_wall(self.x, self.y + self.velocity):
                self.y += self.velocity
            else: self.direction = random.choice(('right', 'left', 'up'))
            if self.y >= map_size - 1:
                self.y = map_size - 1
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.direction == 'left':
            self.image = Textures.unblinded_ghost_left
            if not is_wall(self.x - self.velocity, self.y):
                self.x -= self.velocity
            else: self.direction = random.choice(('right', 'up', 'down'))
            if self.x <= 0:
                self.x = 0
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        if self.direction == 'up':
            if not is_wall(self.x, self.y - self.velocity):
                self.y -= self.velocity
            else: self.direction = random.choice(('right', 'down', 'left'))
            if self.y <= 0:
                self.y = 0
                self.direction = random.choice(('right', 'left', 'up', 'down'))

        self.set_coord(self.x, self.y)


class Pacman(DynamicObject):
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.pacman_right, x, y)
        self.direction = 'stop'
        self.velocity = 4.0 / 10.0
        self.count_food = 0
        self.bonus = None
        self.bonus_time = 0

    def eat(self):
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Food):
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.count_food += 1
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Pickaxe):
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'pickaxe'
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Elixir):
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'elixir'
            self.bonus_time = 70
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Sword):
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'sword'

    def crush_wall(self):
        if is_fragile_wall(self.x, self.y):
            m.MAP.data[int(self.y)][int(self.x)] = None

    def pacman_with_bonus(self):
        if self.bonus == 'pickaxe':
            if is_solid_wall(self.x, self.y):
                m.MAP.data[int(self.y)][int(self.x)] = None
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
        if self.direction == 'right':
            self.image = Textures.pacman_right
            if self.bonus == 'pickaxe':
                self.x += self.velocity
            elif not is_solid_wall(self.x + self.velocity, self.y):
                self.x += self.velocity
            if self.x >= map_size - 1:
                self.x = map_size - 1
        elif self.direction == 'down':
            self.image = Textures.pacman_down
            if self.bonus == 'pickaxe':
                self.y += self.velocity
            elif not is_solid_wall(self.x, self.y + self.velocity):
                self.y += self.velocity
            if self.y >= map_size - 1:
                self.y = map_size - 1
        elif self.direction == 'left':
            self.image = Textures.pacman_left
            if self.bonus == 'pickaxe':
                self.x -= self.velocity
            elif not is_solid_wall(self.x - self.velocity, self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 'up':
            self.image = Textures.pacman_up
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
blind_ghost = BlindGhost(2, 8)
unblinded_ghost = UnblindedGhost(6, 11)
