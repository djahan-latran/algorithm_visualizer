import pygame as pg
import pygame_gui as pg_gui
from visualizer import AnimationCanvas
from algorithms import BubbleSort
import random

class GuiManager:
    def __init__(self, anim_canvas):
        self.screen_size = (1400, 700)
        self.anim_canvas = anim_canvas
        self.anim_canvas_pos = (300, 50)
        self.anim_canvas_size = (650, 350)
        self.anim_canvas_cl = (100, 100, 100)

    def run(self):
        pg.init()

        clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("AlgoLab")

        self.manager = pg_gui.UIManager((self.screen_size))
        
        bs_button = Button(pos= (0,50), size= (300, 45), label= "Bubble Sort", manager= self.manager)
        dp_menu = DropDownMenu(pos= (0, 100), size= (300, 45), manager= self.manager)
        
        self.anim_canvas.create_surface(self.anim_canvas_size)
        running = True
        while running:

            time_delta = clock.tick(60) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                self.manager.process_events(event)

                if event.type == pg_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == bs_button:
                        pass

            self.manager.update(time_delta)
            self.screen.fill((0,0,0))
            self.manager.draw_ui(self.screen)
            self.anim_canvas.surface.fill(self.anim_canvas_cl)
            self.screen.blit(self.anim_canvas.surface, self.anim_canvas_pos)
            self.update()

        pg.quit()

    def update(self):
        pg.display.update()

class Button:
    def __init__(self, pos, size, label, manager):
        self.pos = pos
        self.size = size
        self.label = label
        self.manager = manager
        pg_gui.elements.UIButton(
            relative_rect= pg.Rect(self.pos[0],self.pos[1], self.size[0], self.size[1]),
            text= f"{self.label}",
            manager= self.manager
        )

class DropDownMenu:
    def __init__(self, size, pos, manager):
        self.size = size
        self.pos = pos
        self.manager = manager
        pg_gui.elements.UIDropDownMenu(
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

    #nums = random.sample(range(100), 20)
    
    #bubble_sort = BubbleSort(nums)
    anim_surface = AnimationCanvas()
    app = GuiManager(anim_surface)
    app.run()