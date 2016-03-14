from static_object import *  # import walls, food, bonuses


class Map:
    """This class describes game map."""
    def __init__(self, filename):
        """This function reads a txt file and creates a two-dimensional list
        with static objects references.
        """
        f = open(filename, 'r')
        txt = f.readlines()
        f.close()
        self.data = [[0] * (map_width) for i in range(map_height)]
        for y in range(map_height):
            for x in range(map_width):
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
        """This function returns a static object with given coordinates."""
        return self.data[int(y)][int(x)]

    def count_food(self):
        """This function counts how many food is on the map.
        It is necessary for drawing a map.
        """
        count = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if type(self.get(x, y)) == Food:
                    count += 1
        return count
