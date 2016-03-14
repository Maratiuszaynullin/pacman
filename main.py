# coding: utf-8
from dynamic_object import *  # import pacman and ghosts
import sys
pacman_lvl = 0
levels = ['./maps/lvl_0', './maps/lvl_1', './maps/lvl_2', './maps/lvl_3', './maps/lvl_4']
max_lvl = 4
MAP = Map(levels[pacman_lvl])
count_all_food = MAP.count_food()
t = 0


def init_window():
    """This function creates a game window."""
    pygame.init()
    pygame.display.set_mode((704, 640))
    pygame.display.set_caption('Pacman')


def draw_background(scr, img=None):
    """This function takes an image and draws the background with this image.
    If the image is not given the background is filled with black color.
    """
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((150, 160, 210))
        scr.blit(bg, (0, 0))


def draw_objects():
    """This function draws static objects."""
    for y in range(map_height):
        for x in range(map_width):
            if m.MAP.get(x, y) is not None:
               m.MAP.get(x, y).draw(screen)


def draw_ghosts():
    """This function draws alive ghosts."""
    if unblinded_ghost.status == 'alive':
        unblinded_ghost.draw(screen)
        unblinded_ghost.game_tick()
    if blind_ghost.status == 'alive':
        blind_ghost.draw(screen)
        blind_ghost.game_tick()


def draw_score(scr, x=160, y=591):
    """This function draws the score during the game."""
    for i in range(10):
        if pacman.score // 10 == i:
            scr.blit(Textures.score[i], (x, y))
    for i in range(10):
        if pacman.score % 10 == i:
            scr.blit(Textures.score[i], (x + 32, y))


def game_over(img):
    """When you win or lose this function draws a
    suitable background and shows your score.
    """
    draw_background(screen, img)
    draw_score(screen, 389, 366)
    process_events(pygame.event.get(), pacman)


def you_win():
    """This function checks if pacman ate all the food on the map.
    Return true or false.
    """
    if pacman.count_food == count_all_food:
        return 'true'
    else:
        return 'false'


def you_lose():
    """This function checks if pacman ran into ghost.
    Return true or false.
    """
    if (floor(pacman.x) == floor(blind_ghost.x) and floor(pacman.y) == floor(blind_ghost.y)) or \
            (floor(pacman.x) == floor(unblinded_ghost.x) and floor(pacman.y) == floor(unblinded_ghost.y)):
        return 'true'
    else:
        return 'false'


def restart_lvl():
    """This function sets initial settings."""
    global count_all_food
    (pacman.x, pacman.y) = (9, 8)
    (blind_ghost.x, blind_ghost.y) = (3, 8)
    (unblinded_ghost.x, unblinded_ghost.y) = (9, 11)
    pacman.direction = unblinded_ghost.direction = 'stop'
    m.MAP = Map(levels[pacman_lvl])
    count_all_food = m.MAP.count_food()
    pacman.count_food = 0
    pacman.score = 0
    pacman.bonus = None
    pacman.velocity = 4.0/10.0
    pacman.image = Textures.pacman_right
    blind_ghost.status = 'alive'
    unblinded_ghost.status = 'alive'


def next_lvl():
    """This function sets initial setting when a player goes to the next lvl."""
    global pacman_lvl
    pacman_lvl += 1
    restart_lvl()


def process_events(events, pac):
    """This function helps to control the game
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
                pac.direction = 'stop'


def game_tick():
    """Functions that are used every tick."""
    process_events(pygame.event.get(), pacman)
    pygame.time.delay(100)
    draw_background(screen, Textures.background)
    draw_ghosts()
    pacman.game_tick()
    pacman.draw(screen)
    draw_objects()
    draw_score(screen)
    print pacman.score
    pygame.display.update()


if __name__ == '__main__':
    init_window()
    screen = pygame.display.get_surface()

    while 1:
        if you_win() == 'true':
            img = Textures.win_screen
            if pacman_lvl == max_lvl:
                pacman_lvl = -1
            pygame.time.delay(50)
            game_over(img)
            pygame.display.update()

        elif you_lose() == 'true':
            pygame.time.delay(50)
            game_over(Textures.lose_screen)
            pygame.display.update()
        else:
            game_tick()
            t += 1
            if t % 10 == 0:
                print "lvl =", pacman_lvl
