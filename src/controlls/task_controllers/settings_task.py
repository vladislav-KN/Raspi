import time
from threading import Lock

from src.controlls.task_controllers.base_updt import StateUpdt, FileUpdt
from src.objects.loading_files import Settings


class SettingsTask(StateUpdt):
    def __init__(self, lk: Lock, su: FileUpdt, d: Settings):
        self.lock = lk
        self.settings_upd = su
        self.data = d


    def updater(self):
        while True:
            if self.settings_upd.edited:
                self.lock.acquire()
                self.data = Settings(**self.save_load_data.load_from_file())
                self.settings_upd.edited = False
                self.lock.release()
            time.sleep(5)
