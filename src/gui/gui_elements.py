"""This Module serves as a wrapper for basic pygame_gui elements 
that will be used in the gui_panels.
"""

import pygame_gui as pg_gui
import pygame as pg


class Button:
    """
    This class wraps and creates a pygame_gui UIButton element.
    """
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
    """
    This class wraps and creates a pygame_gui UIScrollingContainer element.
    """
    def __init__(self, pos, size, manager):
        self.pos = pos
        self.size = size
        self.manager = manager
        self.element = pg_gui.elements.UIScrollingContainer(
            relative_rect= pg.Rect(self.pos, self.size),
            manager= self.manager
        )


class Panel:
    """
    This class wraps and creates a pygame_gui UIPanel element.
    """
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
    """
    This class wraps and creates a pygame_gui UIHorizontalSlider element.
    """
    def __init__(self, pos, size, manager, range, start_val, click_inc):
        self.rect = pg.Rect(pos, size)
        self.element = pg_gui.elements.UIHorizontalSlider(
            self.rect, 
            start_val, 
            range, 
            manager, 
            click_increment= click_inc
        )


class TextWindow:
    """
    This class wraps and creates a pygame_gui UITextBox element.
    """
    def __init__(self, pos, size, manager, text):
        self.pos = pos
        self.size = size
        box_rect = pg.Rect(self.pos, self.size)
        self.text = text
        self.element = pg_gui.elements.UITextBox(self.text, 
                                                 box_rect, 
                                                 manager, 
                                                 object_id="#info_text_box"
                                                 )