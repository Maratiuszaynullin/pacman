from dynamic_object import *  # import pacman and ghosts
from map import *  # import class map, static objects, textures
import sys
pacman_lvl = 0
levels = ['./maps/lvl_0', './maps/lvl_1', './maps/lvl_2', './maps/lvl_3', './maps/lvl_4']
MAP = Map(levels[pacman_lvl])
count_all_food = MAP.count_food()
t = 0


def init_window():
    """This function create game window."""
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')


def draw_background(scr, img=None):
    """This function takes image and draw background with this image.
    If image is not given background is filled with black color.
    """
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((150, 160, 210))
        scr.blit(bg, (0, 0))


def score(count_food):
    """This function returns your score."""
    return pacman.count_food


def game_over(img):
    """When you win or lose this function draw
    suitable background and show your score.
    """
    process_events(pygame.event.get(), pacman)
    draw_background(screen, img)
    you_score = score(pacman.count_food)
    print('You score', you_score)


def you_win():
    """This function checks if pacman ate all the food on the map.
    Return true or false.
    """
    if pacman.count_food == count_all_food:
        return 'true'
    else:
        return 'false'


def new_game():
    """This function sets locations of dynamic object
    at the beginning of the game.
    """
    pacman.x = 5
    pacman.y = 8
    blind_ghost.x = 5
    blind_ghost.y = 11


def you_lose():
    """This function checks if pacman ran into ghost.
    Return true or false.
    """
    if ((floor(pacman.x) == floor(blind_ghost.x)
        and floor(pacman.y) == floor(blind_ghost.y))
        or (floor(pacman.x) == floor(unblinded_ghost.x)
        and floor(pacman.y) == floor(unblinded_ghost.y))):
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
    """This function sets new game arguments."""
    (pacman.x, pacman.y) = (5, 8)
    (blind_ghost.x, blind_ghost.y) = (2, 8)
    (unblinded_ghost.x, unblinded_ghost.y) = (6, 11)
    pacman.direction = unblinded_ghost.direction = 'stop'
    m.MAP = Map(levels[pacman_lvl])
    global count_all_food
    count_all_food = m.MAP.count_food()
    pacman.count_food = 0


def next_lvl():
    """This function sets next level arguments."""
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


def draw_objects():
    """This function draw statis objects."""
    for y in range(map_size):
        for x in range(map_size):
            if m.MAP.get(x, y) != None:
               m.MAP.get(x, y).draw(screen)


def process_events(events, pac):
    """This function help control the game
    (pacman, restart game, continue game) with keyboard.
    """
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
                pac.direction = 0


"""def tick_timer(x = 0):
    x += 1
    pac.direction = 'stop'"""

def game_tick():
    """Functions that are used every tick."""
    process_events(pygame.event.get(), pacman)
    pygame.time.delay(100)
    draw_background(screen, Textures.background)
    unblinded_ghost.game_tick()
    unblinded_ghost.draw(screen)
    #tick_timer()
    blind_ghost.game_tick()
    blind_ghost.draw(screen)
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
