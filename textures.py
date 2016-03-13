import pygame


tile_size = 32
map_width = 20
map_height = 16


class Textures:
    """This class doesn't have functionality.
    It needs to keep all textures in one place.
    """
    pacman_right = pygame.image.load('./resources/units/pacman_right.png')
    pacman_left = pygame.image.load('./resources/units/pacman_left.png')
    pacman_up = pygame.image.load('./resources/units/pacman_up.png')
    pacman_down = pygame.image.load('./resources/units/pacman_down.png')

    pacman_right_with_pickaxe = pygame.image.load('./resources/units/pacman_right_with_pickaxe.png')
    pacman_left_with_pickaxe = pygame.image.load('./resources/units/pacman_left_with_pickaxe.png')
    pacman_up_with_pickaxe = pygame.image.load('./resources/units/pacman_up_with_pickaxe.png')
    pacman_down_with_pickaxe = pygame.image.load('./resources/units/pacman_down_with_pickaxe.png')

    pacman_right_with_elixir = pygame.image.load('./resources/units/pacman_right_with_elixir.png')
    pacman_left_with_elixir = pygame.image.load('./resources/units/pacman_left_with_elixir.png')
    pacman_up_with_elixir = pygame.image.load('./resources/units/pacman_up_with_elixir.png')
    pacman_down_with_elixir = pygame.image.load('./resources/units/pacman_down_with_elixir.png')

    pacman_right_with_sword = pygame.image.load('./resources/units/pacman_right_with_sword.png')
    pacman_left_with_sword = pygame.image.load('./resources/units/pacman_left_with_sword.png')
    pacman_up_with_sword = pygame.image.load('./resources/units/pacman_up_with_sword.png')
    pacman_down_with_sword = pygame.image.load('./resources/units/pacman_down_with_sword.png')

    blind_ghost_right = pygame.image.load('./resources/units/blind_ghost_right.png')
    blind_ghost_left = pygame.image.load('./resources/units/blind_ghost_left.png')
    unblinded_ghost_right = pygame.image.load('./resources/units/unblinded_ghost_right.png')
    unblinded_ghost_left = pygame.image.load('./resources/units/unblinded_ghost_left.png')

    solid_wall = pygame.image.load('./resources/terrain/shadow_1.png')
    fragile_wall = pygame.image.load('./resources/terrain/shadow_2.png')

    food = pygame.image.load('./resources/items/cookie.png')
    pickaxe = pygame.image.load('./resources/items/iron_pickaxe.png')
    sword = pygame.image.load('./resources/items/iron_sword.png')
    elixir = pygame.image.load('./resources/items/elixir.png')

    win_screen = pygame.image.load('./resources/win_screen.png')
    lose_screen = pygame.image.load('./resources/lose_screen.png')
    background = pygame.image.load('./resources/background.png')
    gui1 = pygame.image.load('./resources/gui1.png')