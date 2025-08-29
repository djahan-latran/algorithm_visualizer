"""Controls the app logic. Delegates what to do"""

import os
from algorithms import *
from app_states import AppStates
from utility.utils import Parameters, Board, FileReader


class AppController:
    """
    Is responsible for the logic of the application.
    Coordinates between Model and View.
    """

    def __init__(self):
        """
        Initiates the controller and its base attributes.

        Attributes
        ----------

        states : class instance
            initiates an AppStates instance.
        
        file_reader_text : class instance
            initiates a FileReader for the info texts.
        
        file_reader_code : class instance
            initiatesa FileReader for the code texts.
        
        """
        self.states = AppStates()
        file_directory = os.path.dirname(os.path.abspath(__file__)) 
        
        try:
            self.file_reader_text = FileReader(file_directory, 
                                            "info_texts.yaml"
                                            )
            self.file_reader_code = FileReader(file_directory,
                                            "code_texts.yaml"
                                            )
        except FileNotFoundError as e:
            print(f"File could not be found: {e}")

            #Default values in case of FileNotFoundError
            self.file_reader_text = None
            self.file_reader_code = None

        self.board = None
        self.parameters = None
    
    def set_current_time(self, current_time):
        """
        Saves the starting time.
        """
        self.states.surface_upated = current_time
        self.states.gui_updated = current_time

    def check_gui_update(self, current_time):
        """
        Checks if gui should update based on the update interval.
        """
        if current_time - self.states.gui_updated >= self.states.gui_update_intv:
            self.states.gui_updated = current_time
            return True
        return False

    def check_surface_update(self, current_time):
        """
        Checks if animation surface should update based on the update interval.
        """
        if self.states.algo_running and current_time - self.states.surface_updated >= self.states.surface_update_intv:
            self.states.surface_updated = current_time
            return True
        return False

    def basic_search_alg_pressed(self, algorithm):
        """
        If the user selects a basic search algorithm, 
        methods to reset states and to create a new generator are called.
        Sets the current algorithm category and the selected algorithm accordingly.
        """
        self.states.curr_algo_cat = "Basic Search"
        self.states.selected_algo = algorithm

        self.reset_btn_pressed()

    def basic_sort_alg_pressed(self, algorithm):
        """
        If the user selects a basic sort algorithm, 
        methods to reset states and to create a new generator are called.
        Sets the current algorithm category and the selected algorithm accordingly.
        """
        self.states.curr_algo_cat = "Basic Sort"
        self.states.selected_algo = algorithm
        
        self.reset_btn_pressed()

    def graph_traversal_alg_pressed(self, algorithm):
        """
        If the user selects a graph traversal algorithm, 
        methods to reset states and to create a new generator are called.
        Sets the current algorithm category and the selected algorithm accordingly.
        """
                
        #if not board then create one OR reset target_selected to False
        if not self.board:
            self.create_board()

        self.states.curr_algo_cat = "Graph Traversal"
        self.states.selected_algo = algorithm

        self.reset_btn_pressed()

    def create_values(self):
        """
        Creates new Parameters instance and new values.
        """
        self.parameters = Parameters(20)
        self.states.values = self.parameters.create_values()

    def create_value_to_find(self):
        """
        Creates new target value.
        """
        self.states.value_to_find = self.parameters.create_value_to_find()

    def create_board(self):
        """
        Creates a new Board instance (grid)
        """
        self.board = Board(self.states.anim_surf_size, self.states.board_rect_amount)

    def play_btn_pressed(self):
        """
        Responds to play button pressed.
        """
        self.states.algo_running = True
        self.states.obstacle_sel_phase = False
        self.states.obstacle_selected = True

    def pause_btn_pressed(self):
        """
        Responds to paue button pressed.
        """
        self.states.algo_running = False

    def reset_btn_pressed(self):
        """
        Responds to reset button pressed.
        """
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
        """
        Responds to set-target-button pressed.
        """
        if not self.states.target_selected:
            self.states.obstacle_sel_phase = False
            self.states.target_sel_phase = True

    def set_obstacle_btn_pressed(self):
        """
        Responds to set-obstacle-button pressed.
        """
        if not self.states.obstacle_selected:
            self.states.obstacle_sel_phase = True

    def size_slider_moved(self, slider_value):
        """
        Responds to size-slider moved.
        """
        self.states.algo_running = False

        self.parameters.size = slider_value
        self.states.values = self.parameters.create_values()
        self.states.value_to_find = self.parameters.create_value_to_find()

        self.reset_draw_bg_info()
        self.create_generator()

    def speed_slider_moved(self, slider_value= None):
        """
        Responds to speed-slider moved.
        """
        if slider_value:
            self.states.surface_update_intv = 1 / slider_value
        else:
            self.states.surface_update_intv = 1/50

    def set_parameter_reset(self):
        """
        Flag to track if parameters have to be reset.
        """
        if self.states.parameter_reset:
            self.states.parameter_reset = False
        else:
            self.states.parameter_reset = True

    def next_algorithm_step(self):
        """
        Allows the generator to proceed to next step.
        """
        try:
            next(self.states.algo_generator)
        except StopIteration:
            self.states.algo_running = False

    def next_animation_step(self):
        """
        Switches Flag to True so the gui knows if next animation frame should be rendered.
        """
        self.states.next_animation_frame = True
    
    def reset_draw_bg_info(self):
        """
        Resets the value info dictionary
        """
        self.states.draw_bg_info = {"positive": [], "neutral": [], "negative": []}
    
    def reset_draw_pf_info(self):
        """
        Resets the value info dictionary for graph traversal algorithms
        """
        self.states.draw_pf_info = {"current": None, "visited": None}
    
    def create_generator(self):  
        """
        Creates the generator of the run() method in the currently selected algorithm class.
        Also calls the get_text_from_file() method to load the right texts.
        """

        # Checks the current category
        if self.states.curr_algo_cat == "Basic Search":

            # Checks what algorithm in that category is selected
            if self.states.selected_algo == "Linear Search":
                self.get_text_from_file()
                try:
                    lin_search = LinearSearch(self.states.values, self.states.value_to_find, self.states.draw_bg_info)

                    try:
                        self.states.algo_generator = lin_search.run()
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")

                except TypeError as e:
                    print(f"Error with the input data: {e}")

            elif self.states.selected_algo == "Binary Search":
                self.get_text_from_file()
                self.states.values.sort()
                try:
                    bin_search = BinarySearch(self.states.values, self.states.value_to_find, self.states.draw_bg_info)

                    try:
                        self.states.algo_generator = bin_search.run(self.states.values)
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")

                except TypeError as e:
                    print(f"Error with the input data: {e}")

        elif self.states.curr_algo_cat == "Basic Sort":

            if self.states.selected_algo == "Bubble Sort":
                self.get_text_from_file()
                try:
                    bubb_sort = BubbleSort(self.states.values, self.states.draw_bg_info)

                    try:
                        self.states.algo_generator = bubb_sort.run()
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")

                except TypeError as e:
                    print(f"Error with the input data: {e}")

            elif self.states.selected_algo == "Selection Sort":
                self.get_text_from_file()
                try:
                    sel_sort = SelectionSort(self.states.values, self.states.draw_bg_info)
                    
                    try:
                        self.states.algo_generator = sel_sort.run()
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")
                        
                except TypeError as e:
                    print(f"Error with the input data: {e}")  

            elif self.states.selected_algo == "Insertion Sort":
                self.get_text_from_file()
                try:
                    insert_sort = InsertionSort(self.states.values, self.states.draw_bg_info)

                    try:
                        self.states.algo_generator = insert_sort.run()
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")

                except TypeError as e:
                    print(f"Error with the input data: {e}")
        
        elif self.states.curr_algo_cat == "Graph Traversal":

            if self.states.selected_algo == "Breadth-First-Search":
                self.get_text_from_file()
                try:
                    bf_search = Bfs(self.states.draw_pf_info)

                    try:
                        self.states.algo_generator = bf_search.run(self.board)
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")

                except TypeError as e:
                    print(f"Error with the input data: {e}")

            elif self.states.selected_algo == "Depth-First-Search":
                self.get_text_from_file()
                try:
                    df_search = Dfs(self.states.draw_pf_info)

                    try:
                        self.states.algo_generator = df_search.run(0, 0, self.board)
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")

                except TypeError as e:
                    print(f"Error with the input data: {e}")
            
            elif self.states.selected_algo == "Dijkstra":
                self.get_text_from_file()
                try:
                    dijkstra_search = Dijkstras(self.states.draw_pf_info)

                    try:
                        self.states.algo_generator = dijkstra_search.run(self.board)
                    except KeyError as e:
                        print(f"Error in algorithm: {e}")

                except TypeError as e:
                    print(f"Error with the input data: {e}")
    
    def set_target_on_board(self, x, y):
        """
        Calculates where on the grid the target got placed by the mouse position coordinates.
        Sets target_selected to True and target_sel_phase to False.
        Sets the value on the grid to '2'.

        Parameters
        ----------
        x : float
            x-position of mouse click on canvas
        y : float
            y-position of mouse click on canvas
        """
        rect_no_x = x // self.board.rect_size
        rect_no_y = y // self.board.rect_size
        self.board.raster[rect_no_y][rect_no_x] = 2
        self.states.target_loc = (rect_no_y, rect_no_x)
        self.states.target_selected = True
        self.states.target_sel_phase = False
    
    def set_obstacle_on_board(self, x, y):
        """
        Calculates where on the grid an obstacle got placed by the mouse position coordinates.
        Sets the value on the grid to '-1'.

        Parameters
        ----------
        x : float
            x-position of mouse click on canvas
        y : float
            y-position of mouse click on canvas
        """
        rect_no_x = x // self.board.rect_size
        rect_no_y = y // self.board.rect_size
        self.board.raster[rect_no_y][rect_no_x] = -1

    def get_text_from_file(self):
        """
        Calls the FileReader instances to load and get the text for the currently selected algorithm.
        """
        self.states.info_text = self.file_reader_text.get_text(self.states.selected_algo)
        self.states.code_text = self.file_reader_code.get_code_text(self.states.selected_algo)

