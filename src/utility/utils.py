import random
import yaml
import os
import re
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

class Parameters:
    """
    This class creates the values that getfed to the algorithms.
    """

    def __init__(self, size):
        """
        Initializes parameters by size.
        """
        #Initialize size and speed attributes
        self.size = size

    def create_values(self):
        """
        Creates random values beween 1 and 100 according to size attribute.
        """
        #Create values attribute
        self.values = random.sample(range(1, 101), self.size)
        return self.values

    def create_value_to_find(self):
        """
        Creates the target value for basic search algorithms.
        """
        idx = random.randint(0, self.size-1)
        value_to_find = self.values[idx]
        return value_to_find


class Board:
    """
    Default data structure for the grid (2d list) that is used to demonstrate
    how graph traversal algorithms work.
    """

    def __init__(self, surface_size, rect_amount):
        """
        Initiates a 2d list (grid) based on rectangle amounts.
        Fills the grid with values of '1'.
        """
        #Create a 2d matrix that represents a checkerboard

        self.rows = rect_amount[1]
        self.cols = rect_amount[0]

        self.rect_size = surface_size[0] // rect_amount[0]
        
        #Initialize empty list
        self.raster = []

        #2d list filled with 0s to represent checkerboard structure
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(1)
            self.raster.append(row)

    def reset(self):
        """
        Resets the grid values to '1'.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                self.raster[i][j] = 1


class FileReader:
    """
    Used to load and read from yaml files that hold text which is displayed on the app.
    It also formats certain text that gets displayed as code.
    """
    
    def __init__(self, directory, filename):
        """
        Initiates the FileReader class.
        """
        file_path = os.path.join(directory, "gui", filename)

        with open(file_path, "r") as file:
            self.info_texts = yaml.safe_load(file)

    def get_text(self, algorithm):
        """
        Gets the info text for the input algorithm based on its name.
        Sets a default font, color and size.

        Parameters
        ----------

        algorithm : string
            currently selected algorithm name
        """
        info_text = self.info_texts[f"{algorithm}"]["definition"]   
        
        default_font = f"<font face='verdana' color='#ffffff' size=4>{info_text}</font>" 

        return default_font
    
    def get_code_text(self, algorithm):
        """
        Gets the code text for the input algorithm based on its name.
        Sets a default font, color and size. Uses pygments to colorise
        the text so that it looks like actual codein editor.

        Parameters
        ----------

        algorithm : string
            currently selected algorithm name
        """
        code_text = self.info_texts[f"{algorithm}"]["definition"]

        format = HtmlFormatter(noclasses=True, style="monokai")
        code_text = highlight(code_text, PythonLexer(), format)

        code_text = re.sub(r'<span style="color:\s*(#[0-9a-fA-F]{6})">(.*?)</span>', 
                           r'<font color="\1">\2</font>',
                           code_text
                           )

        default_font = f"<font face='verdana' color='#ffffff' size=4>{code_text}</font>"

        return default_font