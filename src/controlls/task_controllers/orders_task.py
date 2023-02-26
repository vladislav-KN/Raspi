import time
from threading import Lock

from settings.settings import ORDERS_DATA
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.update_task import Updator
from src.objects.cpture_data import ProductDO
from src.objects.loading_files import Settings


class OrderTask:
    data:list[ProductDO]
    def __init__(self, lk: Lock, ou: Updator):
        self.close = False
        self.lock = lk
        self.order_upd = ou
        self.data = []
        self.save_load_data = SaveLoad(ORDERS_DATA)

    def order_updator(self):
        while True:
            if self.order_upd.edited:
                self.lock.acquire()
                self.data = self.save_load_data.load_from_file()
                self.order_upd.edited = False
                self.lock.release()
            time.sleep(5)