"""A class to graphically animate how certain algorithms work by using pygames drawing methods"""
import pygame as pg


class AnimationCanvas:
    def __init__(self):
        #Background color
        self.background_cl = (82, 82, 82)

        #Colors for different value states
        self.def_bar_cl = (50, 50, 50)
        self.curr_bar_cl = (120, 120, 120)
        self.curr_rect_cl = (95, 245, 250)
        self.sortd_bar_cl = (50, 255, 50)
        self.red_bar_cl = (200, 50, 50)

    def create_surface(self, surface_size):
        self.surface = pg.Surface(surface_size)

    # def draw_bar_graphs(self):
    #     #fill the surface with bg color
    #     screen.fill(BG_COLOR)

    #     draw_title(algorithm= algo_name, screen= screen)

    #     #calc the spacing between bar graphs and their size
    #     spaces = (len(nums) * 2) - 1
    #     bar_width = int((SCREEN_WIDTH - (PADDING * 2)) / spaces) 

    #     #set font size relative to bar_width
    #     main_font = pg.font.SysFont("Arial", bar_width-8, bold=True)

    #     #calc bar height and coordinates and draw the rectangles
    #     for i, value in enumerate(nums):
    #         bar_height = value * 3
    #         x_coord = i * bar_width * 2 + PADDING
    #         y_coord = Y_COORD_BAR - bar_height
    #         bar_rect = pg.Rect(x_coord, y_coord, bar_width, bar_height)

    #         if drawing_info["green"] and value in drawing_info["green"]:
    #             pg.draw.rect(screen, SORTD_BAR_COLOR, bar_rect, border_radius= BAR_BEVEL)
    #         elif drawing_info["red"] and value in drawing_info["red"]:
    #             pg.draw.rect(screen, RED_BAR_COLOR, bar_rect, border_radius= BAR_BEVEL)
    #         elif drawing_info["lightgrey"] and value in drawing_info["lightgrey"]:
    #             pg.draw.rect(screen, CURR_BAR_COLOR, bar_rect, border_radius= BAR_BEVEL)
    #         else:
    #             pg.draw.rect(screen, DEF_BAR_COLOR, bar_rect, border_radius= BAR_BEVEL)

    #         value_label = main_font.render(f"{value}", True, LABEL_COLOR)
    #         value_rect = value_label.get_rect()
    #         value_rect.midbottom = (x_coord + bar_width/2, Y_COORD_BAR)
    #         screen.blit(value_label, value_rect)

    #     pg.time.wait(SPEED)
    #     pg.display.update()

    def draw_board(self):
        pass
    