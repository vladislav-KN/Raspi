import json
import platform
import sys
import time
from multiprocessing import Process
from threading import Lock, Thread

import cv2
# from RPi import GPIO
from dotenv import load_dotenv
import requests
from src.controlls.device_contolls.cam import CamCapture
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.base_updt import FileUpdt
from src.controlls.task_controllers.interface_task import InterfaceInit
from src.controlls.task_controllers.mqtt_task import MQTTBroker
from src.controlls.task_controllers.orders_task import OrderTask
from src.controlls.task_controllers.settings_task import SettingsTask


from settings.settings import *
from src.controlls.task_controllers.wifi_task import WifiTask
from src.objects.loading_files import Settings, WiFi

load_dotenv()


def download():
    while True:
        try:
            if not os.path.isfile(os.getcwd() + SETTINGS_PATH):
                sl = SaveLoad(SETTINGS_PATH)
                req = requests.request('GET', REQUEST_SETTINGS+f"/settings/{ID_RASPI}")
                if req.status_code < 300:
                    data = json.loads(req.text)
                    sl.save_to_file(data)
                    print("settings loaded")
                else:
                    print("settings: " + str(req))
            elif not os.path.isfile(os.getcwd() + DATA_FOR_GUI):
                sl = SaveLoad(DATA_FOR_GUI)
                req = requests.request('GET', REQUEST_GUI + f"/gui/{ID_RASPI}")
                if req.status_code < 300:
                    data = json.loads(req.text)
                    sl.save_to_file(data)
                    print("gui loaded")
                else:
                    print("gui: " + str(req))
            elif not os.path.isfile(os.getcwd() + ORDERS_DATA):
                sl = SaveLoad(ORDERS_DATA)
                req = requests.request('GET', REQUEST_ORDERS + f"/orders/{ID_RASPI}")
                if req.status_code < 300:
                    data = json.loads(req.text)
                    sl.save_to_file(data)
                    print("orders loaded")
                else:
                    print("order: " + str(req))
            else:
                break
        except:
            time.sleep(1)
class RaspberryPiStartUp:
    def __init__(self):
        download()

        sl = SaveLoad(SETTINGS_PATH)
        data = sl.load_from_file()
        self.lock = Lock()
        self.settings = Settings(mqtt_host=data["mqtt_host"],
                                 mqtt_port=data["mqtt_port"],
                                 rest_host=data["rest_host"],
                                 wifi=[WiFi(ssid=x["ssid"], password=x["password"]) for x in data["wifi"]])
        sl.file = SETTINGS_UPDT
        self.set_updt = FileUpdt(sl.load_from_file())
        self.set_task = SettingsTask(self.lock, self.set_updt, self.settings)
        self.threads = []
        self.threads.append(Thread(target=self.set_task.updater))
        self.threads[len(self.threads) - 1].start()
        self.threads.append(Thread(target=self.set_updt.check_update))
        self.threads[len(self.threads) - 1].start()

        self.wifi_task = WifiTask(self.set_task)
        self.threads.append(Thread(target=self.wifi_task.wifi_connect))
        self.threads[len(self.threads) - 1].start()

        sl.file = ORDER_UPDT
        self.ord_updt = FileUpdt(sl.load_from_file())
        self.ord_task = OrderTask(self.lock, self.ord_updt)
        self.threads.append(Thread(target=self.ord_task.updater))
        self.threads[len(self.threads) - 1].start()
        self.threads.append(Thread(target=self.ord_updt.check_update))
        self.threads[len(self.threads) - 1].start()

        self.mqtt = MQTTBroker(self.set_task)
        self.threads.append(Thread(target=self.mqtt.mqtt_ping))
        self.threads[len(self.threads) - 1].start()

        sl.file = GUI_UPDT
        self.gui_upd = FileUpdt(sl.load_from_file())
        self.gui_init = InterfaceInit(self.lock, self.gui_upd)
        self.pyqt = Process(target=self.gui_init.reloader)

        self.camera = cv2.VideoCapture(0)
        self.cam_task = CamCapture(self.camera, self.mqtt, self.ord_task)
        self.cam = Thread(target=self.cam_task.cam_reader)
        self.cam.start()
        self.pyqt.run()


if __name__ == '__main__':
    try:
        os.environ.update({ "QT_QPA_PLATFORM_PLUGIN_PATH": "/usr/lib/aarch64-linux-gnu/qt5/plugins/xcbglintegrations/libqxcb-glx-integration.so"})
    except:
        ...
    RaspberryPiStartUp()
