"""A modul containen different search, sort and pathfinding algorithm classes for the AnimationCanvas"""
import random
from visualizer import AnimationCanvas

class Parameters:
    def __init__(self, size, speed):
        self.size = size
        self.speed = speed

    def create_values(self):
        return random.sample(range(100), self.size)

class LinearSearch:
    def __init__(self):
        pass

class BinarySearch:
    def __init__(self):
        pass

class BubbleSort:
    def __init__(self, nums, canvas):
        self.canvas = canvas
        self.nums = nums
        self.value_info = {"positive": [], "neutral": [], "negative": []}

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
                    self.value_info["neutral"] = [self.nums[j], self.nums[j+1]]

                    self.canvas.draw_bar_graphs(self.nums, self.value_info)
                    #yield info to visualizer
                    yield

            #store the value that got sorted
            self.value_info["positive"].append(self.nums[j+1])
            
            #edge condition to declare leftest bar graph as 'sorted' at the end
            if i == 1:
                self.value_info["positive"].append(self.nums[j])
            
            #yield info to visualizer
            self.canvas.draw_bar_graphs(self.nums, self.value_info)
            yield


class SelectionSort:
    def __init__(self, nums, canvas):
        self.nums = nums
        self.canvas = canvas
        self.value_info = {"positive": [], "neutral": [], "negative": []}

    def run(self):
         for i in range(len(self.nums)):
            for j in range(i+1, len(self.nums)):
                if self.nums[j] < self.nums[i]:
                    tmp = self.nums[j]
                    self.nums[j] = self.nums[i]
                    self.nums[i] = tmp
                self.value_info["neutral"] = [self.nums[i], self.nums[j]]
                self.canvas.draw_bar_graphs(self.nums, self.value_info)
                yield
            
            self.value_info["positive"].append(self.nums[i])
            self.canvas.draw_bar_graphs(self.nums, self.value_info)
            yield

class InsertionSort:
    def __init__(self, nums, canvas):
        self.nums = nums
        self.canvas = canvas
        self.value_info = {"positive": [], "neutral": [], "negative": []}
    
    def run(self):
        for i in range(1, len(self.nums)):
            tmp = self.nums[i]
            j = i-1
            while tmp < self.nums[j] and j >= 0:
                self.nums[j+1] = self.nums[j]
                self.nums[j] = tmp

                if j > 0:
                    self.value_info["neutral"] = [self.nums[j-1], self.nums[j]]
                else:
                    self.value_info["neutral"] = [self.nums[j]]

                self.canvas.draw_bar_graphs(self.nums, self.value_info)
                yield
                j -= 1

        sorted_values = [value for value in self.nums]
        self.value_info["positive"] = sorted_values
        self.canvas.draw_bar_graphs(self.nums, self.value_info)
        yield

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