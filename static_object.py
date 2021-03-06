# coding: utf-8
from textures import *  # import all images
from math import floor
from pygame.locals import *


class StaticObject(pygame.sprite.Sprite):
    """This is the base class
    for all static objects (walls, food, bonuses).
    """
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * tile_size + 32, floor(y) * tile_size + 32, tile_size, tile_size)

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))

class Wall(StaticObject):
    pass

class SolidWall(Wall):
    """This class describes walls
    that can't be crushed by all dynamic objects.
    """
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.solid_wall, x, y)


class FragileWall(Wall):
    """This class describes walls
    that can be crushed by pacman.

    """
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.fragile_wall, x, y)


class EatableObject(StaticObject):
    pass

class Food(EatableObject):
    """This class describes pacman's food."""
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.food, x, y)


class Pickaxe(EatableObject):
    """This class describes bonus
    that help pacman crush solid walls.

    """
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.pickaxe, x, y)


class Sword(EatableObject):
    """This class describes bonus
        that help pacman kill ghosts

    """
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.sword, x, y)


class Elixir(EatableObject):
    """This class describes bonus
    that increase pacman's speed.

    """
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.elixir, x, y)


class Score(StaticObject):
    def __init__(self, img, x, y):
        StaticObject.__init__(self, img, x, y)
