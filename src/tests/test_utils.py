import unittest
from unittest.mock import patch, mock_open
from src.utility.utils import Parameters, Board, FileReader
import yaml


class TestParameters(unittest.TestCase):
    """
    Unittest class for the Parameters class from utils.
    """
    def test_init_positive(self):
        """
        Tests Parameter's size attribute
        """
        parameters = Parameters(5)

        self.assertEqual(parameters.size, 5)
    
    def test_init_negative(self):
        """
        Tests if ValueError gets raised properly by the constructor if attribute is 0
        """
        with self.assertRaises(ValueError):
            Parameters(0)
    
    def test_create_values(self):
        """
        Tests if Parameters value attribute is instance of a list, the length of the list is right
        and each value is between 1 and 100.
        """
        parameters = Parameters(5)

        parameters.create_values()

        self.assertIsInstance(parameters.values, list)
        self.assertEqual(len(parameters.values), 5)
        self.assertTrue(all(1 <= value <= 100 for value in parameters.values))

    def test_create_value_to_find(self):
        """
        Tests if the created value is part of the value list.
        """
        parameters = Parameters(5)

        value_list = parameters.create_values()
        value = parameters.create_value_to_find()
        
        self.assertIn(value, value_list)


class TestBoard(unittest.TestCase):
    """
    Unittest class for the Board class from utils.
    """
    def test_init_positive(self):
        """
        Tests if the board.raster attribute is an instance of a list and has the proper dimensions.
        """
        board = Board(surface_size=(50, 50), rect_amount=(10, 10))

        rect_size = 5
        test_rect_size = board.rect_size

        self.assertEqual(rect_size, test_rect_size)
        self.assertIsInstance(board.raster, list)
        self.assertEqual(len(board.raster), 10)
        self.assertEqual(len(board.raster[0]), 10)

    def test_init_negative(self):
        """
        Tests if ValueError is raised properly when rect_amount[i] <= 0.
        """
        with self.assertRaises(ValueError):
            Board(surface_size=(50, 50), rect_amount=(0, 10))

    def test_reset(self):
        """
        Tests if Board.reset() properly resets every value to 1.
        """
        board = Board(surface_size=(50,50), rect_amount=(5, 5))
        board.reset()
        raster = board.raster

        self.assertTrue(all(value == 1 for row in raster for value in row))


class TestFileReader(unittest.TestCase):
    """
    Unittest class to test FileReader class from utils.
    """

    @patch("builtins.open", new_callable= mock_open)
    @patch("yaml.safe_load", return_value= {"algo1": {"definition": "Positive"}})
    def test_init_positive(self, mock_yaml_load, mock_yaml_file):
        """
        Uses Mocks to test if the FileReader properly loads and reads a yaml-file.
        Checks if yaml.safe_load gets called.
        """
        
        file_reader = FileReader("directory", "testfile.yaml")
        self.assertEqual(file_reader.info_texts["algo1"]["definition"], "Positive")
        mock_yaml_file.assert_called_once_with("directory\\gui\\testfile.yaml", "r")
    
    @patch("builtins.open", new_callable= mock_open, read_data="4189354891")
    @patch("yaml.safe_load", side_effect= yaml.YAMLError("Broken yaml-file"))
    def test_init_yaml_error(self, mock_yaml_load, mock_yaml_file):
        """
        Uses Mocks to test if the yaml.YAMLError gets raised by the FileReader constructor
        if the data in the file has false formatting.
        """

        with self.assertRaises(yaml.YAMLError):
            FileReader("directory", "testfile.yaml")

    @patch("builtins.open", side_effect= FileNotFoundError)
    def test_init_file_error(self, mock_yaml_load):
        """
        Uses a Mock to test if the FileNotFoundError gets raised by the FileReader constructor.
        """
        
        with self.assertRaises(FileNotFoundError):
            FileReader("directory", "test_missing_file.yaml")


if __name__ == "__main__":
    unittest.main()