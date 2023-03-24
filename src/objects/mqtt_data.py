import json

from pydantic import BaseModel


class MqttData(BaseModel):
    rasp_id: str
    code: str

    def to_json_str(self) -> str:
        return json.dumps(self)
