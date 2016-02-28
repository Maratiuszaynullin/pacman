# coding: utf-8
import sys
import pygame
from pygame.locals import *
from math import floor
import random
tile_size = 32
map_size = 16


class Textures:
    """This class doesn't have functionality.
    It needs to keep all textures in one place.

    """
    pacman = pygame.image.load('./resources/pacman_right.png')
    blind_ghost = pygame.image.load('./resources/ghost.png')
    unblinded_ghost = pygame.image.load('./resources/ghost.png')
    solid_wall = pygame.image.load('./resources/immortal_wall.png')
    fragile_wall = pygame.image.load('./resources/wall.png')
    food = pygame.image.load('./resources/food.png')
    pickaxe = pygame.image.load('./resources/pickaxe.png')
