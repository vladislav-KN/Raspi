import json
import os
import time
from threading import Thread, Lock

from PyQt5.QtWidgets import *

from settings.settings import LOAD_GUI, GUI_NAME, DATA_FOR_GUI
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.base_updt import StateUpdt, FileUpdt

from src.objects.loading_files import GuiData
from src.res.gui.gui import MainWindow


class InterfaceInit(StateUpdt):
    close: bool
    threads: list[Thread]
    gui_updater: FileUpdt

    def __init__(self, lk: Lock, gu: FileUpdt):
        self.close = False
        self.lock = lk
        self.gui_updater = gu
        self.gui_updater.edited = True
        self.save_load_data = SaveLoad(DATA_FOR_GUI)
        self.threads = []
        self.threads.append(Thread(target=self.updater))
        self.threads[len(self.threads) - 1].start()
        self.threads.append(Thread(target=self.gui_updater.check_update))
        self.threads[len(self.threads) - 1].start()

    def interface_loader(self):
        app = QApplication([])
        ex = MainWindow()
        ex.load(LOAD_GUI)

        def closer():
            print("#" + str(self.close))
            while not self.close:
                time.sleep(5)
            try:
                app.exit()
            except:
                time.sleep(1)
            self.lock.acquire()
            self.close = False
            self.lock.release()

        self.close = False
        t = Thread(target=closer)
        t.start()
        t2 = Thread(target=ex.scrole)
        t2.start()
        app.exec()
        self.close = True
        return

    def update_file(self):
        new_dict = {"elem": []}
        for item, i in zip(self.save_load_data.load_from_file()[GUI_NAME],
                           range(len(self.save_load_data.load_from_file()[GUI_NAME]))):
            d = GuiData(**item)
            d.create_img(i)
            new_dict["elem"].append({"folder": i, "name": d.name, "price": d.price})
        with open(os.getcwd() + LOAD_GUI, 'w') as f:
            json.dump(new_dict, f, sort_keys=True, indent=4)

    def updater(self):
        while True:
            if self.gui_updater.edited:
                self.update_file()
                self.lock.acquire()
                self.close = True
                self.gui_updater.edited = False
                self.lock.release()
            time.sleep(5)

    def reloader(self):
        while True:
            if not self.gui_updater.edited:
                self.interface_loader()
