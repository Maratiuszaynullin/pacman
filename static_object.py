# coding: utf-8
from textures import *
"""готово все, кроме рун. Остальное адекватно работает исправлять и добавлять пока не надо"""


class StaticObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.screen_rect = None
        self.x = 0
        self.y = 0
        #self.tick = 0
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * tile_size, floor(y) * tile_size, tile_size, tile_size)

    #def game_tick(self):
        #self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class SolidWall(StaticObject):
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.solid_wall, x, y)


class FragileWall(StaticObject):
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.fragile_wall, x, y)


class Food(StaticObject):
    def __init__(self, x, y):
        StaticObject.__init__(self, Textures.food, x, y)


class Rune(StaticObject):  #руны - модификаторы поведения пакмана
    pass
