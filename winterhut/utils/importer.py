import json


class Importer:

    def __init__(self, file):
        self.file = file

    def load_file_content(self):
        file_json = json.load(self.file)
        return file_json
