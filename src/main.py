import sys
from multiprocessing import Process
from threading import Lock, Thread

import cv2
# from RPi import GPIO
from dotenv import load_dotenv

from src.controlls.device_contolls.cam import CamCapture
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.interface_task import InterfaceInit
from src.controlls.task_controllers.mqtt_task import MQTTBroker
from src.controlls.task_controllers.orders_task import OrderTask
from src.controlls.task_controllers.settings_task import SettingsTask
from src.controlls.task_controllers.update_task import Updator

from settings.settings import *
from src.controlls.task_controllers.wifi_task import WifiTask
from src.objects.loading_files import Settings, WiFi

load_dotenv()


class RaspberryPiStartUp:
    def __init__(self):
        sl = SaveLoad(SETTINGS_PATH)
        data = sl.load_from_file()
        self.lock = Lock()
        self.settings = Settings(mqtt_host=data["mqtt_host"],
                                 mqtt_port=data["mqtt_port"],
                                 rest_host=data["rest_host"],
                                 wifi=[WiFi(ssid=x["ssid"], password=x["ssid"]) for x in data["wifi"]])
        sl.file = SETTINGS_UPDT
        self.set_updt = Updator(sl.load_from_file())
        self.set_task = SettingsTask(self.lock, self.set_updt, self.settings)
        self.threads = []
        self.threads.append(Thread(target=self.set_task.settings_updator))
        self.threads[len(self.threads) - 1].start()
        self.threads.append(Thread(target=self.set_updt.check_update))
        self.threads[len(self.threads) - 1].start()

        self.wifi_task = WifiTask(self.set_task)
        self.threads.append(Thread(target=self.wifi_task.wifi_connect))
        self.threads[len(self.threads) - 1].start()

        sl.file = ORDER_UPDT
        self.ord_updt = Updator(sl.load_from_file())
        self.ord_task = OrderTask(self.lock, self.ord_updt)
        self.threads.append(Thread(target=self.ord_task.order_updator))
        self.threads[len(self.threads) - 1].start()
        self.threads.append(Thread(target=self.ord_updt.check_update))
        self.threads[len(self.threads) - 1].start()

        self.mqtt = MQTTBroker(self.set_task)
        self.threads.append(Thread(target=self.mqtt.mqtt_ping))
        self.threads[len(self.threads) - 1].start()

        sl.file = GUI_UPDT
        self.gui_upd = Updator(sl.load_from_file())
        self.gui_init = InterfaceInit(self.lock, self.gui_upd)
        self.pyqt = Process(target=self.gui_init.updator)

        self.camera = cv2.VideoCapture(0)
        self.cam_task = CamCapture(self.camera, self.mqtt, self.ord_task)
        self.cam = Thread(target=self.cam_task.cam_reader)
        self.cam.start()
        self.pyqt.run()


if __name__ == '__main__':
    RaspberryPiStartUp()
