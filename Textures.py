# coding: utf-8
import sys
import pygame
from pygame.locals import *
from math import floor
import random
tile_size = 32
map_size = 16
"""все работает, только добавлены не все текстуры, и причем все текстуры стоит перерисовать"""

class Textures:
    def __init__(self):
        pass
    pacman = pygame.image.load('./resources/pacman_right.png')
    blind_ghost = pygame.image.load('./resources/ghost.png')
    unblinded_ghost = pygame.image.load('./resources/ghost.png')
    solid_wall = pygame.image.load('./resources/immortal_wall.png')
    fragile_wall = pygame.image.load('./resources/wall.png')
    food = pygame.image.load('./resources/food.png')
