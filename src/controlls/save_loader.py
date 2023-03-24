import os

import json


class SaveLoad:
    def __init__(self, file:str):
        self.file = file

    def load_from_file(self):
        with open(os.getcwd()+self.file, 'r', encoding='utf-8') as j:
            k = json.loads(j.read())
            return k

    def save_to_file(self, data):
        with open(os.getcwd()+self.file, 'w', encoding='utf-8') as f:
            try:
                json.dump(data.__dict__, f)
            except:
                json.dump(data, f)

    def enshure_file_created(self):
        return os.path.isfile(self.file)
