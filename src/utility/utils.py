import random
import yaml
import os
import re
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

class Parameters:

    def __init__(self, size):
        #Initialize size and speed attributes
        self.size = size

    def create_values(self):
        #Create values attribute
        self.values = random.sample(range(1, 101), self.size)
        return self.values

    def create_value_to_find(self):
        idx = random.randint(0, self.size-1)
        value_to_find = self.values[idx]
        return value_to_find


class Board:

    def __init__(self, surface_size, rect_amount):
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
        for i in range(self.rows):
            for j in range(self.cols):
                self.raster[i][j] = 1


class FileReader:
    
    def __init__(self, directory, filename):
        file_path = os.path.join(directory, "gui", filename)

        with open(file_path, "r") as file:
            self.info_texts = yaml.safe_load(file)

    def get_text(self, algorithm):
        info_text = self.info_texts[f"{algorithm}"]["definition"]   
        
        default_font = f"<font face='verdana' color='#ffffff' size=4>{info_text}</font>" 

        return default_font
    
    def get_code_text(self,algorithm):
        code_text = self.info_texts[f"{algorithm}"]["definition"]

        format = HtmlFormatter(noclasses=True, style="monokai")
        code_text = highlight(code_text, PythonLexer(), format)

        code_text = re.sub(r'<span style="color:\s*(#[0-9a-fA-F]{6})">(.*?)</span>', 
                           r'<font color="\1">\2</font>',
                           code_text
                           )

        default_font = f"<font face='verdana' color='#ffffff' size=4>{code_text}</font>"

        return default_font