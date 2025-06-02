"""Controls the app logic. Delegates what to do"""

import os
from algorithms import *
from app_states import AppStates
from utility.utils import Parameters, Board, FileReader


class AppController:

    def __init__(self):
        self.states = AppStates()
        file_directory = os.path.dirname(os.path.abspath(__file__)) 
        self.file_reader_text = FileReader(file_directory, 
                                           "info_texts.yaml"
                                           )
        self.file_reader_code = FileReader(file_directory,
                                           "code_texts.yaml"
                                           )
        self.board = None
        self.parameters = None
    
    def set_current_time(self, current_time):
        self.states.surface_upated = current_time
        self.states.gui_updated = current_time

    def check_gui_update(self, current_time):
        if current_time - self.states.gui_updated >= self.states.gui_update_intv:
            self.states.gui_updated = current_time
            return True
        return False

    def check_surface_update(self, current_time):
        if self.states.algo_running and current_time - self.states.surface_updated >= self.states.surface_update_intv:
            self.states.surface_updated = current_time
            return True
        return False

    def basic_search_alg_pressed(self, algorithm):
        self.states.curr_algo_cat = "Basic Search"
        self.states.selected_algo = algorithm

        self.reset_btn_pressed()

        self.create_generator()

    def basic_sort_alg_pressed(self, algorithm):
        self.states.curr_algo_cat = "Basic Sort"
        self.states.selected_algo = algorithm
        
        self.reset_btn_pressed()

        self.create_generator()

    def grah_traversal_alg_pressed(self, algorithm):
        #if not board then create one OR reset target_selected to False
        if not self.board:
            self.create_board()

        self.states.curr_algo_cat = "Graph Traversal"
        self.states.selected_algo = algorithm

        self.reset_btn_pressed()

        self.create_generator()

    def create_values(self):
        self.parameters = Parameters(20)
        self.states.values = self.parameters.create_values()

    def create_value_to_find(self):
        self.states.value_to_find = self.parameters.create_value_to_find()

    def create_board(self):
        self.board = Board(self.states.anim_surf_size, self.states.board_rect_amount)

    def play_btn_pressed(self):
        self.states.algo_running = True
        self.states.obstacle_sel_phase = False
        self.states.obstacle_selected = True

    def pause_btn_pressed(self):
        self.states.algo_running = False

    def reset_btn_pressed(self):
        self.states.algo_running = False
        self.states.target_selected = False
        self.states.obstacle_selected = False
        self.states.obstacle_sel_phase = False
        self.states.target_sel_phase = False
        if self.board:
            self.board.reset()
        self.reset_draw_pf_info()
        self.reset_draw_bg_info()
        self.create_values()
        self.create_value_to_find()
        self.set_parameter_reset()
        self.speed_slider_moved()
        self.create_generator()
    
    def set_target_btn_pressed(self):
        if not self.states.target_selected:
            self.states.obstacle_sel_phase = False
            self.states.target_sel_phase = True

    def set_obstacle_btn_pressed(self):
        if not self.states.obstacle_selected:
            self.states.obstacle_sel_phase = True

    def size_slider_moved(self, slider_value):
        self.states.algo_running = False

        self.parameters.size = slider_value
        self.states.values = self.parameters.create_values()
        self.states.value_to_find = self.parameters.create_value_to_find()

        self.reset_draw_bg_info()
        self.create_generator()

    def speed_slider_moved(self, slider_value= None):
        if slider_value:
            self.states.surface_update_intv = 1 / slider_value
        else:
            self.states.surface_update_intv = 1/50

    def set_parameter_reset(self):
        if self.states.parameter_reset:
            self.states.parameter_reset = False
        else:
            self.states.parameter_reset = True

    def next_algorithm_step(self):
        try:
            next(self.states.algo_generator)
        except StopIteration:
            self.states.algo_running = False

    def next_animation_step(self):
        self.states.next_animation_frame = True
    
    def reset_draw_bg_info(self):
        self.states.draw_bg_info = {"positive": [], "neutral": [], "negative": []}
    
    def reset_draw_pf_info(self):
        self.states.draw_pf_info = {"current": None, "visited": None}
    
    def create_generator(self):  
        if self.states.curr_algo_cat == "Basic Search":

            if self.states.selected_algo == "Linear Search":
                self.get_text_from_file()
                lin_search = LinearSearch(self.states.values, self.states.value_to_find, self.states.draw_bg_info)
                self.states.algo_generator = lin_search.run()

            elif self.states.selected_algo == "Binary Search":
                self.get_text_from_file()
                self.states.values.sort()
                bin_search = BinarySearch(self.states.values, self.states.value_to_find, self.states.draw_bg_info)
                self.states.algo_generator = bin_search.run(self.states.values)

        elif self.states.curr_algo_cat == "Basic Sort":

            if self.states.selected_algo == "Bubble Sort":
                self.get_text_from_file()
                bubb_sort = BubbleSort(self.states.values, self.states.draw_bg_info)
                self.states.algo_generator = bubb_sort.run()

            elif self.states.selected_algo == "Selection Sort":
                self.get_text_from_file()
                sel_sort = SelectionSort(self.states.values, self.states.draw_bg_info)
                self.states.algo_generator = sel_sort.run()
            
            elif self.states.selected_algo == "Insertion Sort":
                self.get_text_from_file()
                insert_sort = InsertionSort(self.states.values, self.states.draw_bg_info)
                self.states.algo_generator = insert_sort.run()
        
        elif self.states.curr_algo_cat == "Graph Traversal":

            if self.states.selected_algo == "Breadth-First-Search":
                self.get_text_from_file()
                bf_search = Bfs(self.states.draw_pf_info)
                self.states.algo_generator = bf_search.run(self.board)

            elif self.states.selected_algo == "Depth-First-Search":
                self.get_text_from_file()
                df_search = Dfs(self.states.draw_pf_info)
                self.states.algo_generator = df_search.run(0, 0, self.board)
            
            elif self.states.selected_algo == "Dijkstra":
                self.get_text_from_file()
                dijkstra_search = Dijkstras(self.states.draw_pf_info)
                self.states.algo_generator = dijkstra_search.run(self.board)
    
    def set_target_on_board(self, x, y):
        rect_no_x = x // self.board.rect_size
        rect_no_y = y // self.board.rect_size
        self.board.raster[rect_no_y][rect_no_x] = 2
        self.states.target_loc = (rect_no_y, rect_no_x)
        self.states.target_selected = True
        self.states.target_sel_phase = False
    
    def set_obstacle_on_board(self, x, y):
        rect_no_x = x // self.board.rect_size
        rect_no_y = y // self.board.rect_size
        self.board.raster[rect_no_y][rect_no_x] = -1

    def get_text_from_file(self):
        self.states.info_text = self.file_reader_text.get_text(self.states.selected_algo)
        self.states.code_text = self.file_reader_code.get_code_text(self.states.selected_algo)

