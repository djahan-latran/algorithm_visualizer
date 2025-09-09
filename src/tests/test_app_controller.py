import unittest
from unittest.mock import MagicMock, patch
from src.app_controller import AppController
from src.app_states import AppStates
from src.utility.utils import FileReader


class TestAppController(unittest.TestCase):

    @patch("src.app_controller.FileReader")
    def test_init(self, FileReaderMock):
        
        # Mock setup
        mock_file_reader = MagicMock()
        FileReaderMock.return_value = mock_file_reader

        # Initiate AppController
        controller = AppController()

        # Test if FileReader was instanciated twice
        self.assertEqual(FileReaderMock.call_count, 2)
        # Test if controller.states is an instance of AppStates
        self.assertIsInstance(controller.states, AppStates)
    
    def test_algo_button_pressed(self):
        pass

    def test_create_values(self):
        pass

    def test_create_board(self):
        pass

    def test_control_button_pressed(self):
        pass


if __name__ == "__main__":
    unittest.main()

