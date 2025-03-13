import pygame as pg
import pygame_gui as pg_gui
from visualizer import AnimationCanvas
from algorithms import Parameters, BubbleSort
import random

class GuiManager:
    def __init__(self, anim_canvas):
        #Main window size
        self.screen_size = (1400, 700)

        #Animation window instance
        self.anim_canvas = anim_canvas

        #Animation window position, size and color
        self.anim_canvas_pos = (300, 50)
        self.anim_canvas_size = (650, 350)
        self.anim_canvas_cl = (100, 100, 100)

        #Input values for algorithms
        self.values = None

    def run(self):
        pg.init()

        #Setup clock and display
        clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("AlgoLab")

        #Initiate the gui manager
        self.manager = pg_gui.UIManager((self.screen_size))
        
        #Create buttons
        bubb_sort_btn = Button(pos= (0,50), size= (300, 45), label= "Bubble Sort", manager= self.manager, vis= 1)
        sel_sort_btn = Button(pos=(0,95), size= (300, 45), label= "Selection Sort", manager= self.manager, vis= 1)
        play_btn = Button(pos= (1050, 50), size= (60, 60), label= "Play", manager= self.manager, vis= 0)
        play_btn.element.hide()
        
        selected_algo = "None"

        self.anim_canvas.create_surface(self.anim_canvas_size)
        running = True
        while running:

            time_delta = clock.tick(60) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                self.manager.process_events(event)

                if event.type == pg_gui.UI_BUTTON_PRESSED:      
                    #Handle Bubble Sort button
                    if event.ui_element == bubb_sort_btn.element:
                        if not play_btn.vis:
                            play_btn.element.show()

                        selected_algo = "Bubble Sort"
                        self.values = Parameters(size= 10,speed= 50).create_values()
                        print("BubbSort button pressed")

                    #Handle Selection Sort button
                    elif event.ui_element == sel_sort_btn.element:
                        if not play_btn.vis:
                            play_btn.element.show()

                        selected_algo = "Selection Sort"
                        self.values = Parameters(size= 10,speed= 50).create_values()
                        print("SelSort button pressed")

                    #Handle Play button
                    elif event.ui_element == play_btn.element:
                        if selected_algo == "Bubble Sort":
                            print(self.values)
                            print("Play BubbSort")
                        elif selected_algo == "Selection Sort":
                            print(self.values)
                            print("Play SelSort")

            #Fill background
            self.screen.fill((0,0,0))

            #Update manager
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)  
            
            #Blit animation surface
            self.anim_canvas.surface.fill(self.anim_canvas_cl)
            self.screen.blit(self.anim_canvas.surface, self.anim_canvas_pos)
            self.update()

        pg.quit()

    def update(self):
        pg.display.update()

class Button:
    def __init__(self, pos, size, label, manager, vis):
        self.pos = pos
        self.size = size
        self.label = label
        self.vis = vis
        self.element = pg_gui.elements.UIButton(
            relative_rect= pg.Rect(self.pos[0],self.pos[1], self.size[0], self.size[1]),
            text= f"{self.label}",
            manager= manager,
            visible= self.vis
        )

class DropDownMenu:
    def __init__(self, size, pos, manager):
        self.size = size
        self.pos = pos
        self.manager = manager
        self.element = pg_gui.elements.UIDropDownMenu(
            options_list= ["Bubble Sort", "Selection Sort", "Insertion Sort"],
            starting_option="Bubble Sort",
            relative_rect= pg.Rect(self.pos[0],self.pos[1], self.size[0], self.size[1]),
            manager = self.manager
        )

class Slider:
    def __init__(self):
        pass

class TextWindow:
    def __init__(self):
        pass

if __name__ == "__main__":
    anim_surface = AnimationCanvas()
    app = GuiManager(anim_surface)
    app.run()