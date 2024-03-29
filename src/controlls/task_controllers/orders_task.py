import time
from threading import Lock


from settings.settings import ORDERS_DATA, ORDER_NAME
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.base_updt import StateUpdt,FileUpdt
from src.objects.cpture_data import ProductDO






class OrderTask(StateUpdt):
    def __init__(self, lk: Lock, ou: FileUpdt):
        self.lock = lk
        self.order_upd = ou
        self.order_upd.edited = True
        self.data = []
        self.save_load_data = SaveLoad(ORDERS_DATA)

    def updater(self):
        while True:
            if self.order_upd.edited:
                self.lock.acquire()
                self.data = [ProductDO(key=order["key"], line_number=order["line_number"]) for order in
                             self.save_load_data.load_from_file()[ORDER_NAME]]
                self.order_upd.edited = False
                self.lock.release()
            time.sleep(5)
