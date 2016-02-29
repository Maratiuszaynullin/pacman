import pygame


tile_size = 32
map_size = 16


class Textures:
    """This class doesn't have functionality.
    It needs to keep all textures in one place.

    """
    pacman = pygame.image.load('./resources/fish_clownfish_raw.png')
    blind_ghost = pygame.image.load('./resources/ghost.png')
    unblinded_ghost = pygame.image.load('./resources/ghost.png')
    solid_wall = pygame.image.load('./resources/stonebrick_mossy.png')
    fragile_wall = pygame.image.load('./resources/cobblestone_mossy.png')
    food = pygame.image.load('./resources/cookie.png')
    pickaxe = pygame.image.load('./resources/iron_pickaxe.png')
    sword = pygame.image.load('./resources/iron_sword.png')
    elixir = pygame.image.load('./resources/elixir.png')
    win_screen = pygame.image.load('./resources/you_win.png')
    lose_screen = pygame.image.load('./resources/game_over.png')
    background = pygame.image.load('./resources/background.png')