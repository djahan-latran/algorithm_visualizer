"""A modul containen different search, sort and pathfinding algorithm classes for the AnimationCanvas"""
import random
from visualizer import AnimationCanvas
from collections import deque

class Parameters:
    def __init__(self, size):
        #Initialize size and speed attributes
        self.size = size

    def create_values(self):
        #Create values attribute
        self.values = random.sample(range(100), self.size)
        return self.values

    def create_value_to_find(self):
        if self.values:
            idx = random.randint(0, self.size-1)
            value_to_find = self.values[idx]
            return value_to_find


class LinearSearch:
    def __init__(self, nums, canvas, value):
        self.nums = nums
        self.canvas = canvas
        self.value = value
        self.value_info = {"positive": [], "neutral": [], "negative": []}

    def run(self):
        for i in range(len(self.nums)):
            if self.nums[i] == self.value:
                self.value_info["positive"] = [self.nums[i]]
                self.canvas.draw_bar_graphs(self.nums, self.value_info)
                yield
                break
            else:
                self.value_info["neutral"] = [self.nums[i]]
                self.canvas.draw_bar_graphs(self.nums, self.value_info)
                yield
                self.value_info["negative"].append(self.nums[i])
                self.value_info["neutral"] = []


class BinarySearch:
    def __init__(self, nums, canvas, value):
        self.original_nums = nums
        self.canvas = canvas
        self.value = value
        self.value_info = {"positive": [], "neutral": [], "negative": []}

    def run(self, nums):

        #get mid index of list
        mid = len(nums)//2

        self.value_info["neutral"] = [nums[mid]]
        self.canvas.draw_bar_graphs(self.original_nums, self.value_info)
        yield

        if nums[mid] == self.value:
            self.value_info["positive"] = [self.value]
            for i in range(len(nums)):
                if nums[i] != self.value:
                    self.value_info["negative"].append(nums[i])
            self.canvas.draw_bar_graphs(self.original_nums, self.value_info)
            yield

        elif nums[mid] < self.value:
            for i in range(mid):
                self.value_info["negative"].append(nums[i])
            self.value_info["negative"].append(nums[mid])

            self.canvas.draw_bar_graphs(self.original_nums, self.value_info)
            yield
            right = nums[mid:]
            yield from self.run(right)
        else:
            for i in range(mid, len(nums)):
                self.value_info["negative"].append(nums[i])
            
            self.canvas.draw_bar_graphs(self.original_nums, self.value_info)
            yield

            left = nums[:mid]
            yield from self.run(left)


class BubbleSort:
    def __init__(self, nums, canvas):
        self.nums = nums
        self.canvas = canvas
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
    def __init__(self, canvas):
        self.canvas = canvas
        self.rect_info = {"current": None, "visited": None}
    
    def run(self):
        rows = len(self.board)
        cols = len(self.board[0])
        queue = deque([start_pos])
        visited = set([start_pos])
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)] #right, left, up, down

        for i in range(rows):
            for j in range(cols):
                if board[i][j] == 1:
                    visited.add((i, j))

        while queue:
            #pg.event.pump()
            x, y = queue.popleft()
            current = (x, y)

            if (x, y) == end_pos:
                return 

            draw_board(screen, board, visited, end_pos, current)

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))

        return print("Error: No end-pos found")

class Dfs:
    def __init__(self):
        pass


class Astar:
    def __init__(self):
        pass


class Dijkstras:
    def __init__(self):
        pass