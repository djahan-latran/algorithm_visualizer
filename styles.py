"""Styling like colors and fonts"""
import pygame as pg


class AppColours:

    def __init__(self):
        #Colors dictionary
        self.values = {"accent_cl":(58, 186, 249), 
                        "text_cl":(255, 255, 255),
                        "header_cl": (20, 20, 20),
                        "main_bg_cl": (50, 50, 50)
                        }        


class AppFonts:

    def __init__(self):
        #Setup fonts
        self.title = pg.font.SysFont("Verdana", 27)
        self.headline = pg.font.SysFont("Verdana", 20)
        self.slider = pg.font.SysFont("Verdana", 12)
        self.info_icon = pg.font.SysFont("timesnewroman", 30, True)