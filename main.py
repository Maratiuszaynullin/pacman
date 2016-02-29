# coding: utf-8
from dynamic_object import * # import pacman and ghosts
import sys


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))


def game_over(img):
    unblinded_ghost.velocity = 0
    blind_ghost.velocity = 0
    pacman.velocity = 0
    draw_background(screen, img)


def you_win():
    pass
    #if map.count_food() == 0:
       # game_over(Textures.win_screen)


def you_lose():
    if floor(pacman.x) == floor(blind_ghost.x) and floor(pacman.y) == floor(blind_ghost.y):
        game_over(Textures.lose_screen)
    if floor(pacman.x) == floor(unblinded_ghost.x) and floor(pacman.y) == floor(unblinded_ghost.y):
        game_over(Textures.lose_screen)


def draw_objects():
    for y in range(map_size):
        for x in range(map_size):
            if MAP.get(x, y) != None:
                MAP.get(x, y).draw(screen)


def process_events(events, pac):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                pac.direction = 'left'
            elif event.key == K_RIGHT:
                pac.direction = 'right'
            elif event.key == K_UP:
                pac.direction = 'up'
            elif event.key == K_DOWN:
                pac.direction = 'down'
            elif event.key == K_SPACE:
                pac.direction = 'stop'


def tick_timer(x = 0):
    x += 1
    return x


def game_tick():
    process_events(pygame.event.get(), pacman)
    pygame.time.delay(100)
    draw_background(screen, Textures.background)
    unblinded_ghost.game_tick()
    unblinded_ghost.draw(screen)
    blind_ghost.game_tick()
    blind_ghost.draw(screen)
    pacman.game_tick()
    draw_objects()
    pacman.draw(screen)
    you_lose()
    you_win()
    pygame.display.update()


if __name__ == '__main__':
    init_window()
    screen = pygame.display.get_surface()
    while 1:
        game_tick()
