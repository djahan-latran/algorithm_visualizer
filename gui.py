import pygame as pg
import pygame_gui as pg_gui
from visualizer import AnimationCanvas
from algorithms import BubbleSort, SelectionSort, InsertionSort, LinearSearch, BinarySearch, Bfs, Dfs
from inputs import Parameters, Board
import time

class GuiManager:
    def __init__(self, anim_canvas):
        #Main window size
        self.screen_size = (1200, 700)

        #Animation window instance
        self.anim_canvas = anim_canvas
        #Amount of rectangles cols and rows
        self.rect_amount = (34, 20)

        #Animation window position, size and color
        self.anim_canvas_pos = (185, 50)
        self.anim_canvas_size = (680, 400)

        #Theme colours
        self.teal_cl = (58, 186, 249)
        self.white_cl = (255, 255, 255)

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
        self.manager.ui_theme.load_theme("themes.json")

        #Ui layout except buttons, animation surface and panels
        header_rect = pg.Rect((0,0), (self.screen_size[0], 50))
        info_circle_dim = 45
        info_circle_rect = pg.Rect((1035 - info_circle_dim / 2, 360 - info_circle_dim / 2), (info_circle_dim, info_circle_dim))

        #Create basic-sorts scroll container and scroll panel inside
        basic_sorts_scroll_cont = ScrollContainer(pos= (0, 50), size=(200, 200), manager= self.manager) #Actual visible size of container
        basic_sorts_scroll_panel = Panel(pos= (0, 0), size= (180, 1200), manager= self.manager, container= basic_sorts_scroll_cont.element) #Size of scrollable area

        #Create basic sorts category
        basic_sorts = Button(pos= (0, 0), size= (180, 45), label= "Basic Sorting", manager= self.manager, vis= 1, id= "#header_button",container= basic_sorts_scroll_panel.element)
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

        basic_search = Button(pos=(0, 0), size=(180, 45), label= "Basic Search", manager= self.manager, vis= 1, id= "#header_button", container= basic_search_scroll_panel.element)
        basic_search.element.disable()

        basic_search_btn_amount = 1
        
        linear_search_btn = Button(pos=(0, 45), size=(180, 45), label= "Linear Search", manager= self.manager, vis= 1, container= basic_search_scroll_panel.element)
        basic_search_btn_amount += 1
        
        binary_search_btn = Button(pos=(0, 90), size=(180, 45), label= "Binary Search", manager= self.manager, vis= 1, container= basic_search_scroll_panel.element)
        basic_search_btn_amount += 1

        basic_search_scroll_cont.element.set_scrollable_area_dimensions((180, 45 * basic_search_btn_amount))


        #Create pathfinding scroll container and scroll panel inside
        pathfinding_scroll_cont = ScrollContainer(pos= (0, 365), size=(200, 240), manager= self.manager) #Actual visible size of container
        pathfinding_scroll_panel = Panel(pos= (0, 0), size= (180, 1200), manager= self.manager, container= pathfinding_scroll_cont.element) #Size of scrollable area

        pathfinding = Button(pos=(0, 0), size=(180, 45), label= "Pathfinding", manager= self.manager, vis= 1, id= "#header_button", container= pathfinding_scroll_panel.element)
        pathfinding.element.disable()

        pathfinding_btn_amount = 1

        bfs_btn = Button(pos=(0, 45), size= (180, 45), label= "Breadth-First-Search", manager= self.manager, vis= 1, container= pathfinding_scroll_panel.element)
        pathfinding_btn_amount += 1

        dfs_btn = Button(pos=(0, 45*pathfinding_btn_amount), size= (180, 45), label= "Depth-First-Search", manager= self.manager, vis= 1, container= pathfinding_scroll_panel.element)
        pathfinding_btn_amount += 1

        astar_btn = Button(pos=(0, 45*pathfinding_btn_amount), size= (180, 45), label= "A*Search", manager= self.manager, vis= 1, container= pathfinding_scroll_panel.element)
        pathfinding_btn_amount += 1

        dijkstra_btn = Button(pos=(0, 45*pathfinding_btn_amount), size= (180, 45), label= "Dijkstra's", manager= self.manager, vis= 1, container= pathfinding_scroll_panel.element)
        pathfinding_btn_amount += 1

        pathfinding_scroll_cont.element.set_scrollable_area_dimensions((180, 45 * pathfinding_btn_amount))

        #Create play button
        play_btn = Button(pos= (910, 280), size= (65, 25), label= "Play", manager= self.manager, vis= 0, id= "#control_button")
        
        #Create reset button
        reset_btn = Button(pos= (1000, 280), size= (65, 25), label= "Reset", manager= self.manager, vis= 0, id= "#control_button")

        #Create pause button
        pause_btn = Button(pos= (1090, 280), size= (65, 25), label= "Pause", manager= self.manager, vis= 0, id= "#control_button")

        #Create target button
        set_target_btn = Button(pos= (910, 120), size= (85, 25), label= "Set target", manager= self.manager, vis= 0, id= "#control_button")
        
        #Create obstacle button
        set_obstacle_btn = Button(pos= (1055, 120), size= (100, 25), label= "Set Obstacle", manager= self.manager, vis= 0, id= "#control_button")

        #Create sliders
        size_slider_rect = pg.Rect((910,130), (245, 25))
        size_slider = pg_gui.elements.UIHorizontalSlider(size_slider_rect, 20, (10, 100), self.manager, click_increment= 2)
        size_slider.hide()

        speed_slider_rect = pg.Rect((910,200), (245, 25))
        speed_slider = pg_gui.elements.UIHorizontalSlider(speed_slider_rect, 50, (1, 100), self.manager, click_increment= 2)
        speed_slider.hide()

        #Create Info text box
        bs_info_box_rect = pg.Rect((868,360),(334, 340))
        bs_info_box = pg_gui.elements.UITextBox("\n<font face='verdana' color='#ffffff' size=3.5><u><b>Complexity</b></u>\nBest Case (already sorted): <b>O(n)</b>\nAverage & Worst Case: <b>O(n²)</b>"
        "\n\n<u><b>Definition</b></u>\nBubble Sort is a simple sorting algorithm that repeatedly compares adjacent elements and swaps them if they are in the wrong order. "
        "This process continues until no more swaps are needed, meaning the list is fully sorted. "
        "With each pass, the largest value 'bubbles up' to its correct position on the right. "
        "The algorithm then repeats for the remaining unsorted elements until the entire list is ordered. "
        "Due to its inefficient time complexity of <b>O(n²)</b>, Bubble Sort is primarily used for educational purposes rather than practical applications.</font>", bs_info_box_rect, object_id="#info_text_box")
        bs_info_box.hide()

        bs_code_box_rect = pg.Rect((self.anim_canvas_pos[0], self.anim_canvas_pos[1] + self.anim_canvas_size[1] + 5), (self.anim_canvas_size[0], 220))
        bs_code_box = pg_gui.elements.UITextBox("Testing", bs_code_box_rect, object_id= "#info_text_box")
        bs_code_box.hide()

        #Create fonts and texts
        title_font = pg.font.SysFont("Verdana", 27)
        headline_font = pg.font.SysFont("Verdana", 20)
        slider_font = pg.font.SysFont("Verdana", 12)
        info_icon_font = pg.font.SysFont("timesnewroman", 30, True)

        app_name = title_font.render("AlgoLab", True, self.white_cl) #title
        app_name_rect = app_name.get_rect()
        app_name_rect.bottomleft = (40, 40)
        
        settings_text = headline_font.render("Settings", True, self.white_cl)
        settings_text_rect = settings_text.get_rect()
        settings_text_rect.bottomleft = (880, 40)

        size_slider_title = slider_font.render("Adjust Size", True, self.white_cl)
        size_slider_title_rect = size_slider_title.get_rect()
        size_slider_title_rect.bottomleft = (915, 125)

        speed_slider_title = slider_font.render("Adjust Speed", True, self.white_cl)
        speed_slider_title_rect = speed_slider_title.get_rect()
        speed_slider_title_rect.bottomleft = (915, 195)

        letter_i = info_icon_font.render("i", True, self.white_cl)
        letter_i_rect = letter_i.get_rect()
        letter_i_rect.center = (1035-1,360-1) #make variables then subtract 1

        #First no algorithm is selected, therefore no control-buttons show up
        selected_algo = None

        #Create surface attribute of the animation canvas
        self.anim_canvas.create_surface(self.anim_canvas_size)
        
        #Initialize a value to find by search algorithms
        self.value_to_find = None
        #Initialize a generator for the algorithm steps
        self.algo_generator = None
        #Break condition for App running
        self.running = True
        #Yet no algo started
        self.algo_running = False
        #Target for pathfinding not selected yet
        target_sel_phase = False
        #Obstacles for pathfinding not selected yet
        obstacle_sel_phase = False
        #Initialize algorithm categorie
        curr_algo_cat = None

        surface_update_interval = 1/50
        gui_update_interval = 1/60
        surface_updated = time.time()
        gui_updated = time.time()

        checkerboard = None
        
        #Application loop
        while self.running:

            time_delta = clock.tick(60) / 1000
            
            current_time = time.time()

            #Update interval for GUI (fps)
            if current_time - gui_updated >= gui_update_interval:
                gui_updated = current_time

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False

                    #Process events
                    self.manager.process_events(event)

                    #Handle events
                    if event.type == pg_gui.UI_BUTTON_PRESSED: 

                        
                        #Handle Linear Search button
                        if event.ui_element == linear_search_btn.element:
                            #If an algo is running and another algo button is pressed it stops running
                            self.algo_running = False

                            #Control buttons and parameter sliders get shown if not already
                            if not play_btn.vis:
                                play_btn.element.show()
                                reset_btn.element.show()
                                pause_btn.element.show()
                                size_slider.show()
                                size_slider.enable()
                                speed_slider.show()
                                speed_slider.enable()
                                
                                set_target_btn.element.hide()
                                set_obstacle_btn.element.hide()

                            #If there was a checkerboard drawn before set it to None
                            #so the Reset button won't trigger drawing a new one
                            if checkerboard:
                                checkerboard = None

                            #Save what algo was pressed so the play button knows what algo to run
                            selected_algo = "Linear Search"
                            curr_algo_cat = "Searching"

                            #Set default values
                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()
                            self.value_to_find = parameters.create_value_to_find()

                            #Show default values
                            self.anim_canvas.draw_bar_graphs(self.values)
                            
                            #Create the generator of the chosen algo
                            lin_search = LinearSearch(self.values, self.anim_canvas, self.value_to_find)
                            self.algo_generator = lin_search.run()

                        elif event.ui_element == binary_search_btn.element:
                            self.algo_running = False

                            if not play_btn.vis:
                                play_btn.element.show()
                                reset_btn.element.show()
                                pause_btn.element.show()
                                size_slider.show()
                                size_slider.enable()
                                speed_slider.show()
                                speed_slider.enable()
                                
                                set_target_btn.element.hide()
                                set_obstacle_btn.element.hide()

                            if checkerboard:
                                checkerboard = None

                            selected_algo = "Binary Search"
                            curr_algo_cat = "Searching"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()
                            self.value_to_find = parameters.create_value_to_find()
                            self.values.sort()

                            self.anim_canvas.draw_bar_graphs(self.values)
                            
                            bin_search = BinarySearch(self.values, self.anim_canvas, self.value_to_find)
                            self.algo_generator = bin_search.run(self.values)

                        #Handle Bubble Sort button
                        elif event.ui_element == bubb_sort_btn.element:
                            self.algo_running = False

                            bubb_sort_btn.element.select()
                            sel_sort_btn.element.unselect()
                            in_sort_btn.element.unselect()

                            if not play_btn.vis:
                                play_btn.element.show()
                                reset_btn.element.show()
                                pause_btn.element.show()
                                size_slider.show()
                                size_slider.enable()
                                speed_slider.show()
                                speed_slider.enable()
                                bs_info_box.show()
                                bs_code_box.show()
                                set_target_btn.element.hide()
                                set_obstacle_btn.element.hide()
                            
                            if checkerboard:
                                checkerboard = None

                            selected_algo = "Bubble Sort"
                            curr_algo_cat = "Sorting"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()
                            
                            self.anim_canvas.draw_bar_graphs(self.values)
                            
                            #If another algorithm was playing before and got paused
                            #this is going to reset the values if another algorithm gets chosen
                            bubble_sort = BubbleSort(self.values, self.anim_canvas)
                            self.algo_generator = bubble_sort.run()

                        #Handle Selection Sort button
                        elif event.ui_element == sel_sort_btn.element:
                            self.algo_running = False

                            sel_sort_btn.element.select()
                            bubb_sort_btn.element.unselect()
                            in_sort_btn.element.unselect()

                            if not play_btn.vis:
                                play_btn.element.show()
                                reset_btn.element.show()
                                pause_btn.element.show()
                                size_slider.show()
                                size_slider.enable()
                                speed_slider.show()
                                speed_slider.enable()
                                
                                set_target_btn.element.hide()
                                set_obstacle_btn.element.hide()

                            if checkerboard:
                                checkerboard = None

                            selected_algo = "Selection Sort"
                            curr_algo_cat = "Sorting"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()

                            self.anim_canvas.draw_bar_graphs(self.values)

                            #If another algorithm was playing before and got paused
                            #this is going to reset the values if another algorithm gets chosen
                            sel_sort = SelectionSort(self.values, self.anim_canvas)
                            self.algo_generator = sel_sort.run()

                        #Handle Insertion Sort button
                        elif event.ui_element == in_sort_btn.element:
                            self.algo_running = False

                            in_sort_btn.element.select()
                            bubb_sort_btn.element.unselect()
                            sel_sort_btn.element.unselect()

                            if not play_btn.vis:
                                play_btn.element.show()
                                reset_btn.element.show()
                                pause_btn.element.show()
                                size_slider.show()
                                size_slider.enable()
                                speed_slider.show()
                                speed_slider.enable()
                                
                                set_target_btn.element.hide()
                                set_obstacle_btn.element.hide()

                            if checkerboard:
                                checkerboard = None

                            selected_algo = "Insertion Sort"
                            curr_algo_cat = "Sorting"

                            parameters = Parameters(size= 20)
                            self.values = parameters.create_values()

                            self.anim_canvas.draw_bar_graphs(self.values)

                            #If another algorithm was playing before and got paused
                            #this is going to reset the values if another algorithm gets chosen
                            in_sort = InsertionSort(self.values, self.anim_canvas)
                            self.algo_generator = in_sort.run()

                        #Handle Breadth-First-Search button
                        elif event.ui_element == bfs_btn.element:
                            obstacle_selected = False
                            target_selected = False
                            self.algo_running = False
                            size_slider.hide()

                            if not play_btn.vis:
                                play_btn.element.show()
                                reset_btn.element.show()
                                pause_btn.element.show()
                                speed_slider.show()
                                set_target_btn.element.show()
                                set_obstacle_btn.element.show()

                            selected_algo = "Breadth-First-Search"
                            curr_algo_cat = "Pathfinding"

                            checkerboard = Board(self.anim_canvas_size, self.rect_amount)

                            self.anim_canvas.draw_board(checkerboard)

                            bfs = Bfs(self.anim_canvas, checkerboard)
                            self.algo_generator = bfs.run()

                        #Handle Depth-First-Search button
                        elif event.ui_element == dfs_btn.element:
                            obstacle_selected = False
                            target_selected = False
                            self.algo_running = False
                            size_slider.hide()

                            if not play_btn.vis:
                                play_btn.element.show()
                                reset_btn.element.show()
                                pause_btn.element.show()
                                speed_slider.show()
                                set_target_btn.element.show()
                                set_obstacle_btn.element.show()

                            selected_algo = "Depth-First-Search"
                            curr_algo_cat = "Pathfinding"

                            checkerboard = Board(self.anim_canvas_size, self.rect_amount)

                            self.anim_canvas.draw_board(checkerboard)

                            dfs = Dfs(self.anim_canvas, checkerboard)
                            self.algo_generator = dfs.run(0,0)

                        #Handle Play button
                        elif event.ui_element == play_btn.element:
                            
                            if selected_algo == "Bubble Sort":
                                if not self.algo_generator:
                                    bubble_sort = BubbleSort(self.values, self.anim_canvas)
                                    self.algo_generator = bubble_sort.run()
                                self.algo_running = True
                                size_slider.disable()

                            elif selected_algo == "Selection Sort":
                                if not self.algo_generator:
                                    sel_sort = SelectionSort(self.values, self.anim_canvas)
                                    self.algo_generator = sel_sort.run()
                                self.algo_running = True
                                size_slider.disable()

                            elif selected_algo == "Insertion Sort":
                                if not self.algo_generator:
                                    in_sort = InsertionSort(self.values, self.anim_canvas)
                                    self.algo_generator = in_sort.run()
                                self.algo_running = True
                                size_slider.disable()

                            elif selected_algo == "Linear Search":
                                if not self.algo_generator:
                                    lin_search = LinearSearch(self.values, self.anim_canvas, self.value_to_find)
                                    self.algo_generator = lin_search.run()
                                self.algo_running = True
                                size_slider.disable()

                            elif selected_algo == "Binary Search":
                                if not self.algo_generator:
                                    bin_search = BinarySearch(self.values, self.anim_canvas, self.value_to_find)
                                    self.algo_generator = bin_search.run(self.values)
                                self.algo_running = True
                                size_slider.disable()

                            elif selected_algo == "Breadth-First-Search":
                                if not self.algo_generator:
                                    bfs = Bfs(self.anim_canvas, checkerboard)
                                    self.algo_generator = bfs.run()
                                self.algo_running = True

                            elif selected_algo == "Depth-First-Search":
                                if not self.algo_generator:
                                    dfs = Dfs(self.anim_canvas, checkerboard)
                                    self.algo_generator = dfs.run(0,0)
                                self.algo_running = True

                        #Handle Reset button
                        elif event.ui_element == reset_btn.element:
                            self.algo_running = False
                            self.algo_generator = None
                            
                            if checkerboard:
                                target_selected = False
                                checkerboard = Board(self.anim_canvas_size, self.rect_amount)
                                self.anim_canvas.draw_board(checkerboard)

                            else:
                                self.values = parameters.create_values()

                                if self.value_to_find:
                                    self.value_to_find = parameters.create_value_to_find()
                                    
                                if selected_algo == "Binary Search":
                                    self.values.sort()

                                size_slider.enable()
                                self.anim_canvas.draw_bar_graphs(self.values)

                        #Handle Pause button
                        elif event.ui_element == pause_btn.element:
                            self.algo_running = False

                        #Handle Set Target button
                        elif event.ui_element == set_target_btn.element:
                            if target_selected == False:
                                target_sel_phase = True
                            if obstacle_sel_phase:
                                obstacle_sel_phase = False
                        
                        #Handle Set Obstacle button
                        elif event.ui_element == set_obstacle_btn.element:
                            if obstacle_sel_phase == True:
                                obstacle_sel_phase = False
                                obstacle_selected = True
                            else:
                                obstacle_sel_phase = True
                        

                    #Handle sliders
                    if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        if event.ui_element == speed_slider:
                            surface_update_interval = 1 / speed_slider.get_current_value()

                        if event.ui_element == size_slider:
                            new_size = size_slider.get_current_value()
                            parameters.size = new_size
                            self.values = parameters.create_values()
                            if selected_algo == "Binary Search":
                                self.values.sort()
                            self.anim_canvas.draw_bar_graphs(self.values)

                if curr_algo_cat == "Pathfinding" and self.algo_running == False:
                    
                    mouse_pos = pg.mouse.get_pos()
                    mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
                    
                    if pg.mouse.get_pressed()[0] and self.anim_canvas_pos[0] < mouse_x < self.anim_canvas_pos[0] + self.anim_canvas_size[0] and self.anim_canvas_pos[1] < mouse_y < self.anim_canvas_pos[1] + self.anim_canvas_size[1]:
                        canvas_x, canvas_y = mouse_x - self.anim_canvas_pos[0], mouse_y - self.anim_canvas_pos[1]
                        rect_no_x = canvas_x // checkerboard.rect_size
                        rect_no_y = canvas_y // checkerboard.rect_size

                        if target_sel_phase:
                            checkerboard.raster[rect_no_y][rect_no_x] = 2
                            self.anim_canvas.draw_board(checkerboard)
                            target_selected = True
                            target_sel_phase = False

                        elif obstacle_sel_phase:
                            if checkerboard.raster[rect_no_y][rect_no_x] != 2:
                                checkerboard.raster[rect_no_y][rect_no_x] = 1
                            self.anim_canvas.draw_board(checkerboard)
                        else:
                            continue


            if self.algo_running and current_time - surface_updated >= surface_update_interval:
                try:
                    next(self.algo_generator)
                    surface_updated = current_time
                except StopIteration as e:
                    if e.value == True:
                        print("FOUND IT")
                    self.algo_running = False
                    speed_slider.set_current_value(1/20)
                    self.algo_generator = None
            
            #Fill background
            self.screen.fill((50,50,50))

            #Update manager
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)  
            
            #Blit animation surface
            self.screen.blit(self.anim_canvas.surface, self.anim_canvas_pos)
    
            pg.draw.rect(self.screen, (20,20,20), header_rect) #make color a variable
            
            #Blit texts
            self.screen.blit(app_name, app_name_rect)

            if selected_algo:
                pg.draw.line(self.screen, self.teal_cl, (870,360), (1200,360), 5)
                pg.draw.ellipse(self.screen, self.teal_cl, info_circle_rect)

                cat_name = headline_font.render(f"Selected Algorithm:   {selected_algo}", True, self.white_cl)
                cat_name_rect = cat_name.get_rect()
                cat_name_rect.bottomleft = (200, 40)
                
                self.screen.blit(letter_i, letter_i_rect)
                self.screen.blit(cat_name, cat_name_rect)
                self.screen.blit(settings_text, settings_text_rect)
                self.screen.blit(speed_slider_title, speed_slider_title_rect)
                if curr_algo_cat != "Pathfinding":
                    self.screen.blit(size_slider_title, size_slider_title_rect)
            
            self.update()

        pg.quit()

    def update(self):
        pg.display.flip()
    
    def delay(self, time):
        pg.time.delay(time)

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
    def __init__(self):
        pass

class TextWindow:
    def __init__(self):
        pass


if __name__ == "__main__":
    anim_surface = AnimationCanvas()
    app = GuiManager(anim_surface)
    app.run()