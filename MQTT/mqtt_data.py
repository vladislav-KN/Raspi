import json


class mqtt_data:
    def __init__(self, id,code):
        self.id = id
        self.code = code
    def to_json(self):
        return json.dumps(self)