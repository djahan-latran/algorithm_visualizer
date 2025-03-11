"""A modul containen different search, sort and pathfinding algorithm classes for the AnimationCanvas"""
import random
from visualizer import AnimationCanvas

class Parameters:
    def __init__(self, size, speed):
        self.values = random.sample(range(100), self.size)
        self.speed = speed

class LinearSearch:
    def __init__(self):
        pass

class BinarySearch:
    def __init__(self):
        pass

class BubbleSort:
    def __init__(self, nums):
        self.nums = nums

    def run(self):
        #bubble sort application
        for i in range(len(self.nums), 0, -1):
            for j in range(i-1):
                if self.nums[j] > self.nums[j+1]:
                    tmp = self.nums[j]
                    self.nums[j] = self.nums[j+1]
                    self.nums[j+1] = tmp
                
                #condition to draw unsorted bar graphs during the 'bubble process'
                if j < i-2:
                    #indices of graphs that are currently 'bubbled'
                    self.canvas.draw_info["lightgrey"] = [self.nums[j], self.nums[j+1]]
                    #draw the bar graphs
                    self.canvas.draw_bar_graphs()

            #store the value that got sorted
            self.canvas.draw_info["green"].append(self.nums[j+1])
            
            #edge condition to declare leftest bar graph as 'sorted' at the end
            if i == 1:
                self.canvas.draw_info["green"].append(self.nums[j])
            
            #pass the draw info to the drawing function
            self.canvas.draw_bar_graphs()


class SelectionSort:
    def __init__(self):
        pass

class InsertionSort:
    def __init__(self):
        pass

class MergeSort:
    def __init__(self):
        pass

class QuickSort:
    def __init__(self):
        pass

class Bfs:
    def __init__(self):
        pass

class Dfs:
    def __init__(self):
        pass

class Astar:
    def __init__(self):
        pass

class Dijkstras:
    def __init__(self):
        pass