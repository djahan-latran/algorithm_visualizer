from abc import ABC, abstractmethod
from collections import deque
import heapq

class AlgorithmModel(ABC):
    def __init__(self, value_info):
        """
        Initiates the abstract base class for algorithms.

        Parameters
        ----------

        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.
        """
        self.value_info = value_info
    
    @abstractmethod
    def run(self):
        """
        This method has to be implemented for each algorithm as a generator that yields sub results
        back to the controller so that the view can update the visuals.
        """
        pass


class LinearSearch(AlgorithmModel):
    """
    Basic linear search algorithm that inherites from AlgorithmModel (abstract class).
    The run() method works as a generator and yields sub results for the View.
    """
    def __init__(self, nums, value, value_info):
        """
        Initiate the class and init-method from abstract class.
        
        Parameters
        ----------

        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        nums : list
            The input values in which the algorithm is gonna look for the target.

        value : int
            The target value that the algorithm is searching for.
        """
        super().__init__(value_info)
        self.nums = nums
        self.value = value

    def run(self):
        """
        Runs the algorithm as a generator.
        """
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


class BinarySearch(AlgorithmModel):

    """
    Binary Search algorithm that inherites from abstract class.
    """
    def __init__(self, nums, value, value_info):
        """
        Initiates the class.
        
        Parameters
        ----------
        
        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        nums : list
            The input values in which the algorithm is gonna look for the target.
            
        value : int
            The target value that the algorithm is searching for.
        """
        super().__init__(value_info)
        self.original_nums = nums
        self.value = value

    def run(self, nums):
        """
        Runs the algorithm.
        """

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


class BubbleSort(AlgorithmModel):
    """
    Bubble Sort algorithm that inherites from abstract class.
    """
    def __init__(self, nums, value_info):
        """
        Initiates the class.

        Parameters
        ----------
        
        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        nums : list
            The input values that the algorithm is gonna sort.
        """
        super().__init__(value_info)
        self.nums = nums

    def run(self):
        """
        Runs the algorithm as a generator. Yields sub results to controller.
        """
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


class SelectionSort(AlgorithmModel):
    """
    Selection Sort algorithm that inherites from abstract class.
    """
    def __init__(self, nums, value_info):
        """
        Initiates the class.

        Parameters
        ----------
        
        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        nums : list
            The input values that the algorithm is gonna sort.
        """
        super().__init__(value_info)
        self.nums = nums

    def run(self):
         """
         Runs the algorithm as a generator. Yields sub results to controller.
         """
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


class InsertionSort(AlgorithmModel):
    """
    Insertion Sort algorithm implementation.
    """
    def __init__(self, nums, value_info):
        """
        Initiates the class.

        Parameters
        ----------
        
        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        nums : list
            The input values that the algorithm is gonna sort.
        """
        super().__init__(value_info)
        self.nums = nums
    
    def run(self):
        """
        Runs the algorithm as a generator. Yields subresults to controller.
        """
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


class Bfs(AlgorithmModel):
    """
    Breadth-First-Search algorithm implementation.
    """

    def __init__(self, value_info):
        """
        Initiates the class.

        Parameters
        ----------
        
        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        start_pos : tuple
            Coordinates where the algorithm starts on the grid (2d list)

        target : int
            the value the algorithm is searching for.
        """
        super().__init__(value_info)
        self.start_pos = (0, 0)
        self.target = 2

    def run(self, board):
        """
        Runs algorithm as a generator. Yields subresults to controller.
        
        Parameters
        ----------
        
        board : 2d list
            represents the grid (graph) that gets traversed by the algorithm.
        """
        queue = deque([self.start_pos])
        visited = set([self.start_pos])
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)] #right, left, up, down

        for i in range(board.rows):
            for j in range(board.cols):
                if board.raster[i][j] == -1:
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

class Dfs(AlgorithmModel):
    """
    Depth-First-Search implementation.
    """

    def __init__(self, value_info):
        """
        Initiates the class.

        Parameters
        ----------
        
        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        visited : set
            Holds the coordinates that were already visited.

        target : int
            the value the algorithm is searching for.

        directions : list
            A list of four tuples that represent each direction the algorithm can move on the 2d grid.
        """
        super().__init__(value_info)
        self.visited = set()
        self.target = 2
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def run(self, pos_x, pos_y, board):
        """
        Runs the algorithm as agenerator. Yields subresults to controller.
        
        Parameters
        ----------
        
        board : 2d list
            represents the grid (graph) that gets traversed by the algorithm.
        
        pos_x : int
            starting postion x-ccordinate.
        
        pos_y : int
            starting position y-coordinate.
        """
        
        if  pos_x < 0 or pos_y < 0 or pos_x >= board.rows or pos_y >= board.cols or (pos_x, pos_y) in self.visited or board.raster[pos_x][pos_y] == -1:
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


class Dijkstras(AlgorithmModel):
    """
    Dijkstra algorithm implementation.
    """

    def __init__(self, value_info):
    
        """
        Initiates the class.

        Parameters
        ----------
        
        value_info : dict
            categorises values based on keys. The information is then read by the View to visualize the current state.

        start_pos : tuple
            Coordinates where the algorithm starts on the grid (2d list)

        target : int
            the value the algorithm is searching for.
        
        directions : list
            A list of four tuples that represent each direction the algorithm can move on the 2d grid.
        """
        super().__init__(value_info)
        self.start_pos = (0, 0)
        self.target = 2
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def run(self, board):
        """
        Runs the algorithm as a generator. Yields subresults to controller.

        Parameters
        ----------
        
        board : 2d list
            represents the grid (graph) that gets traversed by the algorithm.

        """
        visited = set([self.start_pos])
        distances = [[float('inf')] * board.cols for _ in range(board.rows)]
        distances[self.start_pos[0]][self.start_pos[1]] = 0

        min_heap = [(0, self.start_pos[0], self.start_pos[1])]
        previous = {}

        value_found = False

        while min_heap:
            dist, row, col = heapq.heappop(min_heap)
            visited.add((row, col))
            self.value_info["current"] = (row, col)
            self.value_info["visited"] = visited

            yield
            
            if board.raster[row][col] == self.target:
                target_pos = (row, col)
                value_found = True
                break

            for direction_row, direction_col in self.directions:
                new_row, new_col = row + direction_row, col + direction_col

                if 0 <= new_row < board.rows and 0 <= new_col < board.cols:
                    if board.raster[new_row][new_col] == -1:
                        continue
                    
                    new_dist = dist + board.raster[new_row][new_col]
                    if new_dist < distances[new_row][new_col]:
                        heapq.heappush(min_heap, (new_dist, new_row, new_col))
                        distances[new_row][new_col] = new_dist
                        previous[(new_row, new_col)] = (row, col)
        
        if value_found:
            shortest_path = set([])
            location = target_pos
            visited.remove(self.start_pos)

            while location in previous:
                shortest_path.add(location)
                visited.remove(location)
                location = previous[location]
                self.value_info["path"] = shortest_path
                yield
            shortest_path.add(self.start_pos)
            self.value_info["path"] = shortest_path
            yield
        else:
            return
        