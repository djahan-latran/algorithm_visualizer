import unittest
from src.algorithms import LinearSearch, BinarySearch, BubbleSort, SelectionSort, InsertionSort, Bfs, Dfs, Dijkstras
from src.utility.utils import Board

class TestLinearSearch(unittest.TestCase):

    def setUp(self):
        self.value_info = {"positive": [], "neutral": [], "negative": []}
        self.nums = [1, 2, 3, 4, 5]

    def test_value_found(self):
        linear_search = LinearSearch(self.nums, 3, self.value_info)

        gen = linear_search.run()

        for _ in gen:
            pass

        self.assertEqual(linear_search.value_info["positive"], [3])

    def test_value_not_found(self):
        linear_search = LinearSearch(self.nums, 8, self.value_info)

        gen = linear_search.run()

        for _ in gen:
            pass
        
        self.assertEqual(linear_search.value_info["positive"], [])

    def test_key_error(self):
        false_dict = {"positive": [], "neutral": []}

        linear_search = LinearSearch(self.nums, 5, false_dict)

        gen = linear_search.run()

        with self.assertRaises(KeyError):
            for _ in gen:
                pass


class TestBinarySearch(unittest.TestCase):

    def setUp(self):
        self.value_info = {"positive": [], "neutral": [], "negative": []}
        self.nums = [1, 2, 3, 4, 5]

    def test_value_found(self):
        binary_search = BinarySearch(self.nums, 3, self.value_info)

        gen = binary_search.run(self.nums)

        for _ in gen:
            pass

        self.assertEqual(binary_search.value_info["positive"], [3])

    def test_value_not_found(self):
        binary_search = BinarySearch(self.nums, 8, self.value_info)

        gen = binary_search.run(self.nums)

        for _ in gen:
            pass
        
        self.assertEqual(binary_search.value_info["positive"], [])

    def test_key_error(self):
        false_dict = {"positive": [], "neutral": []}

        binary_search = BinarySearch(self.nums, 5, false_dict)

        gen = binary_search.run(self.nums)

        with self.assertRaises(KeyError):
            for _ in gen:
                pass


class TestBubbleSort(unittest.TestCase):

    def setUp(self):
        self.value_info = {"positive": [], "neutral": []}
        self.nums = [4, 8, 7, 1, 5, 6, 3, 2]

    def test_sort(self):
        bubble_sort = BubbleSort(self.nums, self.value_info)

        gen = bubble_sort.run()

        for _ in gen:
            pass

        self.assertEqual(bubble_sort.nums, sorted(self.nums))

    def test_already_sorted(self):
        self.nums = [1, 2, 3, 4, 5, 6, 7, 8]
        bubble_sort = BubbleSort(self.nums, self.value_info)

        gen = bubble_sort.run()

        for _ in gen:
            pass
        
        self.assertEqual(bubble_sort.nums, self.nums)

    def test_empty_list(self):
        self.nums = []
        bubble_sort = BubbleSort(self.nums, self.value_info)

        gen = bubble_sort.run()

        for _ in gen:
            pass
        
        self.assertEqual(bubble_sort.nums, self.nums)

    def test_key_error(self):
        false_dict = {"neutral": []}

        bubble_sort = BubbleSort(self.nums, false_dict)

        gen = bubble_sort.run()

        with self.assertRaises(KeyError):
            for _ in gen:
                pass


class TestSelectionSort(unittest.TestCase):

    def setUp(self):
        self.value_info = {"positive": [], "neutral": []}
        self.nums = [4, 8, 7, 1, 5, 6, 3, 2]

    def test_sort(self):
        selection_sort = SelectionSort(self.nums, self.value_info)

        gen = selection_sort.run()

        for _ in gen:
            pass

        self.assertEqual(selection_sort.nums, sorted(self.nums))

    def test_already_sorted(self):
        self.nums = [1, 2, 3, 4, 5, 6, 7, 8]
        selection_sort = SelectionSort(self.nums, self.value_info)

        gen = selection_sort.run()

        for _ in gen:
            pass
        
        self.assertEqual(selection_sort.nums, self.nums)

    def test_empty_list(self):
        self.nums = []
        selection_sort = SelectionSort(self.nums, self.value_info)

        gen = selection_sort.run()

        for _ in gen:
            pass
        
        self.assertEqual(selection_sort.nums, self.nums)

    def test_key_error(self):
        false_dict = {"neutral": []}

        selection_sort = SelectionSort(self.nums, false_dict)

        gen = selection_sort.run()

        with self.assertRaises(KeyError):
            for _ in gen:
                pass


class TestInsertionSort(unittest.TestCase):

    def setUp(self):
        self.value_info = {"positive": [], "neutral": []}
        self.nums = [4, 8, 7, 1, 5, 6, 3, 2]

    def test_sort(self):
        insertion_sort = InsertionSort(self.nums, self.value_info)

        gen = insertion_sort.run()

        for _ in gen:
            pass

        self.assertEqual(insertion_sort.nums, sorted(self.nums))

    def test_already_sorted(self):
        self.nums = [1, 2, 3, 4, 5, 6, 7, 8]
        insertion_sort = InsertionSort(self.nums, self.value_info)

        gen = insertion_sort.run()

        for _ in gen:
            pass
        
        self.assertEqual(insertion_sort.nums, self.nums)

    def test_empty_list(self):
        self.nums = []
        insertion_sort = InsertionSort(self.nums, self.value_info)

        gen = insertion_sort.run()

        for _ in gen:
            pass
        
        self.assertEqual(insertion_sort.nums, self.nums)


class TestBfs(unittest.TestCase):

    def setUp(self):
        self.value_info = {"current": None, "visited": None}
        self.board = Board((500, 500), (5, 5))
        self.board.raster[0][3] = 2
        self.target = (0, 3)
    
    def test_value_found(self):
        bfs = Bfs(self.value_info)
        gen = bfs.run(self.board)

        for _ in gen:
            pass

        self.assertEqual(bfs.current, self.target)
    
    def test_value_not_found(self):
        self.board.raster[0][3] = 0
        bfs = Bfs(self.value_info)
        gen = bfs.run(self.board)

        for _ in gen:
            pass

        self.assertNotEqual(bfs.current, self.target)

    #board.raster key/index not found?

class TestDfs(unittest.TestCase):

    def setUp(self):
        self.value_info = {"current": None, "visited": None}
        self.board = Board((500, 500), (5, 5))
        self.board.raster[0][3] = 2
        self.target = (0, 3)
    
    def test_value_found(self):
        dfs = Dfs(self.value_info)
        gen = dfs.run(0, 0, self.board)

        for _ in gen:
            pass

        self.assertEqual(dfs.value_info["current"], self.target)
    
    def test_value_not_found(self):
        self.board.raster[0][3] = 0
        dfs = Dfs(self.value_info)
        gen = dfs.run(0, 0, self.board)

        for _ in gen:
            pass

        self.assertNotEqual(dfs.value_info["current"], self.target)


class TestDijkstras(unittest.TestCase):
    
    def setUp(self):
        self.value_info = {"current": None, "visited": None}
        self.board = Board((500, 500), (5, 5))
        self.board.raster[1][3] = 2
        self.target = (1, 3)
    
    def test_value_found(self):
        dijkstra = Dijkstras(self.value_info)
        gen = dijkstra.run(self.board)

        for _ in gen:
            pass

        self.assertEqual(dijkstra.value_info["current"], self.target)

    def test_value_not_found(self):
        self.board.raster[1][3] = 0

        dijkstra = Dijkstras(self.value_info)
        gen = dijkstra.run(self.board)

        for _ in gen:
            pass

        self.assertNotEqual(dijkstra.value_info["current"], self.target)

    def test_correct_path_returned(self):
        dijkstra = Dijkstras(self.value_info)
        gen = dijkstra.run(self.board)

        shortest_path = {(0, 1), (0, 0), (0, 3), (0, 2), (1, 3)}

        for _ in gen:
            pass

        self.assertEqual(dijkstra.value_info["path"], shortest_path)


if __name__ == "__main__":
    unittest.main()