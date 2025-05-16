"""The main application file that should be run"""

import pygame as pg
import pygame_gui as pg_gui
from algorithms import *
from gui_manager import GuiManager
from app_controller import AppController
from utils import Parameters, Board
import time


class MainApp:
    def __init__(self):
        #Main window size
        self.screen_size = (1200, 700)

        #Amount of rectangles cols and rows
        self.rect_amount = (34, 20)

    def init_pygame(self):
        pg.init() #init pygame

        #Setup clock, window and caption
        self.clock = pg.time.Clock()

    def setup_pg_manager(self):
        #Initiate the pg manager and load themes
        self.pg_manager = pg_gui.UIManager((self.screen_size))
        self.pg_manager.ui_theme.load_theme("themes.json")
    
    def get_curr_time(self):
        return time.time()
    
    def update(self):
        pg.display.flip()
    
    def delay(self, time):
        pg.time.delay(time)
    
    def run(self):

        self.init_pygame()
        self.setup_pg_manager()

        self.controller = AppController()

        self.current_time = self.get_curr_time()
        self.controller.set_current_time(self.current_time)

        self.gui_manager = GuiManager(self.controller, self.pg_manager)
        self.gui_manager.create_gui()

        
        
        self.run_application_loop()

    def run_application_loop(self):
        #Application loop
        self.controller.states.app_running = True
        while self.controller.states.app_running:

            time_delta = self.clock.tick(60) / 1000
            self.current_time = self.get_curr_time()
            
            #Update gui 
            if self.controller.check_gui_update(self.current_time):

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.controller.states.app_running = False

                    #Process events
                    self.pg_manager.process_events(event)

                    #Handle events
                    if event.type == pg_gui.UI_BUTTON_PRESSED: 

                        self.gui_manager.menu_panel.event_handle(event)
                        self.gui_manager.settings_panel.event_handle_btns(event)

                    if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        self.gui_manager.settings_panel.event_handle_sliders(event)
            
            #Update animation surface
            if self.controller.check_surface_update(self.current_time):

                self.controller.next_animation_step()
            
            self.gui_manager.main_panel.screen.fill((self.gui_manager.colours.values["main_bg_cl"]))

            self.gui_manager.animation_panel.update()
            self.gui_manager.animation_panel.blit_surface()
            self.gui_manager.main_panel.update()
            if self.controller.states.curr_algo_cat:
                self.gui_manager.settings_panel.update()
                self.gui_manager.settings_panel.blit_slider_titles()
            
            #Update pygame_gui manager
            self.pg_manager.update(time_delta)
            self.pg_manager.draw_ui(self.gui_manager.main_panel.screen)   
            
            self.update()

        pg.quit()


if __name__ == "__main__":
    app = MainApp()
    app.run()