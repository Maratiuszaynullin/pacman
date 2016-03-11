# coding: utf-8
from static_object import *  # import walls, food, bonuses


class Map:
    def __init__(self, filename):
        f = open(filename, 'r')
        txt = f.readlines()
        f.close()
        self.data = [[0] * (16) for i in range(16)]
        for y in range(16):
            for x in range(16):
                if txt[y][x] == 'O':
                    self.data[y][x] = FragileWall(x, y)
                elif txt[y][x] == ".":
                    self.data[y][x] = Food(x, y)
                elif txt[y][x] == 'X':
                    self.data[y][x] = SolidWall(x, y)
                elif txt[y][x] == 'P':
                    self.data[y][x] = Pickaxe(x, y)
                elif txt[y][x] == 'S':
                    self.data[y][x] = Sword(x, y)
                elif txt[y][x] == 'E':
                    self.data[y][x] = Elixir(x, y)
                else:
                    self.data[y][x] = None

    def get(self, x, y):
        return self.data[int(y)][int(x)]

    def count_food(self):
        count = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if type(self.get(x, y)) == Food:
                    count += 1
        return count
