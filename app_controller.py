"""Controls the app logic. Delegates what to do"""

from algorithms import *
from app_states import AppStates
from utils import Parameters

#write the controller class


class AppController:

    def __init__(self):
        self.states = AppStates()

    def basic_search_alg_pressed(self, algorithm):
        parameters = Parameters(20)
        self.values = parameters.create_values()
        self.states.curr_algo_cat = "Basic Search"
        self.states.selected_algo = algorithm
        if self.states.selected_algo == "Linear Search":
            lin_search = LinearSearch(self.values, self.states.value_to_find)
            self.states.algo_generator = lin_search.run()

    def basic_sort_alg_pressed(self, algorithm):
        parameters = Parameters(20)
        self.values = parameters.create_values()
        self.states.curr_algo_cat = "Basic Sort"
        self.states.selected_algo = algorithm

    def pathfinding_alg_pressed(self, algorithm):

        self.states.curr_algo_cat = "Pathfinding"
        self.states.selected_algo = algorithm

    def play_btn_pressed(self):
        self.states.algo_running = True
        pass

    def pause_btn_pressed(self):
        pass

    def reset_btn_pressed(self):
        pass
    
    def set_target_btn_pressed(self):
        pass

    def set_obstacle_btn_pressed(self):
        pass

    def slider_moved(self):
        pass