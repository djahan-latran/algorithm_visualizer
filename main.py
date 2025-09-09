"""The main application file that should be run"""
import os
import pygame as pg
import pygame_gui as pg_gui
from src.algorithms import *
from src.gui.gui_manager import GuiManager
from src.app_controller import AppController
import time


class MainApp:
    """ Initiates all the necessary moduls. Holds the main application loop.
        Starts and ends the application.
    """
    def __init__(self):
        #Main window size
        self.screen_size = (1200, 700)

    def init_pygame(self):
        """ Initiates the pygame module
        """
        pg.init() #init pygame

        #Setup clock, window and caption
        self.clock = pg.time.Clock()

    def setup_pg_manager(self):
        """ Sets up the pygame_gui manager
        """
        #Initiate the pg manager and load themes
        self.pg_manager = pg_gui.UIManager((self.screen_size))

        file_directory = os.path.dirname(__file__)
        file_path = os.path.join(file_directory,"src", "gui", "themes.json")

        try:
            self.pg_manager.ui_theme.load_theme(file_path)
        except FileNotFoundError:
            print("The theme file for the pg_manager could not be found")
    
    def get_curr_time(self):
        """ Returns the current app-time
        """
        return time.time()
    
    def update(self):
        """ Updates the pygame display.
        """
        pg.display.flip()
    
    def run(self):
        """ Sets up everything for the application to start. Initiates the controller, aswell as the gui-manager.
            Calls the application loop after setting everything up.
        """

        self.init_pygame()
        self.setup_pg_manager()

        self.controller = AppController()

        self.current_time = self.get_curr_time()
        self.controller.set_current_time(self.current_time)

        self.gui_manager = GuiManager(self.controller, self.pg_manager)
        self.gui_manager.create_gui()
        
        # Call application loop
        self._run_application_loop()

    def _run_application_loop(self):
        """ The application loop that runs as long as the application is open.
        """
        # Application loop
        self.controller.states.app_running = True
        while self.controller.states.app_running:

            time_delta = self.clock.tick(60) / 1000
            self.current_time = self.get_curr_time()
            
            # Update gui 
            if self.controller.check_gui_update(self.current_time):

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.controller.states.app_running = False

                    # Process events
                    self.pg_manager.process_events(event)

                    # Handle events
                    if event.type == pg_gui.UI_BUTTON_PRESSED: 

                        self.gui_manager.menu_panel.event_handle(event)
                        self.gui_manager.settings_panel.event_handle_btns(event)

                    if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        self.gui_manager.settings_panel.event_handle_sliders(event)
            
            # Update animation surface
            if self.controller.check_surface_update(self.current_time):

                self.controller.next_animation_step()
            
            self.gui_manager.main_panel.screen.fill((self.gui_manager.colours.values["main_bg_cl"]))

            # Update the panels
            self.gui_manager.animation_panel.update()
            self.gui_manager.animation_panel.blit_surface()
            self.gui_manager.main_panel.update()
            self.gui_manager.settings_panel.update()
            self.gui_manager.info_panel.update()
            self.gui_manager.code_panel.update()
            
            # Update pygame_gui manager
            self.pg_manager.update(time_delta)
            self.pg_manager.draw_ui(self.gui_manager.main_panel.screen)
            # Draw header lastly so it is above info_text panel   
            self.gui_manager.info_panel.draw_header(self.gui_manager.main_panel.screen)
            # Update pygame display
            self.update()

        pg.quit()


if __name__ == "__main__":
    app = MainApp()
    app.run()