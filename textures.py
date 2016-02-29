import pygame


tile_size = 32
map_size = 16


class Textures:
    """This class doesn't have functionality.
    It needs to keep all textures in one place.

    """
    pacman_right = pygame.image.load('./resources/units/pacman_right.png')
    pacman_left = pygame.image.load('./resources/units/pacman_left.png')
    pacman_up = pygame.image.load('./resources/units/pacman_up.png')
    pacman_down = pygame.image.load('./resources/units/pacman_down.png')

    blind_ghost_right = pygame.image.load('./resources/units/blind_ghost_right.png')
    blind_ghost_left = pygame.image.load('./resources/units/blind_ghost_left.png')
    unblinded_ghost_right = pygame.image.load('./resources/units/unblinded_ghost_right.png')
    unblinded_ghost_left = pygame.image.load('./resources/units/unblinded_ghost_left.png')

    solid_wall = pygame.image.load('./resources/terrain/stonebrick_mossy.png')
    fragile_wall = pygame.image.load('./resources/terrain/cobblestone_mossy.png')

    food = pygame.image.load('./resources/items/cookie.png')
    pickaxe = pygame.image.load('./resources/items/iron_pickaxe.png')
    sword = pygame.image.load('./resources/items/iron_sword.png')
    elixir = pygame.image.load('./resources/items/elixir.png')

    win_screen = pygame.image.load('./resources/you_win.png')
    lose_screen = pygame.image.load('./resources/game_over.png')
    background = pygame.image.load('./resources/background.png')