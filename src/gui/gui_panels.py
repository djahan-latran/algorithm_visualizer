"""This module holds the different sections/panels of the user interface as classes and their methods.
"""
import os, sys
import pygame_gui as pg_gui 
import pygame as pg
from src.gui.gui_elements import Button, ScrollContainer, Slider, Panel, TextWindow
from src.utility.utils import source_path

class MainPanel:
    """ The MainPanel holds the pygame display(screen) and the header of the application
    """
    def __init__(self, fonts, colours, controller):
        """ Initiates the main window
        """
        # Main window
        self.screen_size = (1200, 700)
        self.screen = pg.display.set_mode(self.screen_size)

        # Caption
        pg.display.set_caption("AlgoLab")
        
        # Controller
        self.controller = controller

        # Style attributes
        self.fonts = fonts
        self.colours = colours
        self.header_rect = pg.Rect((0,0), (1200, 50))

        # Locations
        self.settings_loc = (880, 40)
        self.app_name_loc = (60, 40)
        self.algo_name_loc = (200, 40)
        self.icon_loc = (5, 5)

    def render_app_name(self):
        """ renders the application name
        """
        self.app_name = self.fonts.title.render("AlgoLab", True, self.colours.values["text_cl"]) #title
        # Get rectangle and position the surface
        self.app_name_rect = self.app_name.get_rect()
        self.app_name_rect.bottomleft = self.app_name_loc

    def render_selected_algo_name(self):
        """ renders the name of the currently selected algorithm
        """
        self.sel_algo_name = self.fonts.headline.render(f"Selected Algorithm: {self.controller.states.selected_algo}",
                                                        True,
                                                        self.colours.values["text_cl"]
                                                        )
        self.sel_algo_name_rect = self.sel_algo_name.get_rect()
        self.sel_algo_name_rect.bottomleft = self.algo_name_loc

    def render_settings(self):
        """ renders the settings word
        """
        self.settings_text = self.fonts.headline.render("Settings", True, self.colours.values["text_cl"])
        self.settings_text_rect = self.settings_text.get_rect()
        self.settings_text_rect.bottomleft = self.settings_loc
   
    def render_dark_bar(self):
        """ draws the header bar
        """
        pg.draw.rect(self.screen, self.colours.values["header_cl"], self.header_rect)

    def render_icon(self):
        """ Loads and draws the application icon
        """
        
        # Path to the icon bmp
        assets_path = "assets/icon.bmp"
        file_path = source_path(assets_path)

        # Load image and rescale it
        self.icon = pg.image.load(file_path)
        self.icon = pg.transform.scale(self.icon, (45, 40))
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.topleft = self.icon_loc

    def blit_icon(self):
        """ Blit icon to screen
        """
        self.screen.blit(self.icon, self.icon_rect)

    def blit_selected_algo_name(self):
        """ blits currently selected algorithm name onto screen
        """
        self.screen.blit(self.sel_algo_name, self.sel_algo_name_rect)

    def blit_name(self):
        """ blits the application name onto screen
        """
        self.screen.blit(self.app_name, self.app_name_rect)

    def blit_settings(self):
        """ blits settings word onto screen
        """
        self.screen.blit(self.settings_text, self.settings_text_rect)

    def render_init_screen(self):
        """ renders the first main screen of the application when opened
        """
        self.render_icon()
        self.render_app_name()
        self.render_dark_bar()
        self.blit_name()
        self.blit_icon()

    def render_active_screen(self):
        """ renders the main screen format after an algorithmn got selected
        """
        self.render_dark_bar()
        self.render_icon()
        self.render_selected_algo_name()
        self.render_settings()
        self.blit_selected_algo_name()
        self.blit_name()
        self.blit_settings()
        self.blit_icon()
    
    def update(self):
        """ updates the main screen
        """
        if self.controller.states.selected_algo:
            self.render_active_screen()
        else:
            self.render_init_screen()


class MenuPanel:
    """ The MenuPanel holds the scroll panels and button for the different algorithms and categories.
    """

    def __init__(self, manager, controller):
        """ Initiates MenuPanel and set parameters like button size and widths and algorithm categories.
            Delegates the pygame_gui manager and the AppController.
        """
        self.manager = manager
        self.controller = controller

        # Initiate lists to hold the algorithms. This is used to know how long their panel and container should be.
        self.basic_sort_algs = []
        self.basic_search_algs = []
        self.graph_traversal_algs = []
        
        # Button dimensions
        self.btn_width = 180
        self.btn_height = 45

    def create_basic_sort_btns(self):
        """ Creates the buttons for the different basic sort algorithms and adds them to their categorie list.
        """

        # Category button that is not clickable
        self.basic_sorts_btn = Button(pos= (0, self.btn_height * len(self.basic_sort_algs)), 
                                            size= (self.btn_width, self.btn_height), 
                                            label= "Basic Sorting",
                                            manager= self.manager, 
                                            vis= 1, 
                                            id= "#header_button", 
                                            container= self.basic_sorts_scroll_panel.element
                                            )
        self.basic_sort_algs.append(self.basic_sorts_btn)
        self.basic_sorts_btn.element.disable()

        # Create algorithm buttons
        self.bubb_sort_btn = Button(pos= (0, self.btn_height * len(self.basic_sort_algs)), 
                                    size= (self.btn_width, self.btn_height),
                                    label= "Bubble Sort", 
                                    manager= self.manager, 
                                    vis= 1,
                                    container= self.basic_sorts_scroll_panel.element
                                    )
        # Append to category list
        self.basic_sort_algs.append(self.bubb_sort_btn)

        self.sel_sort_btn = Button(pos=(0, self.btn_height * len(self.basic_sort_algs)), 
                                   size= (self.btn_width, self.btn_height), 
                                   label= "Selection Sort", 
                                   manager= self.manager, 
                                   vis= 1, 
                                   container= self.basic_sorts_scroll_panel.element
                                   )
        
        self.basic_sort_algs.append(self.sel_sort_btn)

        self.in_sort_btn = Button(pos= (0, self.btn_height * len(self.basic_sort_algs)), 
                                  size= (self.btn_width, self.btn_height), 
                                  label= "Insertion Sort", 
                                  manager= self.manager, 
                                  vis= 1, 
                                  container= self.basic_sorts_scroll_panel.element
                                  )
        
        self.basic_sort_algs.append(self.in_sort_btn)

        #Make scrollable area actually scrollable and set size to total height of buttons
        self.basic_sorts_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * (len(self.basic_sort_algs))))

    def create_basic_sort_cont(self):
        """Creates the ScrollContainer for basic sort algorithms and the necessary Panel for it.
        """

        # Create basic-sorts scroll container and scroll panel inside
        self.basic_sorts_scroll_cont = ScrollContainer(pos= (0, 50), 
                                                       size=(200, 200), 
                                                       manager= self.manager
                                                       ) # Actual visible size of container
        
        self.basic_sorts_scroll_panel = Panel(pos= (0, 0), 
                                              size= (180, 1200), 
                                              manager= self.manager, 
                                              container= self.basic_sorts_scroll_cont.element
                                              ) # Size of scrollable area

    def create_basic_search_cont(self):
        """Creates the ScrollContainer for basic search algorithms and the necessary Panel for it.
        """
                
        #Create basic search scroll container and scroll panel inside
        self.basic_search_scroll_cont = ScrollContainer(pos= (0, 230), 
                                                        size=(200, 200), 
                                                        manager= self.manager
                                                        )
        
        self.basic_search_scroll_panel = Panel(pos= (0, 0), 
                                               size= (180, 1200), 
                                               manager= self.manager, 
                                               container= self.basic_search_scroll_cont.element
                                               )

    def create_basic_search_btns(self):
        """ Creates the buttons for the different basic search algorithms and adds them to their categorie list.
        """

        # Category button that is not clickable
        self.basic_search_btn = Button(pos=(0, self.btn_height * len(self.basic_search_algs)), 
                                       size=(self.btn_width, self.btn_height), 
                                       label= "Basic Search", 
                                       manager= self.manager, 
                                       vis= 1, 
                                       id= "#header_button", 
                                       container= self.basic_search_scroll_panel.element
                                       )
        self.basic_search_algs.append(self.basic_search_btn)
        # Make it not clickable
        self.basic_search_btn.element.disable()
        
        self.linear_search_btn = Button(pos=(0, self.btn_height * len(self.basic_search_algs)), 
                                        size=(self.btn_width, self.btn_height), 
                                        label= "Linear Search", 
                                        manager= self.manager, 
                                        vis= 1, 
                                        container= self.basic_search_scroll_panel.element
                                        )
        # Add to the list
        self.basic_search_algs.append(self.linear_search_btn)
        
        self.binary_search_btn = Button(pos=(0, self.btn_height * len(self.basic_search_algs)), 
                                        size=(self.btn_width, self.btn_height), 
                                        label= "Binary Search", 
                                        manager= self.manager, 
                                        vis= 1, 
                                        container= self.basic_search_scroll_panel.element
                                        )
        
        self.basic_search_algs.append(self.binary_search_btn)

        # Set dimensions of the scroll area according to total amount of buttons
        self.basic_search_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * (len(self.basic_search_algs))))

    def create_graph_traversal_cont(self):
        """Creates the ScrollContainer for graph traversal algorithms and the necessary Panel for it.
        """
                
        #Create graph traversal scroll container and scroll panel inside
        self.graph_traversal_scroll_cont = ScrollContainer(pos= (0, 365), 
                                                       size=(200, 240), 
                                                       manager= self.manager
                                                       ) #Actual visible size of container
        self.graph_traversal_scroll_panel = Panel(pos= (0, 0), 
                                              size= (180, 1200), 
                                              manager= self.manager, 
                                              container= self.graph_traversal_scroll_cont.element
                                              ) #Size of scrollable area

    def create_graph_traversal_btns(self):
        """ Creates the buttons for the graph traversal algorithms and adds them to their categorie list.
        """

        #Create graph_traversal category
        self.graph_traversal_btn = Button(pos=(0, 0), 
                                      size=(self.btn_width, self.btn_height), 
                                      label= "Graph Search", 
                                      manager= self.manager, 
                                      vis= 1, 
                                      id= "#header_button", 
                                      container= self.graph_traversal_scroll_panel.element
                                      )
        # Add button to list and disable
        self.graph_traversal_algs.append(self.graph_traversal_btn)
        self.graph_traversal_btn.element.disable()

        self.bfs_btn = Button(pos=(0, self.btn_height * len(self.graph_traversal_algs)), 
                              size= (self.btn_width, self.btn_height), 
                              label= "Breadth-First-Search", 
                              manager= self.manager, 
                              vis= 1, 
                              container= self.graph_traversal_scroll_panel.element
                              )
        
        self.graph_traversal_algs.append(self.bfs_btn)

        self.dfs_btn = Button(pos=(0, self.btn_height * len(self.graph_traversal_algs)), 
                              size= (self.btn_width, self.btn_height), 
                              label= "Depth-First-Search", 
                              manager= self.manager, 
                              vis= 1,
                              container= self.graph_traversal_scroll_panel.element
                              )
        
        self.graph_traversal_algs.append(self.dfs_btn)

        self.dijkstra_btn = Button(pos=(0, self.btn_height * len(self.graph_traversal_algs)), 
                              size= (self.btn_width, self.btn_height), 
                              label= "Dijkstra's", 
                              manager= self.manager, 
                              vis= 1,
                              container= self.graph_traversal_scroll_panel.element
                              )
        
        self.graph_traversal_algs.append(self.dijkstra_btn)
        # Set the dimensions
        self.graph_traversal_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * len(self.graph_traversal_algs)))

    def create_menu(self):
        """ Creates the menu panel by calling the different create-methods
        """
        self.create_basic_search_cont()
        self.create_basic_search_btns()

        self.create_basic_sort_cont()
        self.create_basic_sort_btns()

        self.create_graph_traversal_cont()
        self.create_graph_traversal_btns()

    def event_handle(self, event):
        """ Handles the events that can happen by the user pressing a menu button.
            Delegates event to the controller.
        """
        if event.ui_element == self.linear_search_btn.element:
            self.controller.basic_search_alg_pressed("Linear Search")

        elif event.ui_element == self.binary_search_btn.element:
            self.controller.basic_search_alg_pressed("Binary Search")
        
        elif event.ui_element == self.bubb_sort_btn.element:
            self.controller.basic_sort_alg_pressed("Bubble Sort")
        
        elif event.ui_element == self.sel_sort_btn.element:
            self.controller.basic_sort_alg_pressed("Selection Sort")
        
        elif event.ui_element == self.in_sort_btn.element:
            self.controller.basic_sort_alg_pressed("Insertion Sort")

        elif event.ui_element == self.bfs_btn.element:
            self.controller.graph_traversal_alg_pressed("Breadth-First-Search")

        elif event.ui_element == self.dfs_btn.element:
            self.controller.graph_traversal_alg_pressed("Depth-First-Search")

        elif event.ui_element == self.dijkstra_btn.element:
            self.controller.graph_traversal_alg_pressed("Dijkstra")

        else:
            pass  #another algorithm can be added here


class AnimationPanel:
    """ The AnimationPanel is an extra surface that gets drawn onto the main screen.
        It displays each frame of the graphical animations that show how the algorithms work.
    """
    def __init__(self, fonts, colours, screen, controller):
        """ Initiates the AnimationPanel as a surface.
        """
        #Main surface to draw animation surface on
        self.screen = screen

        self.colours = colours
        self.fonts = fonts

        #Controller
        self.controller = controller

        #Animation window position, size and color
        self.pos = (185, 50)
        self.size = (680, 400)
        
        #Background color
        self.background_cl = (82, 82, 82)

        #Colors for different value states (bar graph)
        self.def_bar_cl = (50, 50, 50)
        self.curr_bar_cl = (150, 150, 150)
        self.sortd_bar_cl = (50, 255, 50)
        self.red_bar_cl = (200, 50, 50)

        #Colors for different rectangles (checkerboard)
        self.def_rect_bord_cl = (50, 50, 50)
        self.def_rect_cl = (70, 70, 70)
        self.curr_rect_cl = (120, 120, 120)
        self.obstacle_rect_cl = (200, 50, 50)
        self.target_rect_cl = (50, 255, 50)
        self.blue_rect_cl = (95, 245, 250)
        #Label color
        self.label_color = (250, 250, 250)

        #Distance from bar rect to label
        self.label_pad = 3
        
        #Bevel on corners of the bars
        self.bar_bevel = 2

        self.surface = pg.Surface(self.size)
        self.side_pad = int(self.size[0] / 32)

    def draw_bar_graphs(self, values):
        """ Takes a dictionary and draws the bar graphs. It calculates how wide and high a rectangle should be acoording to the total amount of numbers and their values.
            From the keys in the dictionary, it knows how to color the rectangles.
        """
        # Fill the surface with bg color
        self.surface.fill(self.background_cl)

        # Calc the spacing between bar graphs and their size
        spaces = (len(values) * 2) - 1
        bar_width = (self.size[0] - (self.side_pad * 2)) / spaces

        # Set font size relative to bar_width
        main_font = pg.font.SysFont("Arial", int(bar_width) - self.label_pad, bold=True)

        # Calc bar height and coordinates and draw the rectangles
        for i, value in enumerate(values):
            bar_height = value * 3
            x_coord = i * bar_width * 2 + self.side_pad
            y_coord = self.size[1] - bar_height

            bar_rect = pg.Rect(x_coord, y_coord, int(bar_width), bar_height)

            if self.controller.states.draw_bg_info and value in self.controller.states.draw_bg_info["positive"]:
                pg.draw.rect(self.surface, self.sortd_bar_cl, bar_rect, border_radius= self.bar_bevel)

            elif self.controller.states.draw_bg_info and value in self.controller.states.draw_bg_info["negative"]:
                pg.draw.rect(self.surface, self.red_bar_cl, bar_rect, border_radius= self.bar_bevel)

            elif self.controller.states.draw_bg_info and value in self.controller.states.draw_bg_info["neutral"]:
                pg.draw.rect(self.surface, self.curr_bar_cl, bar_rect, border_radius= self.bar_bevel)

            else:
                pg.draw.rect(self.surface, self.def_bar_cl, bar_rect, border_radius= self.bar_bevel)
            
            # Blit the value on bar graph
            value_label = main_font.render(f"{value}", True, self.label_color)
            value_rect = value_label.get_rect()
            value_rect.midbottom = (x_coord + bar_width/2, y_coord)
            self.surface.blit(value_label, value_rect)
    
    def draw_board(self, board):
        """ Takes a 'board' which is a 2d list and draws it as a grid/checkerboard.
            From the values in the 2d list it knows what color to draw the rectangles.
        """
        
        # Starts topleft
        x_coord = 0
        y_coord = 0

        # Shortest path info is safed here if the algorithm provides it
        path = self.controller.states.draw_pf_info.get("path")
        # The value that is currently processed
        current = self.controller.states.draw_pf_info.get("current")
        # The values that have been visited already
        visited = self.controller.states.draw_pf_info.get("visited")

        # Loop through each row and column of 2d list (board)
        for i in range(board.rows):
            for j in range(board.cols):
                sq_rect = pg.Rect(x_coord, y_coord, board.rect_size, board.rect_size)

                # Draws a red rectangle (obstacle)
                if board.raster[i][j] == -1:
                    pg.draw.rect(self.surface, self.obstacle_rect_cl, sq_rect)

                # Draws a green rectangle (target)
                elif board.raster[i][j] == 2:
                    pg.draw.rect(self.surface, self.target_rect_cl, sq_rect)
                
                # Draws the currently proccessed rectangle with a light blue border
                elif current and (i, j) == current:
                    pg.draw.rect(self.surface, self.blue_rect_cl, sq_rect, 3)
                
                # Draws a light grey rectangle (already visited)
                elif visited and (i, j) in visited:
                    pg.draw.rect(self.surface, self.curr_rect_cl, sq_rect)
                    pg.draw.rect(self.surface, self.def_rect_bord_cl, sq_rect, 1)
                
                # Draws a light blue rectangle (part of shortest path)
                elif path and (i, j) in path:
                    pg.draw.rect(self.surface, self.blue_rect_cl, sq_rect)

                # Draws the default rectangle
                else:
                    pg.draw.rect(self.surface, self.def_rect_cl, sq_rect)
                    pg.draw.rect(self.surface, self.def_rect_bord_cl, sq_rect, 1)

                # Increase X-position
                x_coord += board.rect_size

            # Increase Y-position
            y_coord += board.rect_size
            # Reset X-position for new row
            x_coord = 0 

    def still_frame(self):
        """ Draws the state of the values before the algorithm plays.
            (default board and unsorted values)
        """
        if self.controller.states.selected_algo and not self.controller.states.algo_running:

            # If a graph traversal algorithm is selected then draw the board/grid
            if self.controller.states.curr_algo_cat == "Graph Traversal":
                self.draw_board(self.controller.board)
            else:
                # else draw the bar graph theme
                self.draw_bar_graphs(self.controller.states.values)
    
    def next_animation_frame(self):
        """ Checks if the next frame should be drawn and then calls the suitable draw-method.
        """

        # Checks if controller allows next animation frame
        if self.controller.states.next_animation_frame:
        
            if self.controller.states.curr_algo_cat == "Graph Traversal":
                self.draw_board(self.controller.board) 
            else:
                self.draw_bar_graphs(self.controller.states.values)

            # Tells controller it is done so controller can reset the state and request the model to proceed
            self.controller.next_algorithm_step()
            self.controller.states.next_animation_frame = False

    def blit_target_value(self):
        """ Draws the target value in the top left corner when a basic search algorithm is selected
        """
        # If a basic search algorithm is selected
        if self.controller.states.curr_algo_cat == "Basic Search":
            self.target_value = self.fonts.slider.render(f"Looking for '{self.controller.states.value_to_find}'", 
                                                         True, 
                                                         self.colours.values["accent_cl"]
                                                         )
            # Blit target value
            self.target_value_rect = self.target_value.get_rect()
            self.target_value_rect.topleft = (15, 5)
            self.surface.blit(self.target_value, self.target_value_rect)
    
    def blit_instructions(self):
        """ Draws the instructions in the top left corner when a graph traversal algorithm is selected
        """
        # If a graph traversal algorithm is selected
        if self.controller.states.curr_algo_cat == "Graph Traversal":
            self.instructions = self.fonts.slider.render(f"Click 'Set Target' button and click on the grid to place the target.\nClick 'Set Obstacle' to place as many obstacles on the grid as you like", 
                                                            True, 
                                                            self.colours.values["accent_cl"]
                                                            )
            self.instructions_rect = self.instructions.get_rect()
            self.instructions_rect.topleft = (15, 5)
            self.surface.blit(self.instructions, self.instructions_rect)

    def pf_target_selection(self):
        """ If the 'set target'-button was pressed, selection phase activated, and the user clicked on the board,
            the method passes the x- and y-coordinates of the mouse position on to the controller
        """
        # If clicked on board, get mouse position and pass it to controller
        if  self.controller.states.target_sel_phase and not self.controller.states.algo_running and not self.controller.states.target_selected:
            mouse_pos = pg.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

            if pg.mouse.get_pressed()[0] and self.pos[0] < mouse_x < self.pos[0] + self.size[0] and self.pos[1] < mouse_y < self.pos[1] + self.size[1]:
                surface_x, surface_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
                self.controller.set_target_on_board(surface_x, surface_y)

    def pf_obstacle_selection(self):
        """ If the 'set obstacles'-button was pressed, obstacle selection activated, and the user clicks on the board,
            the method passes the x- and y-coordinates of the mouse position on to the controller.
        """
        # If clicked on board, get mouse position and pass it to controller
        if self.controller.states.obstacle_sel_phase and not self.controller.states.algo_running:
            mouse_pos = pg.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

            if pg.mouse.get_pressed()[0] and self.pos[0] < mouse_x < self.pos[0] + self.size[0] and self.pos[1] < mouse_y < self.pos[1] + self.size[1]:
                surface_x, surface_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
                self.controller.set_obstacle_on_board(surface_x, surface_y)

    def update(self):
        """ Updates the AnimationPanel
        """
        self.still_frame()
        self.next_animation_frame()
        self.blit_target_value()    
        self.blit_instructions()  
        self.pf_target_selection()
        self.pf_obstacle_selection()
    
    def blit_surface(self):
        """ Blits the animation surface onto the screen
        """
        self.screen.blit(self.surface, self.pos)


class CodePanel:
    """ The CodePanel is the the panel on the middle bottom of the screen.
        It shows the actual code of the selected algorithm with additional comments.
    """

    def __init__(self, manager, controller):
        """ Initiates CodePanel
        """
        # Set position and size
        self.pos = (185, 455)
        self.size = (680, 220)

        # Pygame_gui manager and controller
        self.pg_manager = manager
        self.controller = controller

        # The actual panel
        self.code_window = None
        # Currently selected algorithm
        self.current_algo = None

    def update(self):
        """ Updates the CodePanel when a different algoritm got selected.
        """
        # Update if a new algorithm was selected
        if self.controller.states.selected_algo != self.current_algo:
            if self.code_window:
                # Delete previous window
                self.code_window.element.kill()
            self.code_window = TextWindow(self.pos, 
                                          self.size, 
                                          self.pg_manager,
                                          self.controller.states.code_text
                                          ) 
            self.current_algo = self.controller.states.selected_algo


class SettingsPanel:
    """ The SettingsPanel holds all the control buttons that the user can interact with.
    """
    
    def __init__(self, fonts, colours, manager, screen, controller):
        """ Initiates the class and the base attributes for all the buttons.
        """
        self.fonts = fonts
        self.colours = colours
        self.pg_manager = manager
        self.screen = screen
        self.controller = controller

        # Button positions and measurements
        self.play_btn_pos = (910, 280)
        self.play_btn_size = (65, 25)
        self.reset_btn_pos = (1000, 280)
        self.reset_btn_size = (65, 25)
        self.pause_btn_pos = (1090, 280)
        self.pause_btn_size = (65, 25)
        self.target_btn_pos = (910, 120)
        self.target_btn_size = (85, 25)
        self.obstacle_btn_pos = (1055, 120)
        self.obstacle_btn_size = (100, 25)
        self.speed_slider_pos = (910, 200)
        self.speed_slider_size = (245, 25)
        self.size_slider_pos = (910, 130)
        self.size_slider_size = (245, 25)
        self.size_slider_title_pos = (915, 125)
        self.speed_slider_title_pos = (915, 195)

    def _create_gen_control_btns(self):
        """ Creates the generic control buttons.
        """

        #Create play button
        self.play_btn = Button(self.play_btn_pos,
                               self.play_btn_size, 
                               label= "Play", 
                               manager= self.pg_manager, 
                               vis= 0, 
                               id= "#control_button"
                               )
        
        #Create reset button
        self.reset_btn = Button(self.reset_btn_pos, 
                                self.reset_btn_size, 
                                label= "Reset", 
                                manager= self.pg_manager, 
                                vis= 0, 
                                id= "#control_button"
                                )

        #Create pause button
        self.pause_btn = Button(self.pause_btn_pos, 
                                self.pause_btn_size, 
                                label= "Pause", 
                                manager= self.pg_manager, 
                                vis= 0, 
                                id= "#control_button"
                                )
    
    def _create_gt_control_btns(self):
        """ Creates buttons for graph traversal algorithms.
        """

        #Create target button
        self.set_target_btn = Button(self.target_btn_pos, 
                                     self.target_btn_size, 
                                     label= "Set target", 
                                     manager= self.pg_manager, 
                                     vis= 0, 
                                     id= "#control_button"
                                     )
        
        #Create obstacle button
        self.set_obstacle_btn = Button(self.obstacle_btn_pos, 
                                       self.obstacle_btn_size, 
                                       label= "Set Obstacle", 
                                       manager= self.pg_manager, 
                                       vis= 0, 
                                       id= "#control_button"
                                       )

    def _create_control_sliders(self):
        """ Creates the control sliders for size and speed.
        """
        self.size_slider = Slider(self.size_slider_pos, self.size_slider_size, self.pg_manager, (10, 100), 20, 2)
        self.speed_slider = Slider(self.speed_slider_pos, self.speed_slider_size, self.pg_manager, (1, 100), 50, 2)
        # Hide them until graph traversal category is selected
        self.size_slider.element.hide()
        self.speed_slider.element.hide()
    
    def _create_slider_titles(self):
        """ Creates the titles for the sliders.
        """
        
        # Create slider titles
        self.size_slider_title = self.fonts.slider.render("Adjust Size", True, self.colours.values["text_cl"])
        self.size_slider_title_rect = self.size_slider_title.get_rect()
        self.size_slider_title_rect.bottomleft = self.size_slider_title_pos

        self.speed_slider_title = self.fonts.slider.render("Adjust Speed", True, self.colours.values["text_cl"])
        self.speed_slider_title_rect = self.speed_slider_title.get_rect()
        self.speed_slider_title_rect.bottomleft = self.speed_slider_title_pos

    def blit_size_slider_title(self):
        """ Blits size slider title onto screen
        """
        self.screen.blit(self.size_slider_title, self.size_slider_title_rect)

    def blit_speed_slider_title(self):
        """ Blits speed slider title onto screen
        """
        self.screen.blit(self.speed_slider_title, self.speed_slider_title_rect)

    def create_settings(self):
        """ Calls the methods to create all settings.
        """
        self._create_gen_control_btns()
        self._create_gt_control_btns()
        self._create_control_sliders()
        self._create_slider_titles()

    def _show_bg_control_btns(self):
        """ Makes the control-button-set for algorithms visible that are visualized with bar graphs.
        """
        self.play_btn.element.show()
        self.reset_btn.element.show()
        self.pause_btn.element.show()
        self.size_slider.element.show()
        self.size_slider.element.enable()
        self.speed_slider.element.show()
        self.speed_slider.element.enable()
        self.set_target_btn.element.hide()
        self.set_obstacle_btn.element.hide()

    def _show_gt_control_btns(self):
        """ Makes the control-button-set for algorithms visible that are visualized with a grid.
        """
        self.play_btn.element.show()
        self.reset_btn.element.show()
        self.pause_btn.element.show()
        self.size_slider.element.hide()
        self.size_slider.element.disable()
        self.speed_slider.element.show()
        self.speed_slider.element.enable()
        self.set_target_btn.element.show()
        self.set_obstacle_btn.element.show()
    
    def event_handle_btns(self, event):
        """ If the user presses a button the info gets passed to the controller and it reacts accordingly.
        """
        if event.ui_element == self.play_btn.element:
            self.controller.play_btn_pressed()

        elif event.ui_element == self.reset_btn.element:
            self.controller.reset_btn_pressed()

        elif event.ui_element == self.pause_btn.element:
            self.controller.pause_btn_pressed()
        
        elif event.ui_element == self.set_target_btn.element:
            self.set_target_btn.element.select()
            self.controller.set_target_btn_pressed()
        
        elif event.ui_element == self.set_obstacle_btn.element:
            self.set_obstacle_btn.element.select()
            self.controller.set_obstacle_btn_pressed()

    def event_handle_sliders(self, event):
        """ Event hdnling for the sliders. Info gets passed to the controller when sliders are moved.
        """
        if event.ui_element == self.size_slider.element:
            curr_slider_value = self.size_slider.element.get_current_value()
            self.controller.size_slider_moved(curr_slider_value)
        
        elif event.ui_element == self.speed_slider.element:
            curr_slider_value = self.speed_slider.element.get_current_value()
            self.controller.speed_slider_moved(curr_slider_value)

    def update(self):
        """ Updates the SettingsPanel.
        """
        if self.controller.states.selected_algo:
            # Checks what the currently active category is
            if self.controller.states.curr_algo_cat == "Graph Traversal":
                self._show_gt_control_btns()
                self.blit_speed_slider_title()
 
            else:
                self._show_bg_control_btns()
                self.blit_size_slider_title()
                self.blit_speed_slider_title()

            # Checks for obstacle selection phase
            if self.controller.states.obstacle_sel_phase == False:
                self.set_obstacle_btn.element.unselect()

            # Checks for target selection phase
            if self.controller.states.target_sel_phase == False:
                self.set_target_btn.element.unselect()

        # Reset slider positions and values to default if 'parameter_reset' is True
        if self.controller.states.parameter_reset:
            self.size_slider.element.set_current_value(20)
            self.speed_slider.element.set_current_value(50)
            
            # Set it to False
            self.controller.set_parameter_reset()


class InfoPanel:
    """ Creates the InfoPanel on the bottom right of the window.
        It shows general information about the currently selected algorithm as text.
    """
    def __init__(self, fonts, colours, manager, controller):
        """ Initiates the InfoPanel with basic attributes.
        """
        self.fonts = fonts
        self.colours = colours 
        self.controller = controller
        self.manager = manager

        self.info_window = None
        self.current_algo = None
 
        # Info icon parameters
        self.info_circle_dim = 45
        self.anchor_x = 1035
        self.anchor_y = 360

        # Info box parameters
        self.box_pos = (868, 360)
        self.box_size = (334, 340)
        self.line_pos_start = (870,360)
        self.line_pos_end = (1200,360)
    
    def create_header(self):
        """ Creates the header of the InfoPanel.
        """
        # Create info icon
        self.info_circle_rect = pg.Rect((self.anchor_x - self.info_circle_dim / 2, self.anchor_y - self.info_circle_dim / 2), 
                                        (self.info_circle_dim, self.info_circle_dim)
                                        )
    
        self.letter_i = self.fonts.info_icon.render("i", True, self.colours.values["text_cl"])
        self.letter_i_rect = self.letter_i.get_rect()
        # Position it
        self.letter_i_rect.center = (self.anchor_x - 1, self.anchor_y - 1) #make variables then subtract 1

    def draw_header(self, screen):
        """ Blits the header onto the surface.
        """
        if self.controller.states.selected_algo:
            pg.draw.line(screen, self.colours.values["accent_cl"], self.line_pos_start, self.line_pos_end, 5)
            pg.draw.ellipse(screen, self.colours.values["accent_cl"], self.info_circle_rect)
            screen.blit(self.letter_i, self.letter_i_rect)
                                             
    def update(self):
        """ Updates the InfoPanel when a new algorithm is selected.
        """
        # Checks if a new algorithm got selected
        if self.controller.states.selected_algo != self.current_algo:
            if self.info_window:
                self.info_window.element.kill()
            self.info_window = TextWindow(self.box_pos, 
                                          self.box_size, 
                                          self.manager,
                                          self.controller.states.info_text
                                          )
            self.current_algo = self.controller.states.selected_algo

   