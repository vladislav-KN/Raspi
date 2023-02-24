import json

from pydantic import BaseModel


class MqttData(BaseModel):
    rasp_id: str
    code: str


    def to_json(self):
        return json.dumps(self)
