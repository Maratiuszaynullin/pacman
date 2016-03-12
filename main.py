# coding: utf-8
from dynamic_object import *  # import pacman and ghosts
from map import *
import sys
pacman_lvl = 0
levels = ['./maps/lvl_0', './maps/lvl_1', './maps/lvl_2', './maps/lvl_3', './maps/lvl_4']
MAP = Map(levels[pacman_lvl])
count_all_food = MAP.count_food()
t = 0


def init_window():
    pygame.init()
    pygame.display.set_mode((704, 640))
    pygame.display.set_caption('Pacman')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((150, 160, 210))
        scr.blit(bg, (0, 0))


def score(count_food):
    return pacman.count_food


def game_over(img):
    process_events(pygame.event.get(), pacman)
    draw_background(screen, img)
    you_score = score(pacman.count_food)
    print('You score', you_score)


def you_win():
    if pacman.count_food == count_all_food:
        return 'true'
    else:
        return 'false'


def you_lose():
    if (floor(pacman.x) == floor(blind_ghost.x) and floor(pacman.y) == floor(blind_ghost.y)) or \
            (floor(pacman.x) == floor(unblinded_ghost.x) and floor(pacman.y) == floor(unblinded_ghost.y)):
        return 'true'
    else:
        return 'false'


"""def set_map():
    global MAP
    if you_lose() == 'true':
        MAP = Map('./maps/lvl_1')
    else: MAP = MAP = Map('./maps/lvl_0')
    return MAP
MAP = set_map()"""


def restart_lvl():
    (pacman.x, pacman.y) = (5, 8)
    (blind_ghost.x, blind_ghost.y) = (2, 8)
    (unblinded_ghost.x, unblinded_ghost.y) = (6, 11)
    pacman.direction = unblinded_ghost.direction = 'stop'
    m.MAP = Map(levels[pacman_lvl])
    global count_all_food
    count_all_food = m.MAP.count_food()
    pacman.count_food = 0
    pacman.score = 0
    pacman.bonus = None
    blind_ghost.status = 'alive'
    unblinded_ghost.status = 'alive'


def next_lvl():
    draw_background(screen, Textures.background)
    pygame.display.update()
    pygame.time.delay(1000)
    global pacman_lvl, count_all_food
    pacman_lvl += 1
    pacman.count_food = 0
    pacman.direction = unblinded_ghost.direction = 'stop'
    (pacman.x, pacman.y) = (5, 8)
    (blind_ghost.x, blind_ghost.y) = (2, 8)
    (unblinded_ghost.x, unblinded_ghost.y) = (6, 11)
    m.MAP = Map(levels[pacman_lvl])
    count_all_food = m.MAP.count_food()
    pacman.score = 0
    pacman.bonus = None
    blind_ghost.status = 'alive'
    unblinded_ghost.status = 'alive'


def draw_objects():
    for y in range(map_height):
        for x in range(map_width):
            if m.MAP.get(x, y) != None:
               m. MAP.get(x, y).draw(screen)


def draw_ghosts():
    """This function draw alive ghosts."""
    if unblinded_ghost.status == 'alive':
        unblinded_ghost.draw(screen)
        unblinded_ghost.game_tick()
    if blind_ghost.status == 'alive':
        blind_ghost.draw(screen)
        blind_ghost.game_tick()


def process_events(events, pac):
    for event in events:
        if you_win() == 'true':
            if event.type == KEYDOWN and event.key == K_RETURN:
                next_lvl()
        elif you_lose() == 'true':
            if event.type == KEYDOWN and event.key == K_RETURN:
                restart_lvl()

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


def game_tick():
    process_events(pygame.event.get(), pacman)
    pygame.time.delay(100)
    draw_background(screen, Textures.background)
    draw_ghosts()
    pacman.game_tick()
    pacman.draw(screen)
    draw_objects()
    pygame.display.update()


if __name__ == '__main__':
    init_window()
    screen = pygame.display.get_surface()

    while 1:
        if you_win() == 'true':
            pygame.time.delay(1000)
            game_over(Textures.win_screen)
            pygame.display.update()
        elif you_lose() == 'true':
            pygame.time.delay(1000)
            game_over(Textures.lose_screen)
            pygame.display.update()
        else:
            game_tick()
            t += 1
            if t % 10 == 0:
                print "lvl =", pacman_lvl

