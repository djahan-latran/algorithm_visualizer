"""A file loader to load and read json data"""
import json

class FileReader:
    def __init__(self):
        with open("info_texts.json", "r") as file:
            self.info_texts = json.load(file)

    def get_text(self, algorithm):
        return self.info_texts[f"{algorithm}"]["definition"]