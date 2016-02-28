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
                pac.direction = 3
            elif event.key == K_RIGHT:
                pac.direction = 1
            elif event.key == K_UP:
                pac.direction = 4
            elif event.key == K_DOWN:
                pac.direction = 2
            elif event.key == K_SPACE:
                pac.direction = 0


def tick_timer(x = 0):
    x += 1
    return x


def game_tick():
    process_events(pygame.event.get(), pacman)
    pygame.time.delay(100)
    draw_background(screen, background)
    #unblinded_ghost.game_tick()
    #unblinded_ghost.draw(screen)
    blind_ghost.game_tick()
    blind_ghost.draw(screen)
    pacman.game_tick()
    draw_objects()
    pacman.draw(screen)
    pygame.display.update()


if __name__ == '__main__':
    tile_size = 32
    map_size = 16
    init_window()
    #unblinded_ghost = UnblindedGhost(8, 4)
    blind_ghost = BlindGhost(5, 11)
    pacman = Pacman(5, 8)
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()
    while 1:
        game_tick()
