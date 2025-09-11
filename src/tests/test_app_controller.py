import unittest
from unittest.mock import MagicMock, patch
from src.app_controller import AppController
from src.app_states import AppStates
from src.utility.utils import FileReader, Parameters, Board


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
        controller = AppController()

        algo_cat = "Basic Search"
        algo = "Linear Search"
        controller.basic_search_alg_pressed(algo)

        test_algo_cat = controller.states.curr_algo_cat
        test_algo = controller.states.selected_algo

        self.assertEqual(algo_cat, test_algo_cat)
        self.assertEqual(algo, test_algo)
        
        with patch.object(controller, "reset_btn_pressed") as mock_reset_call:
            controller.basic_search_alg_pressed("Linear Search")
            mock_reset_call.assert_called_once()


    def test_create_values(self):
        controller = AppController()
        
        controller.create_values()
        test_parameters = controller.parameters

        test_values = controller.states.values

        self.assertIsInstance(test_parameters, Parameters)
        self.assertIsInstance(test_values, list)


    def test_create_board(self):
        controller = AppController()
        controller.create_board()

        self.assertIsInstance(controller.board, Board)

    def test_play_button_pressed(self):
        controller = AppController()
        controller.play_btn_pressed()

        self.assertTrue(controller.states.algo_running)
        self.assertTrue(controller.states.obstacle_selected)
        self.assertFalse(controller.states.obstacle_sel_phase)
    
    def test_speed_slider_moved(self):
        controller = AppController()
        controller.speed_slider_moved(20)

        test_value = controller.states.surface_update_intv
        expected_value = 1/20
        
        self.assertEqual(test_value, expected_value)

        controller.speed_slider_moved()
        test_value = controller.states.surface_update_intv
        expected_value = 1/50

        self.assertEqual(test_value, expected_value)

    def test_size_slider_moved(self):
        controller = AppController()
        mock_parameters = MagicMock()
        controller.parameters = mock_parameters

        mock_parameters.create_values.return_value = [1, 2, 3, 4]
        mock_parameters.create_value_to_find.return_value = 3

        with patch.object(controller, "reset_draw_bg_info") as mock_reset, \
            patch.object(controller, "create_generator") as mock_create_generator:

            controller.size_slider_moved(15)

            self.assertEqual(mock_parameters.size, 15)
            self.assertFalse(controller.states.algo_running)

            mock_parameters.create_values.assert_called_once()
            mock_parameters.create_value_to_find.assert_called_once()

            self.assertEqual(controller.states.values, [1, 2, 3, 4])
            self.assertEqual(controller.states.value_to_find, 3)

            mock_reset.assert_called_once()
            mock_create_generator.assert_called_once()


if __name__ == "__main__":
    unittest.main()

