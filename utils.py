import random


class Parameters:

    def __init__(self, size):
        #Initialize size and speed attributes
        self.size = size

    def create_values(self):
        #Create values attribute
        self.values = random.sample(range(100), self.size)
        return self.values

    def create_value_to_find(self):
        idx = random.randint(0, self.size-1)
        value_to_find = self.values[idx]
        return value_to_find


class Board:

    def __init__(self, surface_size, rect_amount):
        #Create a 2d matrix that represents a checkerboard

        self.rows = rect_amount[1]
        self.cols = rect_amount[0]

        self.rect_size = surface_size[0] // rect_amount[0]
        
        #Initialize empty list
        self.raster = []

        #2d list filled with 0s to represent checkerboard structure
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(0)
            self.raster.append(row)

    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.raster[i][j] = 0
        