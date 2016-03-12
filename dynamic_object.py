from map import *  # import all static objects and lvl_0
import random
import main as m


def is_solid_wall(x, y):
    """This function checks if it is solid wall on this coordinates."""
    return isinstance(m.MAP.data[int(y)][int(x)], SolidWall)


def is_fragile_wall(x, y):
    """This function checks if it is fragile wall on this coordinates."""
    return isinstance(m.MAP.data[int(y)][int(x)], FragileWall)


def is_wall(x, y):
    """This function checks if it is wall with on coordinates."""
    return is_solid_wall(x, y) or is_fragile_wall(x, y)


class DynamicObject(pygame.sprite.Sprite):
    """This is the base class for all dynamic objects (pacman, ghosts)."""
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
    """This class describes ghost that can't see pacman.
    This ghost moves randomly.
    If ghost run into wall or card edge, it chooses new random direction.
    It has two images for different directions.
    """
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.blind_ghost_right, x, y)
        self.direction = 'stop'
        self.velocity = 4.0 / 10.0
        self.status = 'alive'

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
    """This class describes unblinded ghost.
    He moves randomly, but when pacman is in front of him, he goes to pacman.
    """
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.unblinded_ghost_right, x, y)
        self.direction = 'stop'
        self.velocity = 4.0 / 10.0
        self.status = 'alive'

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
                    else: direction = 'down'

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

        if self.ghost_ai() != 'stop':
            self.direction = self.ghost_ai()

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
    """This class describes pacman.
    Pacman can eat food, crush fragile walls
    and have can have different abilities, if he has bonus.
    """
    def __init__(self, x, y):
        DynamicObject.__init__(self, Textures.pacman_right, x, y)
        self.direction = 'stop'
        self.velocity = 4.0 / 10.0
        self.count_food = 0
        self.bonus = None
        self.bonus_time = 0
        self.score = 0

    def eat_static_objects(self):
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Food):  # If pacman eats food count_food changes.
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.count_food += 1
            self.score += 1
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Pickaxe): # If pacman eats pickaxe he can crush solid walls.
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'pickaxe'
            self.velocity = 4.0 / 10.0
            self.score += 3
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Elixir): # If pacman eats elixir his speed increases.
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'elixir'
            self.bonus_time = 70
            self.score += 4
        if isinstance(m.MAP.data[int(self.y)][int(self.x)], Sword):  # If pacman eats sword he can kill ghosts.
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.bonus = 'sword'
            self.velocity = 4.0 / 10.0
            self.score += 3

    def crush_wall(self):
        if is_fragile_wall(self.x, self.y):
            m.MAP.data[int(self.y)][int(self.x)] = None
            self.score += 2

    def pacman_with_bonus(self):
        if self.bonus == 'pickaxe':  # This bonus help pacman crush solid walls.
            if is_solid_wall(self.x, self.y):
                m.MAP.data[int(self.y)][int(self.x)] = None
                self.bonus = None
                self.score += 3
        if self.bonus == 'elixir':  # This bonus increases pacman speed.
            if self.bonus_time != 0:
                self.velocity = 8.0 / 10.0
                self.bonus_time -= 1
            else:
                self.bonus = None
                self.velocity = 4.0 / 10.0
        if self.bonus == 'sword':  # With this bonus pacman can kill ghost
            if floor(pacman.x) == floor(unblinded_ghost.x) and floor(pacman.y) == floor(unblinded_ghost.y):
                unblinded_ghost.status = 'dead'
                unblinded_ghost.x = -1
                unblinded_ghost.y = -1
                self.bonus = None
                self.score += 5
            if floor(pacman.x) == floor(blind_ghost.x) and floor(pacman.y) == floor(blind_ghost.y):
                blind_ghost.status = 'dead'
                blind_ghost.x = -1
                blind_ghost.y = -1
                self.bonus = None
                self.score += 5


    def set_direction_image(self):
        """This function sets pacman image that depends on direction and bonus."""
        if self.bonus == None:
            if self.direction == 'up':
                self.image = Textures.pacman_up
            elif self.direction == 'right':
                self.image = Textures.pacman_right
            elif self.direction == 'left':
                self.image = Textures.pacman_left
            elif self.direction == 'down':
                self.image = Textures.pacman_down

        if self.bonus == 'pickaxe':
            if self.direction == 'up':
                self.image = Textures.pacman_up_with_pickaxe
            elif self.direction == 'right':
                self.image = Textures.pacman_right_with_pickaxe
            elif self.direction == 'left':
                self.image = Textures.pacman_left_with_pickaxe
            elif self.direction == 'down':
                self.image = Textures.pacman_down_with_pickaxe

        if self.bonus == 'elixir':
            if self.direction == 'up':
                self.image = Textures.pacman_up_with_elixir
            elif self.direction == 'right':
                self.image = Textures.pacman_right_with_elixir
            elif self.direction == 'left':
                self.image = Textures.pacman_left_with_elixir
            elif self.direction == 'down':
                self.image = Textures.pacman_down_with_elixir

        if self.bonus == 'sword':
            if self.direction == 'up':
                self.image = Textures.pacman_up_with_sword
            elif self.direction == 'right':
                self.image = Textures.pacman_right_with_sword
            elif self.direction == 'left':
                self.image = Textures.pacman_left_with_sword
            elif self.direction == 'down':
                self.image = Textures.pacman_down_with_sword


    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 'right':
            if self.bonus == 'pickaxe':
                self.x += self.velocity
            elif not is_solid_wall(self.x + self.velocity, self.y):
                self.x += self.velocity
            if self.x >= map_size - 1:
                self.x = map_size - 1
        elif self.direction == 'down':
            if self.bonus == 'pickaxe':
                self.y += self.velocity
            elif not is_solid_wall(self.x, self.y + self.velocity):
                self.y += self.velocity
            if self.y >= map_size - 1:
                self.y = map_size - 1
        elif self.direction == 'left':
            if self.bonus == 'pickaxe':
                self.x -= self.velocity
            elif not is_solid_wall(self.x - self.velocity, self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 'up':
            if self.bonus == 'pickaxe':
                self.y -= self.velocity
            elif not is_solid_wall(self.x, self.y - self.velocity):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.eat_static_objects()
        self.crush_wall()
        self.pacman_with_bonus()
        self.set_direction_image()
        self.set_coord(self.x, self.y)


pacman = Pacman(5, 8)
blind_ghost = BlindGhost(2, 8)
unblinded_ghost = UnblindedGhost(6, 11)
