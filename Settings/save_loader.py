import os

import json

class SL_functions:
    def __init__(self, file):
        self.file = file

    def load_from_file(self):
        with open(self.file, 'r') as j:
            return json.loads(j.read())

    def save_to_file(self, data):
        with open(self.file, 'w') as f:
            json.dump(data.__dict__, f)
    def enshure_file_created(self):
        return os.path.isfile(self.file)

