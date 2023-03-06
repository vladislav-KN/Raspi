import time
from threading import Lock

from settings.settings import SETTINGS_PATH
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.update_task import Updater
from src.objects.loading_files import Settings


class SettingsTask:
    def __init__(self, lk: Lock, su: Updater, d: Settings):
        self.lock = lk
        self.settings_upd = su
        self.data = d
        self.save_load_data = SaveLoad(SETTINGS_PATH)

    def settings_updator(self):
        while True:
            if self.settings_upd.edited:
                self.lock.acquire()
                self.data = Settings(**self.save_load_data.load_from_file())
                self.settings_upd.edited = False
                self.lock.release()
            time.sleep(5)
