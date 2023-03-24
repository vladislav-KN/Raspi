import requests
import json
import time

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional
from threading import Lock

from settings.settings import SETTINGS_PATH
from settings.settings import ID_RASPI
from src.controlls.save_loader import SaveLoad


class FileUpdt:

    def __init__(self, dict_param: dict, edited: bool = False):
        self.param = dict_param
        self.edited = edited

    def check_update(self):
        while True:
            try:
                # req = requests.request('GET', self.param["to"] + f"/update?id={ID_RASPI}")
                # if req.status_code < 300:
                # update_info = json.loads(req.text)
                # if update_info[self.param["updt"]]:
                req = requests.request('GET', self.param["to"] + f"/{self.param['controller']}/{ID_RASPI}")
                if req.status_code < 300:
                    data = json.loads(req.text)
                    FileUpdt.save_updates(self.param["file"], data)
                    self.edited = True
                    time.sleep(self.param["sleep_if_exist"])
                else:
                    time.sleep(self.param["sleep_if_not_exist"])
                    # else:
                    # time.sleep(self.param["sleep_if_not_updt"])
            except:

                time.sleep(self.param["sleep_if_err"])

    @staticmethod
    def save_updates(file: str, data) -> None:
        sl = SaveLoad(file)
        sl.save_to_file(data)


class StateUpdt(ABC):
    data: Optional[list[BaseModel]] | Optional[BaseModel]
    save_load_data: SaveLoad = SaveLoad(SETTINGS_PATH)
    lock: Lock
    updater: FileUpdt

    @abstractmethod
    def updater(self) -> None:
        """
        Функция для обновления данных из файла

        :return:
        """
