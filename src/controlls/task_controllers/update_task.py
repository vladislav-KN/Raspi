import json
import time
from abc import abstractmethod

import requests

from settings.settings import DATA_FOR_GUI, REQUEST_GUI
from src.controlls.save_loader import SaveLoad


class BaseUpdator:

    @abstractmethod
    def check_update(self) -> None:
        ...

    @staticmethod
    def save_updates(file: str, data) -> None:
        sl = SaveLoad(file)
        sl.save_to_file(data)


class GuiUpdate(BaseUpdator):
    def __init__(self, json_param, edited):
        self.param = json_param
        self.edited = edited

    def check_update(self):
        while True:
            time.sleep(10)


            try:
                req = requests.request('GET', REQUEST_GUI + "/update")
                if req.status_code < 300:
                    update_info = json.loads(req.text)
                    if update_info["updt"]:
                        req = requests.request('GET', REQUEST_GUI + "/gui")
                        json.loads(req.text)
                    else:
                        time.sleep(100)
            except:
                time.sleep(500)

            # if sl.load_from_file() != json.text:
            for item, i in zip(self.save_load.load_from_file()["elements"],
                               range(len(self.save_load.load_from_file()["elements"]))):
                d = Data(**item)
                d.create_img(i)
                new_dict["elem"].append({"folder": i, "name": d.name, "price": d.price})
            with open(os.getenv("LOAD_GUI"), 'w') as f:
                json.dump(new_dict, f, sort_keys=True, indent=4)
            self.lock.acquire()
            self.close = True
            self.lock.release()

    def updator(self):
        while (True):
            self.interface_loader()
