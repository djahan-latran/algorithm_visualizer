"""A class to graphically animate how certain algorithms work by using pygames drawing methods"""
import pygame as pg


class AnimationCanvas:
    def __init__(self):
        #Background color
        self.background_cl = (82, 82, 82)

        #Colors for different value states (bar graph)
        self.def_bar_cl = (50, 50, 50)
        self.curr_bar_cl = (120, 120, 120)
        self.sortd_bar_cl = (50, 255, 50)
        self.red_bar_cl = (200, 50, 50)

        #Colors for different rectangles (checkerboard)
        self.def_rect_bord_cl = (50, 50, 50)
        self.def_rect_cl = (70, 70, 70)
        self.curr_rect_cl = (120, 120, 120)
        self.obstacle_rect_cl = (200, 50, 50)
        self.target_rect_cl = (50, 255, 50)

        #Label color
        self.label_color = (250, 250, 250)

        #Distance from bar rect to label
        self.label_pad = 3

        #Distance from surface sides
        self.side_pad = 0
        
        #Bevel on corners of the bars
        self.bar_bevel = 2

        #Size of each rectangle in checkerboard
        self.rect_size = 16

    def create_surface(self, surface_size):
        self.surface_size = surface_size
        self.surface = pg.Surface(self.surface_size)
        self.side_pad = int(self.surface_size[0] / 32)

    def draw_bar_graphs(self, values, draw_info=None):
        #fill the surface with bg color
        self.surface.fill(self.background_cl)

        #draw_title(algorithm= algo_name, screen= screen)

        #calc the spacing between bar graphs and their size
        spaces = (len(values) * 2) - 1
        bar_width = int((self.surface_size[0] - (self.side_pad * 2)) / spaces) 

        #set font size relative to bar_width
        main_font = pg.font.SysFont("Arial", bar_width - self.label_pad, bold=True)

        #calc bar height and coordinates and draw the rectangles
        for i, value in enumerate(values):
            bar_height = value * 3
            x_coord = i * bar_width * 2 + self.side_pad
            y_coord = self.surface_size[1] - bar_height
            bar_rect = pg.Rect(x_coord, y_coord, bar_width, bar_height)

            if draw_info and value in draw_info["positive"]:
                pg.draw.rect(self.surface, self.sortd_bar_cl, bar_rect, border_radius= self.bar_bevel)
            elif draw_info and value in draw_info["negative"]:
                pg.draw.rect(self.surface, self.red_bar_cl, bar_rect, border_radius= self.bar_bevel)
            elif draw_info and value in draw_info["neutral"]:
                pg.draw.rect(self.surface, self.curr_bar_cl, bar_rect, border_radius= self.bar_bevel)
            else:
                pg.draw.rect(self.surface, self.def_bar_cl, bar_rect, border_radius= self.bar_bevel)
            
            #blit the value on bar graph
            value_label = main_font.render(f"{value}", True, self.label_color)
            value_rect = value_label.get_rect()
            value_rect.midbottom = (x_coord + bar_width/2, y_coord)
            self.surface.blit(value_label, value_rect)
    
    def create_def_board(self):
        #Create a 2d matrix that represents a checkerboard

        self.checker_rows = self.surface_size[1] // self.rect_size
        self.checker_cols = self.surface_size[0] // self.rect_size

        #Initialze empty list
        self.board = []

        #2d list filled with 0s to represent checkerboard structure
        for _ in range(self.checker_rows):
            row = []
            for _ in range(self.checker_cols):
                row.append(0)
            self.board.append(row)

        return self.board
    
    def draw_board(self, value_info):
        #Draw the checkerboard
        
        x_coord = 0
        y_coord = 0

        #Collect the changes
        changes = []
        end_pos = (self.checker_rows, self.checker_cols)


        for i in range(self.checker_rows):
            for j in range(self.checker_cols):
                sq_rect = pg.Rect(x_coord, y_coord, self.rect_size, self.rect_size)
                if self.board[i][j] == 1:
                    pg.draw.rect(self.surface, self.obstacle_rect_cl, sq_rect)
                    changes.append(sq_rect)
                elif end_pos and (i, j) == end_pos:
                    pg.draw.rect(self.surface, self.target_rect_cl, sq_rect)
                    changes.append(sq_rect)
                elif current and (i, j) == current:
                    pg.draw.rect(self.surface, self.curr_rect_cl, sq_rect, 3)
                    changes.append(sq_rect)
                elif visited and (i, j) in visited:
                    pg.draw.rect(self.surface, self.curr_rect_cl, sq_rect)
                    pg.draw.rect(self.surface, self.def_rect_cl, sq_rect, 1)
                    changes.append(sq_rect)
                else:
                    pg.draw.rect(self.surface, self.def_rect_cl, sq_rect)
                    pg.draw.rect(self.surface, self.def_rect_bord_cl, sq_rect, 1)
                    changes.append(sq_rect)

                x_coord += self.rect_size

            y_coord += self.rect_size
            x_coord = 0 