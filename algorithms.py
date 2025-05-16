"""A modul containen different search, sort and pathfinding algorithm classes for the AnimationCanvas"""
from collections import deque


class AlgorithmModel:
    def __init__(self):
        pass
    
    def run(self):
        pass


class LinearSearch:
    def __init__(self, nums, value, value_info):
        self.nums = nums
        self.value = value
        self.value_info = value_info

    def run(self):
        for i in range(len(self.nums)):
            if self.nums[i] == self.value:
                self.value_info["positive"] = [self.nums[i]]
                
                yield

                break
            else:
                self.value_info["neutral"] = [self.nums[i]]

                yield

                self.value_info["negative"].append(self.nums[i])
                self.value_info["neutral"] = []


class BinarySearch:
    def __init__(self, nums, value, value_info):
        self.original_nums = nums
        self.value = value
        self.value_info = value_info

    def run(self, nums):

        #get mid index of list
        mid = len(nums)//2

        self.value_info["neutral"] = [nums[mid]]

        yield

        if nums[mid] == self.value:
            self.value_info["positive"] = [self.value]
            for i in range(len(nums)):
                if nums[i] != self.value:
                    self.value_info["negative"].append(nums[i])

            yield

        elif nums[mid] < self.value:
            for i in range(mid):
                self.value_info["negative"].append(nums[i])
            self.value_info["negative"].append(nums[mid])

            yield

            right = nums[mid:]

            yield from self.run(right)

        else:
            for i in range(mid, len(nums)):
                self.value_info["negative"].append(nums[i])
            
            yield

            left = nums[:mid]

            yield from self.run(left)


class BubbleSort:
    def __init__(self, nums, value_info):
        self.nums = nums
        self.value_info = value_info

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

                    #yield info to visualizer
                    yield

            #store the value that got sorted
            self.value_info["positive"].append(self.nums[j+1])
            
            #edge condition to declare leftest bar graph as 'sorted' at the end
            if i == 1:
                self.value_info["positive"].append(self.nums[j])
            
            #yield info to visualizer
            yield


class SelectionSort:
    def __init__(self, nums, value_info):
        self.nums = nums
        self.value_info = value_info

    def run(self):
         for i in range(len(self.nums)):
            for j in range(i+1, len(self.nums)):
                if self.nums[j] < self.nums[i]:
                    tmp = self.nums[j]
                    self.nums[j] = self.nums[i]
                    self.nums[i] = tmp
                self.value_info["neutral"] = [self.nums[i], self.nums[j]]
                
                yield
            
            self.value_info["positive"].append(self.nums[i])

            yield


class InsertionSort:
    def __init__(self, nums, value_info):
        self.nums = nums
        self.value_info = value_info
    
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

                yield

                j -= 1

        sorted_values = [value for value in self.nums]
        self.value_info["positive"] = sorted_values

        yield


class MergeSort:
    def __init__(self):
        pass


class QuickSort:
    def __init__(self):
        pass


class Bfs:
    def __init__(self, value_info):
        self.start_pos = (0, 0)
        self.target = 2
        self.value_info = value_info

    def run(self, board):
        queue = deque([self.start_pos])
        visited = set([self.start_pos])
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)] #right, left, up, down

        for i in range(board.rows):
            for j in range(board.cols):
                if board.raster[i][j] == 1:
                    visited.add((i, j))

        while queue:
            x, y = queue.popleft()
            current = (x, y)

            if board.raster[x][y] == self.target:
                return 

            self.value_info["current"] = current
            self.value_info["visited"] = visited
            
            yield

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                if 0 <= new_x < board.rows and 0 <= new_y < board.cols and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))

        return print("Error: No end-pos found")

class Dfs:
    def __init__(self, value_info):
        self.value_info = value_info
        self.visited = set()
        self.target = 2
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def run(self, pos_x, pos_y, board):
        
        if  pos_x < 0 or pos_y < 0 or pos_x >= board.rows or pos_y >= board.cols or (pos_x, pos_y) in self.visited or board.raster[pos_x][pos_y] == 1:
            return
        
        self.value_info["current"] = (pos_x, pos_y)

        yield

        self.visited.add((pos_x, pos_y))
        self.value_info["visited"] = self.visited

        if board.raster[pos_x][pos_y] == self.target:
            
            yield

            return True

        for dx, dy in self.directions:

            result = yield from self.run(pos_x + dx, pos_y + dy, board)

            if result == True:
                return True


class Astar:
    def __init__(self):
        pass


class Dijkstras:
    def __init__(self):
        pass