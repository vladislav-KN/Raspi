import json
import time
from threading import Thread, Lock

from PyQt5.QtWidgets import *

from settings.settings import LOAD_GUI, GUI_NAME, DATA_FOR_GUI
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.update_task import Updator
from src.objects.loading_files import Data
from src.res.gui.gui import MainWindow


class InterfaceInit:
    close: bool
    lock: Lock
    gu: Updator

    def __init__(self, lk: Lock, gu: Updator):
        self.close = False
        self.lock = lk
        self.gui_upd = gu
        self.save_load_data = SaveLoad(DATA_FOR_GUI)
        self.threads = []
    def interface_loader(self):
        app = QApplication([])
        ex = MainWindow()
        ex.load(LOAD_GUI)
        def closer():
            ex.scrole()
            while not self.close:
                time.sleep(5)
            app.exit()
            self.lock.acquire()
            self.close = False
            self.lock.release()

        t = Thread(target=closer)
        t.start()
        app.exec()
        t.join()
        return

    def interface_updator(self):
        while True:
            if self.gui_upd.edited:
                new_dict = {}
                for item, i in zip(self.save_load_data.load_from_file()[GUI_NAME],
                                   range(len(self.save_load_data.load_from_file()[GUI_NAME]))):
                    d = Data(**item)
                    d.create_img(i)
                    new_dict["elem"].append({"folder": i, "name": d.name, "price": d.price})
                with open(LOAD_GUI, 'w') as f:
                    json.dump(new_dict, f, sort_keys=True, indent=4)
                self.lock.acquire()
                self.close = True
                self.gui_upd.edited = False
                self.lock.release()
            time.sleep(5)
    def updator(self):
        self.threads.append(Thread(target=self.interface_updator))
        self.threads[len(self.threads) - 1].start()
        self.threads.append(Thread(target=self.gui_upd.check_update))
        self.threads[len(self.threads) - 1].start()
        while True:
            self.interface_loader()

