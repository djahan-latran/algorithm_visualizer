import pygame as pg
import pygame_gui as pg_gui
from visualizer import AnimationCanvas
from algorithms import Parameters, BubbleSort, SelectionSort, InsertionSort
import random

class GuiManager:
    def __init__(self, anim_canvas):
        #Main window size
        self.screen_size = (1200, 700)

        #Animation window instance
        self.anim_canvas = anim_canvas

        #Animation window position, size and color
        self.anim_canvas_pos = (185, 50)
        self.anim_canvas_size = (650, 350)
        self.anim_canvas_cl = (100, 100, 100)

        #Input values for algorithms
        self.values = None

        #Default algorithm speed
        self.algo_speed = 10

    def run(self):
        pg.init()

        #Setup clock and display
        clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("AlgoLab")

        #Initiate the gui manager
        self.manager = pg_gui.UIManager((self.screen_size))
        

        #Create basic-sorts scroll container and scroll panel inside
        basic_sorts_scroll_cont = ScrollContainer(pos= (0, 50), size=(200, 200), manager= self.manager) #Actual visible size of container
        basic_sorts_scroll_panel = Panel(pos= (0, 0), size= (180, 1200), manager= self.manager, container= basic_sorts_scroll_cont.element) #Size of scrollable area

        #Create basic sorts category
        basic_sorts = Button(pos= (0, 0), size= (180, 45), label= "Basic Sorting", manager= self.manager, vis= 1, container= basic_sorts_scroll_panel.element)
        basic_sorts.element.disable()

        #Create algorithm buttons
        basic_sorts_btn_amount = 1
        bubb_sort_btn = Button(pos= (0, 45), size= (180, 45), label= "Bubble Sort", manager= self.manager, vis= 1, container= basic_sorts_scroll_panel.element)
        basic_sorts_btn_amount += 1

        sel_sort_btn = Button(pos=(0, 90), size= (180, 45), label= "Selection Sort", manager= self.manager, vis= 1, container= basic_sorts_scroll_panel.element)
        basic_sorts_btn_amount += 1

        in_sort_btn = Button(pos= (0, 135), size= (180, 45), label= "Insertion Sort", manager= self.manager, vis= 1, container= basic_sorts_scroll_panel.element)
        basic_sorts_btn_amount += 1

        #Make scrollable area actually scrollable and set size to total height of buttons
        basic_sorts_scroll_cont.element.set_scrollable_area_dimensions((180, 45 * basic_sorts_btn_amount))


        #Create basic search scroll container and scroll panel inside
        basic_search_scroll_cont = ScrollContainer(pos= (0, 230), size=(200, 200), manager= self.manager) 
        basic_search_scroll_panel = Panel(pos= (0, 0), size= (180, 1200), manager= self.manager, container= basic_search_scroll_cont.element)

        basic_search = Button(pos=(0, 0), size=(180, 45), label= "Basic Search", manager= self.manager, vis= 1, container= basic_search_scroll_panel.element)
        basic_search.element.disable()

        basic_search_btn_amount = 1
        
        linear_search = Button(pos=(0, 45), size=(180, 45), label= "Linear Search", manager= self.manager, vis= 1, container= basic_search_scroll_panel.element)
        basic_search_btn_amount += 1
        
        binary_search = Button(pos=(0, 90), size=(180, 45), label= "Binary Search", manager= self.manager, vis= 1, container= basic_search_scroll_panel.element)
        basic_search_btn_amount += 1

        basic_search_scroll_cont.element.set_scrollable_area_dimensions((180, 45 * basic_search_btn_amount))


        #Create play button
        play_btn = Button(pos= (890, 280), size= (65, 25), label= "Play", manager= self.manager, vis= 0)
        
        #Create reset button
        reset_btn = Button(pos= (990, 280), size= (65, 25), label= "Reset", manager= self.manager, vis= 0)

        #Create reset button
        pause_btn = Button(pos= (1090, 280), size= (65, 25), label= "Pause", manager= self.manager, vis= 0)


        #Create sliders
        size_slider_rect = pg.Rect((890,100), (200,50))
        size_slider = pg_gui.elements.UIHorizontalSlider(size_slider_rect, 100, (0,200), self.manager)
        size_slider.enable()

        #First no algorithm is selected, therefore no control-buttons show up
        selected_algo = None

        #Create surface attribute of the animation canvas
        self.anim_canvas.create_surface(self.anim_canvas_size)
        
        self.algo_generator = None
        #Break condition for App running
        self.running = True
        #Yet no algo started
        self.algo_running = False
        #Application loop
        while self.running:

            time_delta = clock.tick(60) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                #Process events
                self.manager.process_events(event)

                #Handle events
                if event.type == pg_gui.UI_BUTTON_PRESSED: 

                    #Handle Bubble Sort button
                    if event.ui_element == bubb_sort_btn.element:
                        self.algo_running = False

                        if not play_btn.vis:
                            play_btn.element.show()
                            reset_btn.element.show()
                            pause_btn.element.show()

                        selected_algo = "Bubble Sort"

                        parameters = Parameters(size= 20,speed= 100)
                        self.values = parameters.create_values()
                        self.algo_speed = parameters.speed
                        
                        self.anim_canvas.draw_bar_graphs(self.values)

                    #Handle Selection Sort button
                    elif event.ui_element == sel_sort_btn.element:
                        self.algo_running = False
                        if not play_btn.vis:
                            play_btn.element.show()
                            reset_btn.element.show()
                            pause_btn.element.show()

                        selected_algo = "Selection Sort"

                        parameters = Parameters(size= 20,speed= 50)
                        self.values = parameters.create_values()
                        self.algo_speed = parameters.speed

                        self.anim_canvas.draw_bar_graphs(self.values)

                    #Handle Insertion Sort button
                    elif event.ui_element == in_sort_btn.element:
                        self.algo_running = False
                        if not play_btn.vis:
                            play_btn.element.show()
                            reset_btn.element.show()
                            pause_btn.element.show()

                        selected_algo = "Insertion Sort"

                        parameters = Parameters(size= 20, speed= 50)
                        self.values = parameters.create_values()
                        self.algo_speed = parameters.speed

                        self.anim_canvas.draw_bar_graphs(self.values)

                    #Handle Play button
                    elif event.ui_element == play_btn.element:
                        
                        if selected_algo == "Bubble Sort":
                            if not self.algo_generator:
                                bubble_sort = BubbleSort(self.values, self.anim_canvas)
                                self.algo_generator = bubble_sort.run()
                            self.algo_running = True

                        elif selected_algo == "Selection Sort":
                            sel_sort = SelectionSort(self.values, self.anim_canvas)
                            self.algo_generator = sel_sort.run()
                            self.algo_running = True

                        elif selected_algo == "Insertion Sort":
                            in_sort = InsertionSort(self.values, self.anim_canvas)
                            self.algo_generator = in_sort.run()
                            self.algo_running = True

                    #Handle Reset button
                    elif event.ui_element == reset_btn.element:
                        self.algo_running = False
                        self.algo_generator = None
                        self.values = Parameters(size= 20,speed= 50).create_values()
                        self.anim_canvas.draw_bar_graphs(self.values)

                    #Handle Pause button
                    elif event.ui_element == pause_btn.element:
                        self.algo_running = False

                #Handel size slider
                if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == size_slider:
                        self.algo_speed = size_slider.get_current_value()
                        print(size_slider.get_current_value())
                        


            if self.algo_running:
                try:
                    next(self.algo_generator)
                except StopIteration:
                    self.algo_running = False
                    self.algo_generator = None
            
            #Fill background
            self.screen.fill((50,50,50))

            #Update manager
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)  
            
            #Blit animation surface
            self.screen.blit(self.anim_canvas.surface, self.anim_canvas_pos)
            self.delay(self.algo_speed)
            self.update()

        pg.quit()

    def update(self):
        pg.display.flip()
    
    def delay(self, time):
        pg.time.delay(time)

class Button:
    def __init__(self, pos, size, label, manager, vis, container=None):
        self.pos = pos
        self.size = size
        self.label = label
        self.vis = vis
        self.element = pg_gui.elements.UIButton(
            relative_rect= pg.Rect(self.pos, self.size),
            text= f"{self.label}",
            manager= manager,
            visible= self.vis,
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
    def __init__(self):
        pass

class TextWindow:
    def __init__(self):
        pass

if __name__ == "__main__":
    anim_surface = AnimationCanvas()
    app = GuiManager(anim_surface)
    app.run()