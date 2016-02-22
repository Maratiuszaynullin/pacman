import sys
import pygame
from pygame.locals import *
from math import floor
import random

def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')

def draw_objects():
    for y in range(map_size):
        for x in range(map_size):
            if map.get(x, y) != None:
                map.get(x, y).draw(screen)

def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))

def game_over(img):
    unblinded_ghost_Marat.velocity = 0
    unblinded_ghost_Ksenia.velocity = 0
    blind_ghost.velocity = 0
    pacman.velocity = 0
    draw_background(screen, img)

def you_win():
    win_screen = pygame.image.load('./resources/you_win.png')
    if map.count_food() == 0:
        game_over(win_screen)
        draw_background(screen, win_screen)

def you_lose(): #FIXME
    lose_screen = pygame.image.load('./resources/game_over.png')
    if (floor(pacman.x) == floor(unblinded_ghost_Marat.x)) and (floor(pacman.y) == floor(unblinded_ghost_Marat.y)):
        game_over(lose_screen)
    if floor(pacman.x) == floor(unblinded_ghost_Ksenia.x) and floor(pacman.y) == floor(unblinded_ghost_Ksenia .y):
        game_over(lose_screen)
    if floor(pacman.x) == floor(blind_ghost.x) and floor(pacman.y) == floor(blind_ghost .y):
        game_over(lose_screen)


class Map:
    def __init__(self, filename):
        f = open('map', 'r')
        txt = f.readlines()
        f.close()
        self.data = [[0]*(len(txt)) for i in range(len(txt))]
        for y in range(len(txt)):
            for x in range(len(txt)):
                if txt[y][x] == 'O':
                    self.data[y][x] = Wall(x, y)
                elif txt[y][x] == ".":
                    self.data[y][x] = Food(x, y)
                elif txt[y][x] == 'X':
                    self.data[y][x] = Immortal_wall(x, y)
                else:
                    self.data[y][x] = None

    def get(self, x, y):
        return self.data[y][x]

    def count_food(self):
        count = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if type(self.get(x, y)) == Food:
                    count += 1
        return count


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))

#FIXME proverky na nalichie sten sdelat' function v class Ghost, Inblinded_ghost, Pacman
class Ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Ghost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if type(map.get(int(self.x + self.velocity), int(self.y))) != Immortal_wall and type(map.get(int(self.x + self.velocity), int(self.y))) != Wall:
                self.x += self.velocity
            else:
                self.direction = random.randint(1, 4)

            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)

        elif self.direction == 2:
            if type(map.get(int(self.x), int(self.y + self.velocity))) != Immortal_wall and type(map.get(int(self.x), int(self.y + self.velocity))) != Wall:
                self.y += self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)

        elif self.direction == 3:
            if type(map.get(int(self.x - self.velocity), int(self.y))) != Immortal_wall and type(map.get(int(self.x - self.velocity), int(self.y))) != Wall:
                self.x -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)

        elif self.direction == 4:
            if type(map.get(int(self.x), int(self.y - self.velocity))) != Immortal_wall and type(map.get(int(self.x), int(self.y - self.velocity))) != Wall:
                self.y -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)


class Unblinded_ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 3.95 / 10.0

    def game_tick(self):
        super(Unblinded_ghost, self).game_tick()

        if floor(self.y) == floor(pacman.y):
            if (floor(self.x) > floor(pacman.x)):
                for i in range(int(abs(self.x - pacman.x))+1):
                    if type(map.get(int(self.x - i), int(self.y))) == Immortal_wall or type(map.get(int(self.x - i), int(self.y))) == Wall:
                        self.direction = 0
                        break
                    else:
                        self.direction = 3
            else:
                for i in range(int(abs(self.x - pacman.x))):
                    if type(map.get(int(self.x + i), int(self.y))) == Immortal_wall or type(map.get(int(self.x + i), int(self.y))) == Wall:
                        self.direction = 0
                        break
                    else:
                        self.direction = 1

        elif floor(self.x) == floor(pacman.x):
            if floor(self.y) > floor(pacman.y):
                for i in range(int(abs(self.y - pacman.y))+1):
                    if type(map.get(int(self.x), int(self.y - i))) == Immortal_wall or type(map.get(int(self.x), int(self.y - i))) == Wall:
                        self.direction = 0
                        break
                    else:
                        self.direction = 4

            else:
                for i in range(int(abs(self.y - pacman.y))):
                    if type(map.get(int(self.x), int(self.y + i))) == Immortal_wall or type(map.get(int(self.x), int(self.y + i))) == Wall:
                        self.direction = 0
                        break
                    else:
                        self.direction = 2


        if self.direction == 0:
            self.direction = random.randint(1, 4)


        if self.direction == 1:
            if type(map.get(int(self.x + self.velocity), int(self.y))) != Immortal_wall and type(map.get(int(self.x + self.velocity), int(self.y))) != Wall:
                self.x += self.velocity
            else:
                self.direction = random.randint(2, 4)

            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(2, 4)

        elif self.direction == 2:
            if type(map.get(int(self.x), int(self.y + self.velocity))) != Immortal_wall and type(map.get(int(self.x), int(self.y + self.velocity))) != Wall:
                self.y += self.velocity
            else:
                self.direction = random.choice((2, 3, 4))
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.choice((2, 3, 4))

        elif self.direction == 3:
            if type(map.get(int(self.x - self.velocity), int(self.y))) != Immortal_wall and type(map.get(int(self.x - self.velocity), int(self.y))) != Wall:
                self.x -= self.velocity
            else:
                self.direction = random.choice((1, 2, 4))
            if self.x <= 0:
                self.x = 0
                self.direction = random.choice((1, 2, 4))

        elif self.direction == 4:
            if type(map.get(int(self.x), int(self.y - self.velocity))) != Immortal_wall and type(map.get(int(self.x), int(self.y - self.velocity))) != Wall:
                self.y -= self.velocity
            else:
                self.direction = random.randint(1, 3)
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 3)

        self.set_coord(self.x, self.y)


class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        self.direction = 0
        self.velocity = 4.0 / 10.0
        self.image = './resources/pacman_right.png'
        GameObject.__init__(self, self.image, x, y, tile_size, map_size)


    def direction_image(self, direction):
        if direction == 1:
            self.image = pygame.image.load('./resources/pacman_right.png')
        elif self.direction == 2:
            self.image = pygame.image.load('./resources/pacman_down.png')
        elif self.direction == 3:
            self.image = pygame.image.load('./resources/pacman_left.png')
        elif self.direction == 4:
            self.image = pygame.image.load('./resources/pacman_up.png')


    def eat_food(self):
        if type(map.get(int(self.x), int(self.y))) == Food:
            map.data[int(self.y)][int(self.x)] = None

    def crush_wall(self):
        if type(map.get(int(self.x), int(self.y))) == Wall:
            map.data[int(self.y)][int(self.x)] = None

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if type(map.get(int(self.x + self.velocity), int(self.y))) != Immortal_wall:
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if type(map.get(int(self.x), int(self.y + self.velocity))) != Immortal_wall:
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if type(map.get(int(self.x - self.velocity), int(self.y))) != Immortal_wall:
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if type(map.get(int(self.x), int(self.y - self.velocity))) != Immortal_wall:
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.eat_food()
        self.crush_wall()
        self.direction_image(self.direction)
        self.set_coord(self.x, self.y)


class Wall(GameObject):
    def __init__(self, x, y, tile_size=32, map_size=16):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)


class Immortal_wall(GameObject):
    def __init__(self, x, y, tile_size=32, map_size=16):
        GameObject.__init__(self, './resources/immortal_wall.png', x, y, tile_size, map_size)


class Food(GameObject):
    def __init__(self, x, y, tile_size=32, map_size=16):
        GameObject.__init__(self, './resources/food.png', x, y, tile_size, map_size)


def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0

#FIXME sdelat' creator dlya ghosts
if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 16

    unblinded_ghost_Ksenia = Unblinded_ghost(8, 10, tile_size, map_size)
    unblinded_ghost_Marat = Unblinded_ghost(8, 4, tile_size, map_size)
    blind_ghost = Ghost(0, 0, tile_size, map_size)
    pacman = Pacman(5, 5, tile_size, map_size)


    map = Map('map')
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)

        unblinded_ghost_Ksenia.game_tick()
        unblinded_ghost_Marat.game_tick()
        blind_ghost.game_tick()
        pacman.game_tick()

        draw_background(screen, background)
        draw_objects()

        pacman.draw(screen)
        unblinded_ghost_Ksenia.draw(screen)
        unblinded_ghost_Marat.draw(screen)
        blind_ghost.draw(screen)
        you_win()
        #you_lose()
        pygame.display.update()


