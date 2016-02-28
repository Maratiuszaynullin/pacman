import pygame


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
    #sword = pygame.image.load('./resources/sword.png')
    elixir = pygame.image.load('./resources/elixir.png')