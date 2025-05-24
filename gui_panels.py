"""The different sections/panels of the user interface"""
import pygame_gui as pg_gui 
import pygame as pg
from gui_elements import Button, ScrollContainer, Slider, Panel, TextWindow


class MainPanel:

    def __init__(self, fonts, colours, controller):
        #Main window
        self.screen_size = (1200, 700)
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("AlgoLab")
        
        #Controller
        self.controller = controller

        #Style attributes
        self.fonts = fonts
        self.colours = colours
        self.header_rect = pg.Rect((0,0), (1200, 50))

        #Locations
        self.settings_loc = (880, 40)
        self.app_name_loc = (40, 40)
        self.algo_name_loc = (200, 40)

    def render_app_name(self):
        #Render application name
        self.app_name = self.fonts.title.render("AlgoLab", True, self.colours.values["text_cl"]) #title
        self.app_name_rect = self.app_name.get_rect()
        self.app_name_rect.bottomleft = self.app_name_loc

    def render_selected_algo_name(self):
        self.sel_algo_name = self.fonts.headline.render(f"Selected Algorithm: {self.controller.states.selected_algo}",
                                                        True,
                                                        self.colours.values["text_cl"]
                                                        )
        self.sel_algo_name_rect = self.sel_algo_name.get_rect()
        self.sel_algo_name_rect.bottomleft = self.algo_name_loc

    def render_settings(self):
        #Render settings
        self.settings_text = self.fonts.headline.render("Settings", True, self.colours.values["text_cl"])
        self.settings_text_rect = self.settings_text.get_rect()
        self.settings_text_rect.bottomleft = self.settings_loc
   
    def render_dark_bar(self):
        pg.draw.rect(self.screen, self.colours.values["header_cl"], self.header_rect)

    def blit_selected_algo_name(self):
        self.screen.blit(self.sel_algo_name, self.sel_algo_name_rect)

    def blit_name(self):
        self.screen.blit(self.app_name, self.app_name_rect)

    def blit_settings(self):
        self.screen.blit(self.settings_text, self.settings_text_rect)

    def render_init_screen(self):
        self.render_app_name()
        self.render_dark_bar()
        self.blit_name()

    def render_active_screen(self):
        self.render_dark_bar()
        self.render_selected_algo_name()
        self.render_settings()
        self.blit_selected_algo_name()
        self.blit_name()
        self.blit_settings()
    
    def update(self):
        if self.controller.states.selected_algo:
            self.render_active_screen()
        else:
            self.render_init_screen()


class MenuPanel:

    def __init__(self, manager, controller):
        self.manager = manager
        self.controller = controller

        self.basic_sort_algs = []
        self.basic_search_algs = []
        self.pathfinding_algs = []
        self.btn_width = 180
        self.btn_height = 45

    def create_basic_sort_btns(self):
        #Category button that is not clickable
        self.basic_sorts_btn = Button(pos= (0, 0), 
                                            size= (self.btn_width, self.btn_height), 
                                            label= "Basic Sorting",
                                            manager= self.manager, 
                                            vis= 1, 
                                            id= "#header_button", 
                                            container= self.basic_sorts_scroll_panel.element
                                            )
        
        #self.basic_sort_algs.append(self.basic_sorts_btn)
        self.basic_sorts_btn.element.disable()

        #Create algorithm buttons
        self.bubb_sort_btn = Button(pos= (0, self.btn_height), 
                                    size= (self.btn_width, self.btn_height),
                                    label= "Bubble Sort", 
                                    manager= self.manager, 
                                    vis= 1,
                                    container= self.basic_sorts_scroll_panel.element
                                    )
        
        self.basic_sort_algs.append(self.bubb_sort_btn)

        self.sel_sort_btn = Button(pos=(0, self.btn_height * 2), 
                                   size= (self.btn_width, self.btn_height), 
                                   label= "Selection Sort", 
                                   manager= self.manager, 
                                   vis= 1, 
                                   container= self.basic_sorts_scroll_panel.element
                                   )
        
        self.basic_sort_algs.append(self.sel_sort_btn)

        self.in_sort_btn = Button(pos= (0, self.btn_height * 3), 
                                  size= (self.btn_width, self.btn_height), 
                                  label= "Insertion Sort", 
                                  manager= self.manager, 
                                  vis= 1, 
                                  container= self.basic_sorts_scroll_panel.element
                                  )
        
        self.basic_sort_algs.append(self.in_sort_btn)

        #Make scrollable area actually scrollable and set size to total height of buttons
        self.basic_sorts_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * (len(self.basic_sort_algs) + 1)))

    def create_basic_sort_cont(self):
        #Create basic-sorts scroll container and scroll panel inside
        self.basic_sorts_scroll_cont = ScrollContainer(pos= (0, 50), 
                                                       size=(200, 200), 
                                                       manager= self.manager
                                                       ) #Actual visible size of container
        
        self.basic_sorts_scroll_panel = Panel(pos= (0, 0), 
                                              size= (180, 1200), 
                                              manager= self.manager, 
                                              container= self.basic_sorts_scroll_cont.element
                                              ) #Size of scrollable area

    def create_basic_search_cont(self):
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
        #Category button that is not clickable
        self.basic_search_btn = Button(pos=(0, 0), 
                                       size=(self.btn_width, self.btn_height), 
                                       label= "Basic Search", 
                                       manager= self.manager, 
                                       vis= 1, 
                                       id= "#header_button", 
                                       container= self.basic_search_scroll_panel.element
                                       )
        
        #self.basic_search_algs.append(self.basic_search_btn)
        self.basic_search_btn.element.disable()
        
        self.linear_search_btn = Button(pos=(0, 45), 
                                        size=(self.btn_width, self.btn_height), 
                                        label= "Linear Search", 
                                        manager= self.manager, 
                                        vis= 1, 
                                        container= self.basic_search_scroll_panel.element
                                        )
        
        self.basic_search_algs.append(self.linear_search_btn)
        
        self.binary_search_btn = Button(pos=(0, 90), 
                                        size=(self.btn_width, self.btn_height), 
                                        label= "Binary Search", 
                                        manager= self.manager, 
                                        vis= 1, 
                                        container= self.basic_search_scroll_panel.element
                                        )
        
        self.basic_search_algs.append(self.binary_search_btn)

        self.basic_search_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * (len(self.basic_search_algs) + 1)))

    def create_pathfinding_cont(self):
        #Create pathfinding scroll container and scroll panel inside
        self.pathfinding_scroll_cont = ScrollContainer(pos= (0, 365), 
                                                       size=(200, 240), 
                                                       manager= self.manager
                                                       ) #Actual visible size of container
        self.pathfinding_scroll_panel = Panel(pos= (0, 0), 
                                              size= (180, 1200), 
                                              manager= self.manager, 
                                              container= self.pathfinding_scroll_cont.element
                                              ) #Size of scrollable area

    def create_pathfinding_btns(self):
        #Create pathfinding category
        self.pathfinding_btn = Button(pos=(0, 0), 
                                      size=(self.btn_width, self.btn_height), 
                                      label= "Tree Search", 
                                      manager= self.manager, 
                                      vis= 1, 
                                      id= "#header_button", 
                                      container= self.pathfinding_scroll_panel.element
                                      )
        
        self.pathfinding_algs.append(self.pathfinding_btn)
        self.pathfinding_btn.element.disable()

        self.bfs_btn = Button(pos=(0, self.btn_height), 
                              size= (self.btn_width, self.btn_height), 
                              label= "Breadth-First-Search", 
                              manager= self.manager, 
                              vis= 1, 
                              container= self.pathfinding_scroll_panel.element
                              )
        
        self.pathfinding_algs.append(self.bfs_btn)

        self.dfs_btn = Button(pos=(0, self.btn_height * 2), 
                              size= (self.btn_width, self.btn_height), 
                              label= "Depth-First-Search", 
                              manager= self.manager, 
                              vis= 1,
                              container= self.pathfinding_scroll_panel.element
                              )
        
        self.pathfinding_algs.append(self.dfs_btn)

        self.pathfinding_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * len(self.pathfinding_algs)))

    def create_menu(self):
        self.create_basic_search_cont()
        self.create_basic_search_btns()

        self.create_basic_sort_cont()
        self.create_basic_sort_btns()

        self.create_pathfinding_cont()
        self.create_pathfinding_btns()

    def event_handle(self, event):
        #write method that delegates to controller
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
            self.controller.pathfinding_alg_pressed("Breadth-First-Search")

        elif event.ui_element == self.dfs_btn.element:
            self.controller.pathfinding_alg_pressed("Depth-First-Search")

        else:
            pass  #another algorithm can be added here


class AnimationPanel:

    def __init__(self, fonts, colours, screen, controller):
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

        #Distance from surface sides
        self.side_pad = 0
        
        #Bevel on corners of the bars
        self.bar_bevel = 2

        self.surface = pg.Surface(self.size)
        self.side_pad = int(self.size[0] / 32)

    def draw_bar_graphs(self, values):
        #fill the surface with bg color
        self.surface.fill(self.background_cl)

        #draw_title(algorithm= algo_name, screen= screen)

        #calc the spacing between bar graphs and their size
        spaces = (len(values) * 2) - 1
        bar_width = int((self.size[0] - (self.side_pad * 2)) / spaces) 

        #set font size relative to bar_width
        main_font = pg.font.SysFont("Arial", bar_width - self.label_pad, bold=True)

        #calc bar height and coordinates and draw the rectangles
        for i, value in enumerate(values):
            bar_height = value * 3
            x_coord = i * bar_width * 2 + self.side_pad
            y_coord = self.size[1] - bar_height

            bar_rect = pg.Rect(x_coord, y_coord, bar_width, bar_height)

            if self.controller.states.draw_bg_info and value in self.controller.states.draw_bg_info["positive"]:
                pg.draw.rect(self.surface, self.sortd_bar_cl, bar_rect, border_radius= self.bar_bevel)

            elif self.controller.states.draw_bg_info and value in self.controller.states.draw_bg_info["negative"]:
                pg.draw.rect(self.surface, self.red_bar_cl, bar_rect, border_radius= self.bar_bevel)

            elif self.controller.states.draw_bg_info and value in self.controller.states.draw_bg_info["neutral"]:
                pg.draw.rect(self.surface, self.curr_bar_cl, bar_rect, border_radius= self.bar_bevel)

            else:
                pg.draw.rect(self.surface, self.def_bar_cl, bar_rect, border_radius= self.bar_bevel)
            
            #blit the value on bar graph
            value_label = main_font.render(f"{value}", True, self.label_color)
            value_rect = value_label.get_rect()
            value_rect.midbottom = (x_coord + bar_width/2, y_coord)
            self.surface.blit(value_label, value_rect)
    
    def draw_board(self, board):
        #Draw the checkerboard
        
        x_coord = 0
        y_coord = 0

        end_pos = (len(board.raster), len(board.raster[1]))

        for i in range(board.rows):
            for j in range(board.cols):
                sq_rect = pg.Rect(x_coord, y_coord, board.rect_size, board.rect_size)

                if board.raster[i][j] == 1:
                    pg.draw.rect(self.surface, self.obstacle_rect_cl, sq_rect)
                    
                elif board.raster[i][j] == 2:
                    pg.draw.rect(self.surface, self.target_rect_cl, sq_rect)

                elif end_pos and (i, j) == end_pos:  #check if this is still necessary
                    pg.draw.rect(self.surface, self.target_rect_cl, sq_rect)
                    
                elif self.controller.states.draw_pf_info["current"] and (i, j) == self.controller.states.draw_pf_info["current"]:
                    pg.draw.rect(self.surface, self.blue_rect_cl, sq_rect, 3)
                    
                elif self.controller.states.draw_pf_info["visited"] and (i, j) in self.controller.states.draw_pf_info["visited"]:
                    pg.draw.rect(self.surface, self.curr_rect_cl, sq_rect)
                    pg.draw.rect(self.surface, self.def_rect_bord_cl, sq_rect, 1)
                    
                else:
                    pg.draw.rect(self.surface, self.def_rect_cl, sq_rect)
                    pg.draw.rect(self.surface, self.def_rect_bord_cl, sq_rect, 1)
                    

                x_coord += board.rect_size

            y_coord += board.rect_size
            x_coord = 0 

    def still_frame(self):
        if self.controller.states.selected_algo and not self.controller.states.algo_running:
            
            if not self.controller.states.anim_surf_size:
                self.controller.states.anim_surf_size = self.size

            if self.controller.states.curr_algo_cat == "Pathfinding":
                self.draw_board(self.controller.board)
            else:
                self.draw_bar_graphs(self.controller.states.values)
    
    def update(self):
        self.still_frame()
                
        if self.controller.states.curr_algo_cat == "Basic Search":
            self.target_value = self.fonts.slider.render(f"Looking for '{self.controller.states.value_to_find}'", 
                                                         True, 
                                                         self.colours.values["accent_cl"]
                                                         )
            self.target_value_rect = self.target_value.get_rect()
            self.target_value_rect.topleft = (15, 5)
            self.surface.blit(self.target_value, self.target_value_rect)

        if self.controller.states.next_animation_frame:
            
            if self.controller.states.curr_algo_cat == "Pathfinding":
                self.draw_board(self.controller.board) 
            else:
                self.draw_bar_graphs(self.controller.states.values)
            
            self.controller.next_algorithm_step()
            self.controller.states.next_animation_frame = False

        if  self.controller.states.target_sel_phase and not self.controller.states.algo_running and not self.controller.states.target_selected:
            mouse_pos = pg.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

            if pg.mouse.get_pressed()[0] and self.pos[0] < mouse_x < self.pos[0] + self.size[0] and self.pos[1] < mouse_y < self.pos[1] + self.size[1]:
                surface_x, surface_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
                self.controller.set_target_on_board(surface_x, surface_y)

        if self.controller.states.obstacle_sel_phase and not self.controller.states.algo_running:
            mouse_pos = pg.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

            if pg.mouse.get_pressed()[0] and self.pos[0] < mouse_x < self.pos[0] + self.size[0] and self.pos[1] < mouse_y < self.pos[1] + self.size[1]:
                surface_x, surface_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
                self.controller.set_obstacle_on_board(surface_x, surface_y)
    
    def blit_surface(self):
        self.screen.blit(self.surface, self.pos)

class CodePanel:

    def __init__(self, manager, controller):
        self.pos = (185, 455)
        self.size = (680, 220)

        self.pg_manager = manager
        self.controller = controller

        self.code_window = None
        self.current_algo = None

    def create_window(self):
        if self.controller.states.selected_algo and not self.code_window:
            self.code_window = TextWindow(self.pos, 
                                            self.size, 
                                            self.pg_manager,
                                            self.controller.states.code_text
                                         )

    def update(self):
        if self.controller.states.selected_algo != self.current_algo:
            self.code_window = TextWindow(self.pos, 
                                          self.size, 
                                          self.pg_manager,
                                          self.controller.states.code_text
                                          ) 
            self.current_algo = self.controller.states.selected_algo

class SettingsPanel:
    
    def __init__(self, fonts, colours, manager, screen, controller):
        self.fonts = fonts
        self.colours = colours
        self.pg_manager = manager
        self.screen = screen
        self.controller = controller

    def create_gen_control_btns(self):
        #Create play button
        self.play_btn = Button(pos= (910, 280),
                               size= (65, 25), 
                               label= "Play", 
                               manager= self.pg_manager, 
                               vis= 0, 
                               id= "#control_button"
                               )
        
        #Create reset button
        self.reset_btn = Button(pos= (1000, 280), 
                                size= (65, 25), 
                                label= "Reset", 
                                manager= self.pg_manager, 
                                vis= 0, 
                                id= "#control_button"
                                )

        #Create pause button
        self.pause_btn = Button(pos= (1090, 280), 
                                size= (65, 25), 
                                label= "Pause", 
                                manager= self.pg_manager, 
                                vis= 0, 
                                id= "#control_button"
                                )
    
    def create_pf_control_btns(self):
        #Create target button
        self.set_target_btn = Button(pos= (910, 120), 
                                     size= (85, 25), 
                                     label= "Set target", 
                                     manager= self.pg_manager, 
                                     vis= 0, 
                                     id= "#control_button"
                                     )
        
        #Create obstacle button
        self.set_obstacle_btn = Button(pos= (1055, 120), 
                                       size= (100, 25), 
                                       label= "Set Obstacle", 
                                       manager= self.pg_manager, 
                                       vis= 0, 
                                       id= "#control_button"
                                       )

    def create_control_sliders(self):
        #Create sliders
        self.size_slider = Slider((910,130), (245, 25), self.pg_manager, (10, 100), 20, 2)
        self.speed_slider = Slider((910,200), (245, 25), self.pg_manager, (1, 100), 50, 2)
        self.size_slider.element.hide()
        self.speed_slider.element.hide()
    
    def create_slider_titles(self):
        #Create slider titles
        self.size_slider_title = self.fonts.slider.render("Adjust Size", True, self.colours.values["text_cl"])
        self.size_slider_title_rect = self.size_slider_title.get_rect()
        self.size_slider_title_rect.bottomleft = (915, 125)

        self.speed_slider_title = self.fonts.slider.render("Adjust Speed", True, self.colours.values["text_cl"])
        self.speed_slider_title_rect = self.speed_slider_title.get_rect()
        self.speed_slider_title_rect.bottomleft = (915, 195)
    
    def blit_size_slider_title(self):
        self.screen.blit(self.size_slider_title, self.size_slider_title_rect)

    def blit_speed_slider_title(self):
        self.screen.blit(self.speed_slider_title, self.speed_slider_title_rect)

    def create_settings(self):
        self.create_gen_control_btns()
        self.create_pf_control_btns()
        self.create_control_sliders()
        self.create_slider_titles()

    def show_bg_control_btns(self):
        self.play_btn.element.show()
        self.reset_btn.element.show()
        self.pause_btn.element.show()
        self.size_slider.element.show()
        self.size_slider.element.enable()
        self.speed_slider.element.show()
        self.speed_slider.element.enable()
        self.set_target_btn.element.hide()
        self.set_obstacle_btn.element.hide()

    def show_pf_control_btns(self):
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
        if event.ui_element == self.play_btn.element:
            self.controller.play_btn_pressed()

        elif event.ui_element == self.reset_btn.element:
            self.controller.reset_btn_pressed()

        elif event.ui_element == self.pause_btn.element:
            self.controller.pause_btn_pressed()
        
        elif event.ui_element == self.set_target_btn.element:
            self.controller.set_target_btn_pressed()
        
        elif event.ui_element == self.set_obstacle_btn.element:
            self.controller.set_obstacle_btn_pressed()

    def event_handle_sliders(self, event):
        if event.ui_element == self.size_slider.element:
            curr_slider_value = self.size_slider.element.get_current_value()
            self.controller.size_slider_moved(curr_slider_value)
        
        elif event.ui_element == self.speed_slider.element:
            curr_slider_value = self.speed_slider.element.get_current_value()
            self.controller.speed_slider_moved(curr_slider_value)

    def update(self):
        if self.controller.states.selected_algo:
            if self.controller.states.curr_algo_cat == "Pathfinding":
                self.show_pf_control_btns()
 
            else:
                self.show_bg_control_btns()

        if self.controller.states.parameter_reset:
            self.size_slider.element.set_current_value(20)
            self.speed_slider.element.set_current_value(50)
            self.controller.set_parameter_reset_false()
    
    def blit_slider_titles(self):
        if self.controller.states.selected_algo:
            if self.controller.states.curr_algo_cat == "Pathfinding":
                self.blit_speed_slider_title()
            else:
                self.blit_speed_slider_title()
                self.blit_size_slider_title()


class InfoPanel:

    def __init__(self, fonts, colours, manager, controller):
        self.fonts = fonts
        self.colours = colours 
        self.controller = controller
        self.manager = manager

        self.info_window = None
        self.current_algo = None

        #Info icon parameters
        self.info_circle_dim = 45
        self.anchor_x = 1035
        self.anchor_y = 360

        #Info box parameters
        self.box_pos = (868, 360)
        self.box_size = (334, 340)
    
    def create_header(self):
        #Create info icon
        self.info_circle_rect = pg.Rect((self.anchor_x - self.info_circle_dim / 2, self.anchor_y - self.info_circle_dim / 2), 
                                        (self.info_circle_dim, self.info_circle_dim)
                                        )
    
        self.letter_i = self.fonts.info_icon.render("i", True, self.colours.values["text_cl"])
        self.letter_i_rect = self.letter_i.get_rect()
        self.letter_i_rect.center = (self.anchor_x - 1, self.anchor_y - 1) #make variables then subtract 1

    def draw_header(self, screen):
        if self.controller.states.selected_algo:
            pg.draw.line(screen, self.colours.values["accent_cl"], (870,360), (1200,360), 5)
            pg.draw.ellipse(screen, self.colours.values["accent_cl"], self.info_circle_rect)
            screen.blit(self.letter_i, self.letter_i_rect)
        
    def create_window(self):
        if self.controller.states.selected_algo and not self.info_window:
            self.current_algo = self.controller.states.selected_algo
            self.info_window = TextWindow(self.box_pos, 
                                          self.box_size, 
                                          self.manager,
                                          self.controller.states.info_text
                                          )
                                             

    def update(self):
        if self.controller.states.selected_algo != self.current_algo:
            self.info_window = TextWindow(self.box_pos, 
                                          self.box_size, 
                                          self.manager,
                                          self.controller.states.info_text
                                          )
            self.current_algo = self.controller.states.selected_algo


        