import pygame as pg
import pygame_gui as pg_gui
from visualizer import AnimationCanvas
from algorithms import BubbleSort, SelectionSort, InsertionSort, LinearSearch, BinarySearch, Bfs, Dfs
from inputs import Parameters, Board
import time
import json


class AppManager:
    def __init__(self):
        #Main window size
        self.screen_size = (1200, 700)
        
        #Animation window instance
        self.anim_canvas = AnimationCanvas()

        #Amount of rectangles cols and rows
        self.rect_amount = (34, 20)

        #Animation window position, size and color
        self.anim_canvas_pos = (185, 50)
        self.anim_canvas_size = (680, 400)

        #Theme colours
        self.colours = {"accent_cl":(58, 186, 249), "text_cl":(255, 255, 255)}

        #Input values for algorithms
        self.values = None
        self.checkerboard = None

        #Default algorithm speed
        self.algo_speed = 10

    def init_pygame(self):
        pg.init() #init pygame

        #Setup clock, window and caption
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("AlgoLab")

    def setup_gui_manager(self):
        #Initiate the gui manager and load themes
        self.manager = pg_gui.UIManager((self.screen_size))
        self.manager.ui_theme.load_theme("themes.json")

    def set_update_intervals(self):
        #Set individual update intervals for gui and animation loop
        self.surface_update_interval = 1/50
        self.gui_update_interval = 1/60
    
    def get_curr_time(self):
        return time.time()
    
    def init_update_time(self):
        #Init the time of last gui and animation loop update
        self.surface_updated = self.get_curr_time()
        self.gui_updated = self.get_curr_time()
    
    def update(self):
        pg.display.flip()
    
    def delay(self, time):
        pg.time.delay(time)

    def run_application_loop(self):
        #Application loop
        self.states.running = True
        while self.states.running:

            time_delta = self.clock.tick(60) / 1000
            
            self.current_time = self.get_curr_time()
            
            #Update interval for GUI (fps)
            if self.current_time - self.gui_updated >= self.gui_update_interval:
                self.gui_updated = self.current_time

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.states.running = False

                    #Process events
                    self.manager.process_events(event)

                    #Handle events
                    if event.type == pg_gui.UI_BUTTON_PRESSED: 

                        
                        #Handle Linear Search button
                        if event.ui_element == self.menu.linear_search_btn.element:
                            #If an algo is running and another algo button is pressed it stops running
                            self.states.algo_running = False

                            #Control buttons and parameter sliders get shown if not already
                            if not self.settings_panel.play_btn.vis:
                                self.settings_panel.play_btn.element.show()
                                self.settings_panel.reset_btn.element.show()
                                self.settings_panel.pause_btn.element.show()
                                self.settings_panel.size_slider.element.show()
                                self.settings_panel.size_slider.element.enable()
                                self.settings_panel.speed_slider.element.show()
                                self.settings_panel.speed_slider.element.enable()
                                
                                self.settings_panel.set_target_btn.element.hide()
                                self.settings_panel.set_obstacle_btn.element.hide()

                            #If there was a checkerboard drawn before set it to None
                            #so the Reset button won't trigger drawing a new one
                            if self.checkerboard:
                                self.checkerboard = None

                            #Save what algo was pressed so the play button knows what algo to run
                            self.states.selected_algo = "Linear Search"
                            self.states.curr_algo_cat = "Searching"

                            #Set default values
                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()
                            self.states.value_to_find = parameters.create_value_to_find()

                            #Show default values
                            self.anim_canvas.draw_bar_graphs(self.values)
                            
                            #Create the generator of the chosen algo
                            lin_search = LinearSearch(self.values, self.anim_canvas, self.states.value_to_find)
                            self.states.algo_generator = lin_search.run()

                        elif event.ui_element == self.menu.binary_search_btn.element:
                            self.states.algo_running = False

                            if not self.settings_panel.play_btn.vis:
                                self.settings_panel.play_btn.element.show()
                                self.settings_panel.reset_btn.element.show()
                                self.settings_panel.pause_btn.element.show()
                                self.settings_panel.size_slider.element.show()
                                self.settings_panel.size_slider.element.enable()
                                self.settings_panel.speed_slider.element.show()
                                self.settings_panel.speed_slider.element.enable()
                                
                                self.settings_panel.set_target_btn.element.hide()
                                self.settings_panel.set_obstacle_btn.element.hide()

                            if self.checkerboard:
                                self.checkerboard = None

                            self.states.selected_algo = "Binary Search"
                            self.states.curr_algo_cat = "Searching"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()
                            self.states.value_to_find = parameters.create_value_to_find()
                            self.values.sort()

                            self.anim_canvas.draw_bar_graphs(self.values)
                            
                            bin_search = BinarySearch(self.values, self.anim_canvas, self.states.value_to_find)
                            self.states.algo_generator = bin_search.run(self.values)

                        #Handle Bubble Sort button
                        elif event.ui_element == self.menu.bubb_sort_btn.element:
                            self.states.algo_running = False

                            self.menu.bubb_sort_btn.element.select()
                            self.menu.sel_sort_btn.element.unselect()
                            self.menu.in_sort_btn.element.unselect()

                            if not self.settings_panel.play_btn.vis:
                                self.settings_panel.play_btn.element.show()
                                self.settings_panel.reset_btn.element.show()
                                self.settings_panel.pause_btn.element.show()
                                self.settings_panel.size_slider.element.show()
                                self.settings_panel.size_slider.element.enable()
                                self.settings_panel.speed_slider.element.show()
                                self.settings_panel.speed_slider.element.enable()
                                
                                self.settings_panel.set_target_btn.element.hide()
                                self.settings_panel.set_obstacle_btn.element.hide()

                                self.info_panel.show_info()
                            
                            if self.checkerboard:
                                self.checkerboard = None

                            self.states.selected_algo = "Bubble Sort"
                            self.states.curr_algo_cat = "Sorting"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()
                            
                            self.anim_canvas.draw_bar_graphs(self.values)
                            
                            #If another algorithm was playing before and got paused
                            #this is going to reset the values if another algorithm gets chosen
                            bubble_sort = BubbleSort(self.values, self.anim_canvas)
                            self.states.algo_generator = bubble_sort.run()

                        #Handle Selection Sort button
                        elif event.ui_element == self.menu.sel_sort_btn.element:
                            self.states.algo_running = False

                            self.menu.sel_sort_btn.element.select()
                            self.menu.bubb_sort_btn.element.unselect()
                            self.menu.in_sort_btn.element.unselect()

                            if not self.settings_panel.play_btn.vis:
                                self.settings_panel.play_btn.element.show()
                                self.settings_panel.reset_btn.element.show()
                                self.settings_panel.pause_btn.element.show()
                                self.settings_panel.size_slider.element.show()
                                self.settings_panel.size_slider.element.enable()
                                self.settings_panel.speed_slider.element.show()
                                self.settings_panel.speed_slider.element.enable()
                                
                                self.settings_panel.set_target_btn.element.hide()
                                self.settings_panel.set_obstacle_btn.element.hide()

                            if self.checkerboard:
                                self.checkerboard = None

                            self.states.selected_algo = "Selection Sort"
                            self.states.curr_algo_cat = "Sorting"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()

                            self.anim_canvas.draw_bar_graphs(self.values)

                            #If another algorithm was playing before and got paused
                            #this is going to reset the values if another algorithm gets chosen
                            sel_sort = SelectionSort(self.values, self.anim_canvas)
                            self.states.algo_generator = sel_sort.run()

                        #Handle Insertion Sort button
                        elif event.ui_element == self.menu.in_sort_btn.element:
                            self.states.algo_running = False

                            self.menu.in_sort_btn.element.select()
                            self.menu.bubb_sort_btn.element.unselect()
                            self.menu.sel_sort_btn.element.unselect()

                            if not self.settings_panel.play_btn.vis:
                                self.settings_panel.play_btn.element.show()
                                self.settings_panel.reset_btn.element.show()
                                self.settings_panel.pause_btn.element.show()
                                self.settings_panel.size_slider.element.show()
                                self.settings_panel.size_slider.element.enable()
                                self.settings_panel.speed_slider.element.show()
                                self.settings_panel.speed_slider.element.enable()
                                
                                self.settings_panel.set_target_btn.element.hide()
                                self.settings_panel.set_obstacle_btn.element.hide()

                            if self.checkerboard:
                                self.checkerboard = None

                            self.states.selected_algo = "Insertion Sort"
                            self.states.curr_algo_cat = "Sorting"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()

                            self.anim_canvas.draw_bar_graphs(self.values)

                            #If another algorithm was playing before and got paused
                            #this is going to reset the values if another algorithm gets chosen
                            in_sort = InsertionSort(self.values, self.anim_canvas)
                            self.states.algo_generator = in_sort.run()

                        #Handle Breadth-First-Search button
                        elif event.ui_element == self.menu.bfs_btn.element:
                            self.states.obstacle_selected = False
                            self.states.target_selected = False
                            self.states.algo_running = False
                            self.settings_panel.size_slider.element.hide()

                            if not self.settings_panel.play_btn.vis:
                                self.settings_panel.play_btn.element.show()
                                self.settings_panel.reset_btn.element.show()
                                self.settings_panel.pause_btn.element.show()
                                self.settings_panel.speed_slider.element.show()
                                self.settings_panel.set_target_btn.element.show()
                                self.settings_panel.set_obstacle_btn.element.show()

                            self.states.selected_algo = "Breadth-First-Search"
                            self.states.curr_algo_cat = "Pathfinding"

                            self.checkerboard = Board(self.anim_canvas_size, self.rect_amount)

                            self.anim_canvas.draw_board(self.checkerboard)

                            bfs = Bfs(self.anim_canvas, self.checkerboard)
                            self.states.algo_generator = bfs.run()

                        #Handle Depth-First-Search button
                        elif event.ui_element == self.menu.dfs_btn.element:
                            self.states.obstacle_selected = False
                            self.states.target_selected = False
                            self.states.algo_running = False
                            self.settings_panel.size_slider.element.hide()

                            if not self.settings_panel.play_btn.vis:
                                self.settings_panel.play_btn.element.show()
                                self.settings_panel.reset_btn.element.show()
                                self.settings_panel.pause_btn.element.show()
                                self.settings_panel.speed_slider.element.show()
                                self.settings_panel.set_target_btn.element.show()
                                self.settings_panel.set_obstacle_btn.element.show()

                            self.states.selected_algo = "Depth-First-Search"
                            self.states.curr_algo_cat = "Pathfinding"

                            self.checkerboard = Board(self.anim_canvas_size, self.rect_amount)

                            self.anim_canvas.draw_board(self.checkerboard)

                            dfs = Dfs(self.anim_canvas, self.checkerboard)
                            self.states.algo_generator = dfs.run(0,0)

                        #Handle Play button
                        elif event.ui_element == self.settings_panel.play_btn.element:
                            
                            if self.states.selected_algo == "Bubble Sort":
                                if not self.states.algo_generator:
                                    bubble_sort = BubbleSort(self.values, self.anim_canvas)
                                    self.states.algo_generator = bubble_sort.run()
                                self.states.algo_running = True
                                self.settings_panel.size_slider.element.disable()

                            elif self.states.selected_algo == "Selection Sort":
                                if not self.states.algo_generator:
                                    sel_sort = SelectionSort(self.values, self.anim_canvas)
                                    self.states.algo_generator = sel_sort.run()
                                self.states.algo_running = True
                                self.settings_panel.size_slider.element.disable()

                            elif self.states.selected_algo == "Insertion Sort":
                                if not self.states.algo_generator:
                                    in_sort = InsertionSort(self.values, self.anim_canvas)
                                    self.states.algo_generator = in_sort.run()
                                self.states.algo_running = True
                                self.settings_panel.size_slider.element.disable()

                            elif self.states.selected_algo == "Linear Search":
                                if not self.states.algo_generator:
                                    lin_search = LinearSearch(self.values, self.anim_canvas, self.states.value_to_find)
                                    self.states.algo_generator = lin_search.run()
                                self.states.algo_running = True
                                self.settings_panel.size_slider.element.disable()

                            elif self.states.selected_algo == "Binary Search":
                                if not self.states.algo_generator:
                                    bin_search = BinarySearch(self.values, self.anim_canvas, self.states.value_to_find)
                                    self.states.algo_generator = bin_search.run(self.values)
                                self.states.algo_running = True
                                self.settings_panel.size_slider.element.disable()

                            elif self.states.selected_algo == "Breadth-First-Search":
                                if not self.states.algo_generator:
                                    bfs = Bfs(self.anim_canvas, self.checkerboard)
                                    self.states.algo_generator = bfs.run()
                                self.states.algo_running = True

                            elif self.states.selected_algo == "Depth-First-Search":
                                if not self.states.algo_generator:
                                    dfs = Dfs(self.anim_canvas, self.checkerboard)
                                    self.states.algo_generator = dfs.run(0,0)
                                self.states.algo_running = True

                        #Handle Reset button
                        elif event.ui_element == self.settings_panel.reset_btn.element:
                            self.states.algo_running = False
                            self.states.algo_generator = None
                            
                            if self.checkerboard:
                                self.states.target_selected = False
                                self.checkerboard = Board(self.anim_canvas_size, self.rect_amount)
                                self.anim_canvas.draw_board(self.checkerboard)

                            else:
                                self.values = parameters.create_values()

                                if self.states.value_to_find:
                                    self.states.value_to_find = parameters.create_value_to_find()
                                    
                                if self.states.selected_algo == "Binary Search":
                                    self.values.sort()

                                self.settings_panel.size_slider.element.enable()
                                self.anim_canvas.draw_bar_graphs(self.values)

                        #Handle Pause button
                        elif event.ui_element == self.settings_panel.pause_btn.element:
                            self.states.algo_running = False

                        #Handle Set Target button
                        elif event.ui_element == self.settings_panel.set_target_btn.element:
                            if self.states.target_selected == False:
                                self.states.target_sel_phase = True
                            if self.states.obstacle_sel_phase:
                                self.states.obstacle_sel_phase = False
                        
                        #Handle Set Obstacle button
                        elif event.ui_element == self.settings_panel.set_obstacle_btn.element:
                            if self.states.obstacle_sel_phase == True:
                                self.states.obstacle_sel_phase = False
                                self.states.obstacle_selected = True
                            else:
                                self.states.obstacle_sel_phase = True
                        

                    #Handle sliders
                    if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        if event.ui_element == self.settings_panel.speed_slider.element:
                            self.surface_update_interval = 1 / self.settings_panel.speed_slider.element.get_current_value()

                        if event.ui_element == self.settings_panel.size_slider.element:
                            new_size = self.settings_panel.size_slider.element.get_current_value()
                            parameters.size = new_size
                            self.values = parameters.create_values()
                            if self.states.algo_generator:
                                self.states.algo_generator = None
                            if self.states.selected_algo == "Binary Search":
                                self.values.sort()
                            self.anim_canvas.draw_bar_graphs(self.values)

                if self.states.curr_algo_cat == "Pathfinding" and self.states.algo_running == False:
                    
                    mouse_pos = pg.mouse.get_pos()
                    mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
                    
                    if pg.mouse.get_pressed()[0] and self.anim_canvas_pos[0] < mouse_x < self.anim_canvas_pos[0] + self.anim_canvas_size[0] and self.anim_canvas_pos[1] < mouse_y < self.anim_canvas_pos[1] + self.anim_canvas_size[1]:
                        canvas_x, canvas_y = mouse_x - self.anim_canvas_pos[0], mouse_y - self.anim_canvas_pos[1]
                        rect_no_x = canvas_x // self.checkerboard.rect_size
                        rect_no_y = canvas_y // self.checkerboard.rect_size
                        
                        if self.states.target_sel_phase:
                            self.checkerboard.raster[rect_no_y][rect_no_x] = 2
                            self.anim_canvas.draw_board(self.checkerboard)
                            self.states.target_selected = True
                            self.states.target_sel_phase = False

                        elif self.states.obstacle_sel_phase:
                            if self.checkerboard.raster[rect_no_y][rect_no_x] != 2:
                                self.checkerboard.raster[rect_no_y][rect_no_x] = 1
                            self.anim_canvas.draw_board(self.checkerboard)
                        else:
                            continue


            if self.states.algo_running and self.current_time - self.surface_updated >= self.surface_update_interval:
                try:
                    next(self.states.algo_generator)
                    self.surface_updated = self.current_time
                except StopIteration: 
                    self.states.algo_running = False
                    self.settings_panel.speed_slider.element.set_current_value(1/20)
                    self.states.algo_generator = None
            
            #Fill background
            self.screen.fill((50,50,50))

            #Update manager
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)  
            
            #Blit animation surface
            self.screen.blit(self.anim_canvas.surface, self.anim_canvas_pos)
    
            pg.draw.rect(self.screen, (20,20,20), self.header.rect) #make color a variable
            
            #Blit texts
            self.header.render_app_name()
            self.screen.blit(self.header.app_name, self.header.app_name_rect)

            if self.states.selected_algo:
                self.cat_name = self.fonts.headline.render(f"Selected Algorithm:   {self.states.selected_algo}", True, self.colours["text_cl"])
                self.cat_name_rect = self.cat_name.get_rect()
                self.cat_name_rect.bottomleft = (200, 40)
                self.info_panel.show_info()
                self.info_panel.render_header(self.screen)

                self.screen.blit(self.info_panel.letter_i, self.info_panel.letter_i_rect)
                self.screen.blit(self.cat_name, self.cat_name_rect)
                self.header.render_settings()
                self.screen.blit(self.header.settings_text, self.header.settings_text_rect)
                self.screen.blit(self.settings_panel.speed_slider_title, self.settings_panel.speed_slider_title_rect)
                if self.states.curr_algo_cat != "Pathfinding":
                    self.screen.blit(self.settings_panel.size_slider_title, self.settings_panel.size_slider_title_rect)
            
            self.update()

        pg.quit()

    def run(self):
        #Init pygame, clock, screen
        self.init_pygame()
        
        #Initiate gui manager
        self.setup_gui_manager()

        #Fonts instance
        self.fonts = AppFonts()

        #Header instance
        self.header = GuiHeader(self.fonts, self.colours, self.screen_size[0])

        #Menu instance
        self.menu = GuiMenu(self.manager)
        self.menu.create_panel()

        #Settings panel instance
        self.settings_panel = GuiSettings(self.fonts, self.colours, self.manager)
        self.settings_panel.create_panel()
    
        #Create application states
        self.states = States()

        #Info panel instance
        self.info_panel = GuiInfoPanel(self.fonts, self.colours, self.states.selected_algo)
        self.info_panel.hide_info()

        self.bs_code_box_rect = pg.Rect((self.anim_canvas_pos[0], self.anim_canvas_pos[1] + self.anim_canvas_size[1] + 5), (self.anim_canvas_size[0], 220))
        self.bs_code_box = pg_gui.elements.UITextBox("Testing", self.bs_code_box_rect, object_id= "#info_text_box")
        self.bs_code_box.hide()

        #Create surface attribute of the animation canvas
        self.anim_canvas.create_surface(self.anim_canvas_size)

        self.set_update_intervals()
        self.init_update_time()
        
        self.run_application_loop()


class Button:
    def __init__(self, pos, size, label, manager, vis, id=None, container=None):
        self.vis = vis
        self.element = pg_gui.elements.UIButton(
            relative_rect= pg.Rect(pos, size),
            text= f"{label}",
            manager= manager,
            visible= self.vis,
            object_id= id,
            container= container
        )


class ScrollContainer:
    def __init__(self, pos, size, manager):
        self.pos = pos
        self.size = size
        self.manager = manager
        self.element = pg_gui.elements.UIScrollingContainer(
            relative_rect= pg.Rect(self.pos, self.size),
            manager= self.manager
        )


class Panel:
    def __init__(self, pos, size, manager, container):
        self.pos = pos
        self.size = size
        self.manager = manager
        self.element = pg_gui.elements.UIPanel(
            relative_rect= pg.Rect(self.pos, self.size),
            manager= self.manager,
            container= container
        )


class Slider:
    def __init__(self, pos, size, manager, range, start_val, click_inc):
        self.rect = pg.Rect(pos, size)
        self.element = pg_gui.elements.UIHorizontalSlider(
            self.rect, 
            start_val, 
            range, 
            manager, 
            click_increment= click_inc
        )


class States:
    def __init__(self):
        #Break condition for App running
        self.running = False

        #Yet no algo started
        self.algo_running = False

        #Initialize a generator for the algorithm steps
        self.algo_generator = None

        #Set the currently selected category and algorithm
        self.selected_algo = None
        self.curr_algo_cat = None

        #Initialize a value to find by search algorithms
        self.value_to_find = None

        #If set True then user can selected a target
        self.target_sel_phase = False
        #Target has been selected
        self.target_selected = False

        #If set True then user can selected obstacles
        self.obstacle_sel_phase = False
        #Obstacle has been selected
        self.obstacle_selected = False


class GuiAnimationWindow:
    def __init__(self):
        pass


class FileReader:
    def __init__(self):
        with open("info_texts.json", "r") as file:
            self.info_texts = json.load(file)

    def get_text(self, algorithm):
        return self.info_texts[f"{algorithm}"]["definition"]
    

class TextWindow:
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        box_rect = pg.Rect(self.pos, self.size)
        self.text = text
        self.element = pg_gui.elements.UITextBox(self.text, box_rect, object_id="#info_text_box")


class GuiInfoPanel:
    def __init__(self, fonts, colours, file_reader):
        self.fonts = fonts
        self.colours = colours 
        #Info icon parameters
        self.info_circle_dim = 45
        self.anchor_x = 1035
        self.anchor_y = 360
        #Info box parameters
        self.box_pos = (868, 360)
        self.box_size = (334, 340)
        self.file_reader = file_reader

        text = self.file_reader.get_text()
        self.info_window = TextWindow(self.box_pos, self.box_size, self.text)
    
    def render_header(self, screen):
        #Create info icon
        self.info_circle_rect = pg.Rect((self.anchor_x - self.info_circle_dim / 2, self.anchor_y - self.info_circle_dim / 2), 
                                        (self.info_circle_dim, self.info_circle_dim)
                                        )
    
        self.letter_i = self.fonts.info_icon.render("i", True, self.colours["text_cl"])
        self.letter_i_rect = self.letter_i.get_rect()
        self.letter_i_rect.center = (1035-1,360-1) #make variables then subtract 1
        
        pg.draw.line(screen, self.colours["accent_cl"], (870,360), (1200,360), 5)
        pg.draw.ellipse(screen, self.colours["accent_cl"], self.info_circle_rect)


class GuiSettings:
    def __init__(self, fonts, colours, manager):
        self.fonts = fonts
        self.colours = colours
        self.manager = manager
    
    def create_panel(self):
        #Create play button
        self.play_btn = Button(pos= (910, 280), size= (65, 25), label= "Play", 
                               manager= self.manager, vis= 0, id= "#control_button")
        
        #Create reset button
        self.reset_btn = Button(pos= (1000, 280), size= (65, 25), label= "Reset", 
                                manager= self.manager, vis= 0, id= "#control_button")

        #Create pause button
        self.pause_btn = Button(pos= (1090, 280), size= (65, 25), label= "Pause", 
                                manager= self.manager, vis= 0, id= "#control_button")

        #Create target button
        self.set_target_btn = Button(pos= (910, 120), size= (85, 25), label= "Set target", 
                                     manager= self.manager, vis= 0, id= "#control_button")
        
        #Create obstacle button
        self.set_obstacle_btn = Button(pos= (1055, 120), size= (100, 25), label= "Set Obstacle", 
                                       manager= self.manager, vis= 0, id= "#control_button")

        #Create sliders
        self.size_slider = Slider((910,130), (245, 25), self.manager, (10, 100), 20, 2)
        self.size_slider.element.hide()

        self.speed_slider = Slider((910,200), (245, 25), self.manager, (1, 100), 50, 2)
        self.speed_slider.element.hide()

        #Create slider titles
        self.size_slider_title = self.fonts.slider.render("Adjust Size", True, self.colours["text_cl"])
        self.size_slider_title_rect = self.size_slider_title.get_rect()
        self.size_slider_title_rect.bottomleft = (915, 125)

        self.speed_slider_title = self.fonts.slider.render("Adjust Speed", True, self.colours["text_cl"])
        self.speed_slider_title_rect = self.speed_slider_title.get_rect()
        self.speed_slider_title_rect.bottomleft = (915, 195)


class GuiMenu:
    def __init__(self, manager):
        self.manager = manager

        self.basic_sort_algs = []
        self.basic_search_algs = []
        self.pathfinding_algs = []
        self.btn_width = 180
        self.btn_height = 45

    def create_panel(self):
        #Create basic-sorts scroll container and scroll panel inside
        self.basic_sorts_scroll_cont = ScrollContainer(pos= (0, 50), size=(200, 200), manager= self.manager) #Actual visible size of container
        self.basic_sorts_scroll_panel = Panel(pos= (0, 0), size= (180, 1200), manager= self.manager, 
                                              container= self.basic_sorts_scroll_cont.element) #Size of scrollable area

        #Create basic sorts category
        self.basic_sorts_btn = Button(pos= (0, 0), size= (self.btn_width, self.btn_height), 
                                  label= "Basic Sorting", manager= self.manager, 
                                  vis= 1, id= "#header_button", container= self.basic_sorts_scroll_panel.element)
        
        self.basic_sort_algs.append(self.basic_sorts_btn)
        self.basic_sorts_btn.element.disable()

        #Create algorithm buttons
        self.bubb_sort_btn = Button(pos= (0, self.btn_height), size= (self.btn_width, self.btn_height),
                                    label= "Bubble Sort", manager= self.manager, 
                                    vis= 1, container= self.basic_sorts_scroll_panel.element)
        
        self.basic_sort_algs.append(self.bubb_sort_btn)

        self.sel_sort_btn = Button(pos=(0, self.btn_height * 2), size= (self.btn_width, self.btn_height), 
                                   label= "Selection Sort", manager= self.manager, 
                                   vis= 1, container= self.basic_sorts_scroll_panel.element)
        
        self.basic_sort_algs.append(self.sel_sort_btn)

        self.in_sort_btn = Button(pos= (0, self.btn_height * 3), size= (self.btn_width, self.btn_height), 
                                  label= "Insertion Sort", manager= self.manager, 
                                  vis= 1, container= self.basic_sorts_scroll_panel.element)
        
        self.basic_sort_algs.append(self.in_sort_btn)

        #Make scrollable area actually scrollable and set size to total height of buttons
        self.basic_sorts_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * len(self.basic_sort_algs)))

        #Create basic search scroll container and scroll panel inside
        self.basic_search_scroll_cont = ScrollContainer(pos= (0, 230), size=(200, 200), manager= self.manager) 
        self.basic_search_scroll_panel = Panel(pos= (0, 0), size= (180, 1200), manager= self.manager, 
                                               container= self.basic_search_scroll_cont.element)

        #Create basic search category
        self.basic_search_btn = Button(pos=(0, 0), size=(self.btn_width, self.btn_height), 
                                   label= "Basic Search", manager= self.manager, 
                                   vis= 1, id= "#header_button", container= self.basic_search_scroll_panel.element)
        
        self.basic_search_algs.append(self.basic_search_btn)
        self.basic_search_btn.element.disable()
        
        self.linear_search_btn = Button(pos=(0, 45), size=(self.btn_width, self.btn_height), 
                                        label= "Linear Search", manager= self.manager, 
                                        vis= 1, container= self.basic_search_scroll_panel.element)
        
        self.basic_search_algs.append(self.linear_search_btn)
        
        self.binary_search_btn = Button(pos=(0, 90), size=(self.btn_width, self.btn_height), 
                                        label= "Binary Search", manager= self.manager, 
                                        vis= 1, container= self.basic_search_scroll_panel.element)
        
        self.basic_search_algs.append(self.binary_search_btn)

        self.basic_search_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * len(self.basic_search_algs)))

        #Create pathfinding scroll container and scroll panel inside
        self.pathfinding_scroll_cont = ScrollContainer(pos= (0, 365), size=(200, 240), manager= self.manager) #Actual visible size of container
        self.pathfinding_scroll_panel = Panel(pos= (0, 0), size= (180, 1200), 
                                              manager= self.manager, container= self.pathfinding_scroll_cont.element) #Size of scrollable area

        #Create pathfinding category
        self.pathfinding_btn = Button(pos=(0, 0), size=(self.btn_width, self.btn_height), 
                                  label= "Pathfinding", manager= self.manager, 
                                  vis= 1, id= "#header_button", container= self.pathfinding_scroll_panel.element)
        
        self.pathfinding_algs.append(self.pathfinding_btn)
        self.pathfinding_btn.element.disable()

        self.bfs_btn = Button(pos=(0, self.btn_height), size= (self.btn_width, self.btn_height), 
                              label= "Breadth-First-Search", manager= self.manager, 
                              vis= 1, container= self.pathfinding_scroll_panel.element)
        
        self.pathfinding_algs.append(self.bfs_btn)

        self.dfs_btn = Button(pos=(0, self.btn_height * 2), size= (self.btn_width, self.btn_height), 
                              label= "Depth-First-Search", manager= self.manager, 
                              vis= 1, container= self.pathfinding_scroll_panel.element)
        
        self.pathfinding_algs.append(self.dfs_btn)

        self.astar_btn = Button(pos=(0, self.btn_height * 3), size= (self.btn_width, self.btn_height), 
                                label= "A*Search", manager= self.manager, 
                                vis= 1, container= self.pathfinding_scroll_panel.element)
        
        self.pathfinding_algs.append(self.astar_btn)

        self.dijkstra_btn = Button(pos=(0, self.btn_height * 4), size= (self.btn_width, self.btn_height), 
                                   label= "Dijkstra's", manager= self.manager, 
                                   vis= 1, container= self.pathfinding_scroll_panel.element)
        
        self.pathfinding_algs.append(self.dijkstra_btn)

        self.pathfinding_scroll_cont.element.set_scrollable_area_dimensions((self.btn_width, self.btn_height * len(self.pathfinding_algs)))


class GuiCodePanel:
    def __init__(self):
        pass


class GuiHeader:
    def __init__(self, fonts, colours, screen_width):
        self.fonts = fonts
        self.colours = colours
        self.rect = pg.Rect((0,0), (screen_width, 50))

    def render_app_name(self):
        #Render application name
        self.app_name = self.fonts.title.render("AlgoLab", True, self.colours["text_cl"]) #title
        self.app_name_rect = self.app_name.get_rect()
        self.app_name_rect.bottomleft = (40, 40)
        
    def render_settings(self):
        #Render settings
        self.settings_text = self.fonts.headline.render("Settings", True, self.colours["text_cl"])
        self.settings_text_rect = self.settings_text.get_rect()
        self.settings_text_rect.bottomleft = (880, 40)


class AppFonts:
    def __init__(self):
        #Setup fonts
        self.title = pg.font.SysFont("Verdana", 27)
        self.headline = pg.font.SysFont("Verdana", 20)
        self.slider = pg.font.SysFont("Verdana", 12)
        self.info_icon = pg.font.SysFont("timesnewroman", 30, True)


if __name__ == "__main__":
    app = AppManager()
    app.run()