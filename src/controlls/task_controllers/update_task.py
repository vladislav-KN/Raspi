import json
import time
from abc import abstractmethod

import requests

from settings.settings import ID_RASPI
from src.controlls.save_loader import SaveLoad


class Updator:

    def __init__(self, dict_param: dict, edited: bool = False):
        self.param = dict_param
        self.edited = edited

    def check_update(self):
        while True:
            try:
                req = requests.request('GET', self.param["to"] + f"/update?id={ID_RASPI}")
                if req.status_code < 300:
                    update_info = json.loads(req.text)
                    if update_info[self.param["updt"]]:
                        req = requests.request('GET', self.param["to"] + f"/{self.param['controller']}?id={ID_RASPI}")
                        if req.status_code < 300:
                            data = json.loads(req.text)
                            Updator.save_updates(self.param["file"], data)
                            self.edited = True
                            time.sleep(self.param["sleep_if_exist"])
                        else:
                            time.sleep(self.param["sleep_if_not_exist"])
                    else:
                        time.sleep(self.param["sleep_if_not_updt"])
            except:

                time.sleep(self.param["sleep_if_err"])
    @staticmethod
    def save_updates(file: str, data) -> None:
        sl = SaveLoad(file)
        sl.save_to_file(data)



