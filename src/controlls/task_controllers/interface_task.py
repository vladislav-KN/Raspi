import json
import os
import time
from threading import Thread, Lock

from PyQt5.QtWidgets import *

from settings.settings import LOAD_GUI, GUI_NAME, DATA_FOR_GUI
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.update_task import Updater
from src.objects.loading_files import Data
from src.res.gui.gui import MainWindow


class InterfaceInit:
    close: bool
    lock: Lock
    gu: Updater

    def __init__(self, lk: Lock, gu: Updater):
        self.close = False
        self.lock = lk
        self.gui_upd = gu
        self.gui_upd.edited = True
        self.save_load_data = SaveLoad(DATA_FOR_GUI)
        self.threads = []
        self.threads.append(Thread(target=self.interface_updator))
        self.threads[len(self.threads) - 1].start()
        self.threads.append(Thread(target=self.gui_upd.check_update))
        self.threads[len(self.threads) - 1].start()

    def interface_loader(self):
        app = QApplication([])
        ex = MainWindow()
        ex.load(LOAD_GUI)

        def closer():
            ex.scrole()
            while not self.close:
                time.sleep(5)
            try:
                app.exit()
            except:
                time.sleep(1)
            self.lock.acquire()
            self.close = False
            self.lock.release()

        t = Thread(target=closer)
        t.start()
        app.exec()
        self.close = True
        return

    def update_file(self):
        new_dict = {"elem": []}
        for item, i in zip(self.save_load_data.load_from_file()[GUI_NAME],
                           range(len(self.save_load_data.load_from_file()[GUI_NAME]))):
            d = Data(**item)
            d.create_img(i)
            new_dict["elem"].append({"folder": i, "name": d.name, "price": d.price})
        with open(os.getcwd() + LOAD_GUI, 'w') as f:
            json.dump(new_dict, f, sort_keys=True, indent=4)

    def interface_updator(self):
        while True:
            if self.gui_upd.edited:
                self.update_file()
                self.lock.acquire()
                self.close = True
                self.gui_upd.edited = False
                self.lock.release()
            time.sleep(5)

    def updator(self):
        while True:
            if not self.gui_upd.edited:
                self.interface_loader()
