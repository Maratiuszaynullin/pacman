# coding: utf-8
from static_object import *
"""изменить каунт для еды"""


class Map:
    def __init__(self, filename):
        f = open(filename, 'r')
        txt = f.readlines()
        f.close()
        self.data = [[0] * (16) for i in range(16)]
        for y in range(16):
            for x in range(len(txt)):
                if txt[y][x] == 'O':
                    self.data[y][x] = FragileWall(x, y)
                elif txt[y][x] == ".":
                    self.data[y][x] = Food(x, y)
                elif txt[y][x] == 'X':
                    self.data[y][x] = SolidWall(x, y)
                    # elif txt[y][x] == 'S':
                    # self.data[y][x] = Speed_bonus(x, y)
                else:
                    self.data[y][x] = None

    def get(self, x, y):
        return self.data[int(y)][int(x)]

    """def count_food(self):
        count = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if type(self.get(x, y)) == Food:
                    count += 1
        return count"""


global MAP
MAP = Map('./maps/map')
