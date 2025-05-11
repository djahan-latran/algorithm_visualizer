"""The main application file that should be run"""

import pygame as pg
import pygame_gui as pg_gui
from algorithms import *
from gui_manager import GuiManager
from app_controller import AppController
from utils import Parameters, Board
import time
import json


class MainApp:
    def __init__(self):
        #Main window size
        self.screen_size = (1200, 700)

        #Amount of rectangles cols and rows
        self.rect_amount = (34, 20)
      
        #Input values for algorithms
        self.values = None
        self.checkerboard = None

    def init_pygame(self):
        pg.init() #init pygame

        #Setup clock, window and caption
        self.clock = pg.time.Clock()

    def setup_pg_manager(self):
        #Initiate the pg manager and load themes
        self.pg_manager = pg_gui.UIManager((self.screen_size))
        self.pg_manager.ui_theme.load_theme("themes.json")

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
    
    def run(self):

        self.init_pygame()
        self.setup_pg_manager()

        self.controller = AppController()

        self.gui_manager = GuiManager(self.controller, self.pg_manager)
        self.gui_manager.create_gui()
        
        self.set_update_intervals()
        self.init_update_time()
        
        self.run_application_loop()

    def run_application_loop(self):
        #Application loop
        self.controller.states.running = True
        while self.controller.states.running:

            time_delta = self.clock.tick(60) / 1000
            
            self.current_time = self.get_curr_time()

            #Update interval for GUI (fps)
            if self.current_time - self.gui_updated >= self.gui_update_interval:
                self.gui_updated = self.current_time

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.controller.states.running = False

                    #Process events
                    self.pg_manager.process_events(event)

                    #Handle events
                    if event.type == pg_gui.UI_BUTTON_PRESSED: 

                        self.gui_manager.menu_panel.event_handle(event)

                            #If an algo is running and another algo button is pressed it stops running


            if self.controller.states.algo_running and self.current_time - self.surface_updated >= self.surface_update_interval:
                try:
                    next(self.controller.states.algo_generator)
                    self.surface_updated = self.current_time
                except StopIteration: 
                    self.controller.states.algo_running = False
                    self.gui_manager.settings_panel.speed_slider.element.set_current_value(1/20)
                    self.controller.states.algo_generator = None

            self.gui_manager.main_panel.screen.fill((50,50,50))

            self.gui_manager.settings_panel.update()
            self.gui_manager.animation_panel.update()
            #Update manager
            self.pg_manager.update(time_delta)
            self.pg_manager.draw_ui(self.gui_manager.main_panel.screen)  
            

            if self.controller.states.selected_algo:
                self.cat_name = self.gui_manager.fonts.headline.render(f"Selected Algorithm:   {self.controller.states.selected_algo}", 
                                                                       True, self.gui_manager.colours.values["text_cl"]
                                                                       )
                self.cat_name_rect = self.cat_name.get_rect()
                self.cat_name_rect.bottomleft = (200, 40)
                #self.gui_manager.info_panel.show_info()
                #self.info_panel.render_header(self.screen)

                # self.gui_manager.main_panel.screen.blit(self.info_panel.letter_i, 
                #                                         self.info_panel.letter_i_rect)
                self.gui_manager.main_panel.screen.blit(self.cat_name, self.cat_name_rect)
                
            
            self.update()

        pg.quit()


                        # elif event.ui_element == self.menu.binary_search_btn.element:
                        #     self.controller.states.algo_running = False

                        #     if not self.settings_panel.play_btn.vis:
                        #         self.settings_panel.play_btn.element.show()
                        #         self.settings_panel.reset_btn.element.show()
                        #         self.settings_panel.pause_btn.element.show()
                        #         self.settings_panel.size_slider.element.show()
                        #         self.settings_panel.size_slider.element.enable()
                        #         self.settings_panel.speed_slider.element.show()
                        #         self.settings_panel.speed_slider.element.enable()
                                
                        #         self.settings_panel.set_target_btn.element.hide()
                        #         self.settings_panel.set_obstacle_btn.element.hide()

                        #     if self.checkerboard:
                        #         self.checkerboard = None

                        #     self.states.selected_algo = "Binary Search"
                        #     self.states.curr_algo_cat = "Searching"

                        #     parameters = Parameters(size= 20)
                        #     self.values = parameters.create_values()
                        #     self.states.value_to_find = parameters.create_value_to_find()
                        #     self.values.sort()

                        #     self.anim_canvas.draw_bar_graphs(self.values)
                            
                        #     bin_search = BinarySearch(self.values, self.anim_canvas, self.states.value_to_find)
                        #     self.states.algo_generator = bin_search.run(self.values)

                        # #Handle Bubble Sort button
                        # elif event.ui_element == self.menu.bubb_sort_btn.element:
                        #     self.states.algo_running = False

                        #     self.menu.bubb_sort_btn.element.select()
                        #     self.menu.sel_sort_btn.element.unselect()
                        #     self.menu.in_sort_btn.element.unselect()

                        #     if not self.settings_panel.play_btn.vis:
                        #         self.settings_panel.play_btn.element.show()
                        #         self.settings_panel.reset_btn.element.show()
                        #         self.settings_panel.pause_btn.element.show()
                        #         self.settings_panel.size_slider.element.show()
                        #         self.settings_panel.size_slider.element.enable()
                        #         self.settings_panel.speed_slider.element.show()
                        #         self.settings_panel.speed_slider.element.enable()
                                
                        #         self.settings_panel.set_target_btn.element.hide()
                        #         self.settings_panel.set_obstacle_btn.element.hide()

                        #         self.info_panel.show_info()
                            
                        #     if self.checkerboard:
                        #         self.checkerboard = None

                        #     self.states.selected_algo = "Bubble Sort"
                        #     self.states.curr_algo_cat = "Sorting"

                        #     parameters = Parameters(size= 20)
                        #     self.values = parameters.create_values()
                            
                        #     self.anim_canvas.draw_bar_graphs(self.values)
                            
                        #     #If another algorithm was playing before and got paused
                        #     #this is going to reset the values if another algorithm gets chosen
                        #     bubble_sort = BubbleSort(self.values, self.anim_canvas)
                        #     self.states.algo_generator = bubble_sort.run()

 

                        #Handle Breadth-First-Search button
            #             elif event.ui_element == self.menu.bfs_btn.element:
            #                 self.states.obstacle_selected = False
            #                 self.states.target_selected = False
            #                 self.states.algo_running = False
            #                 self.settings_panel.size_slider.element.hide()

            #                 if not self.settings_panel.play_btn.vis:
            #                     self.settings_panel.play_btn.element.show()
            #                     self.settings_panel.reset_btn.element.show()
            #                     self.settings_panel.pause_btn.element.show()
            #                     self.settings_panel.speed_slider.element.show()
            #                     self.settings_panel.set_target_btn.element.show()
            #                     self.settings_panel.set_obstacle_btn.element.show()

            #                 self.states.selected_algo = "Breadth-First-Search"
            #                 self.states.curr_algo_cat = "Pathfinding"

            #                 self.checkerboard = Board(self.anim_canvas_size, self.rect_amount)

            #                 self.anim_canvas.draw_board(self.checkerboard)

            #                 bfs = Bfs(self.anim_canvas, self.checkerboard)
            #                 self.states.algo_generator = bfs.run()

            #             #Handle Depth-First-Search button
            #             elif event.ui_element == self.menu.dfs_btn.element:
            #                 self.states.obstacle_selected = False
            #                 self.states.target_selected = False
            #                 self.states.algo_running = False
            #                 self.settings_panel.size_slider.element.hide()

            #                 if not self.settings_panel.play_btn.vis:
            #                     self.settings_panel.play_btn.element.show()
            #                     self.settings_panel.reset_btn.element.show()
            #                     self.settings_panel.pause_btn.element.show()
            #                     self.settings_panel.speed_slider.element.show()
            #                     self.settings_panel.set_target_btn.element.show()
            #                     self.settings_panel.set_obstacle_btn.element.show()

            #                 self.states.selected_algo = "Depth-First-Search"
            #                 self.states.curr_algo_cat = "Pathfinding"

            #                 self.checkerboard = Board(self.anim_canvas_size, self.rect_amount)

            #                 self.anim_canvas.draw_board(self.checkerboard)

            #                 dfs = Dfs(self.anim_canvas, self.checkerboard)
            #                 self.states.algo_generator = dfs.run(0,0)

            #             #Handle Play button
            #             elif event.ui_element == self.settings_panel.play_btn.element:

            #                 elif self.states.selected_algo == "Insertion Sort":
            #                     if not self.states.algo_generator:
            #                         in_sort = InsertionSort(self.values, self.anim_canvas)
            #                         self.states.algo_generator = in_sort.run()
            #                     self.states.algo_running = True
            #                     self.settings_panel.size_slider.element.disable()

            #                 elif self.states.selected_algo == "Linear Search":
            #                     if not self.states.algo_generator:
            #                         lin_search = LinearSearch(self.values, self.anim_canvas, self.states.value_to_find)
            #                         self.states.algo_generator = lin_search.run()
            #                     self.states.algo_running = True
            #                     self.settings_panel.size_slider.element.disable()

            #                 elif self.states.selected_algo == "Breadth-First-Search":
            #                     if not self.states.algo_generator:
            #                         bfs = Bfs(self.anim_canvas, self.checkerboard)
            #                         self.states.algo_generator = bfs.run()
            #                     self.states.algo_running = True

            #             #Handle Reset button
            #             elif event.ui_element == self.settings_panel.reset_btn.element:
            #                 self.states.algo_running = False
            #                 self.states.algo_generator = None
                            
            #                 if self.checkerboard:
            #                     self.states.target_selected = False
            #                     self.checkerboard = Board(self.anim_canvas_size, self.rect_amount)
            #                     self.anim_canvas.draw_board(self.checkerboard)

            #                 else:
            #                     self.values = parameters.create_values()

            #                     if self.states.value_to_find:
            #                         self.states.value_to_find = parameters.create_value_to_find()
                                    
            #                     if self.states.selected_algo == "Binary Search":
            #                         self.values.sort()

            #                     self.settings_panel.size_slider.element.enable()
            #                     self.anim_canvas.draw_bar_graphs(self.values)

            #             #Handle Pause button
            #             elif event.ui_element == self.settings_panel.pause_btn.element:
            #                 self.states.algo_running = False

            #             #Handle Set Target button
            #             elif event.ui_element == self.settings_panel.set_target_btn.element:
            #                 if self.states.target_selected == False:
            #                     self.states.target_sel_phase = True
            #                 if self.states.obstacle_sel_phase:
            #                     self.states.obstacle_sel_phase = False
                        
            #             #Handle Set Obstacle button
            #             elif event.ui_element == self.settings_panel.set_obstacle_btn.element:
            #                 if self.states.obstacle_sel_phase == True:
            #                     self.states.obstacle_sel_phase = False
            #                     self.states.obstacle_selected = True
            #                 else:
            #                     self.states.obstacle_sel_phase = True
                        

            #         #Handle sliders
            #         if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
            #             if event.ui_element == self.settings_panel.speed_slider.element:
            #                 self.surface_update_interval = 1 / self.settings_panel.speed_slider.element.get_current_value()

            #             if event.ui_element == self.settings_panel.size_slider.element:
            #                 new_size = self.settings_panel.size_slider.element.get_current_value()
            #                 parameters.size = new_size
            #                 self.values = parameters.create_values()
            #                 if self.states.algo_generator:
            #                     self.states.algo_generator = None
            #                 if self.states.selected_algo == "Binary Search":
            #                     self.values.sort()
            #                 self.anim_canvas.draw_bar_graphs(self.values)

            #     if self.controller.states.curr_algo_cat == "Pathfinding" and self.controller.states.algo_running == False:
                    
            #         mouse_pos = pg.mouse.get_pos()
            #         mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
                    
            #         if pg.mouse.get_pressed()[0] and self.anim_canvas_pos[0] < mouse_x < self.anim_canvas_pos[0] + self.anim_canvas_size[0] and self.anim_canvas_pos[1] < mouse_y < self.anim_canvas_pos[1] + self.anim_canvas_size[1]:
            #             canvas_x, canvas_y = mouse_x - self.anim_canvas_pos[0], mouse_y - self.anim_canvas_pos[1]
            #             rect_no_x = canvas_x // self.checkerboard.rect_size
            #             rect_no_y = canvas_y // self.checkerboard.rect_size
                        
            #             if self.states.target_sel_phase:
            #                 self.checkerboard.raster[rect_no_y][rect_no_x] = 2
            #                 self.anim_canvas.draw_board(self.checkerboard)
            #                 self.states.target_selected = True
            #                 self.states.target_sel_phase = False

            #             elif self.states.obstacle_sel_phase:
            #                 if self.checkerboard.raster[rect_no_y][rect_no_x] != 2:
            #                     self.checkerboard.raster[rect_no_y][rect_no_x] = 1
            #                 self.anim_canvas.draw_board(self.checkerboard)
            #             else:
            #                 continue
            


if __name__ == "__main__":
    app = MainApp()
    app.run()