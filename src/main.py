import json

import threading
import time
from multiprocessing import Process
from threading import Thread


from PyQt5.QtWidgets import QApplication
# from RPi import GPIO
from dotenv import load_dotenv

from datetime import datetime

from src.controlls.device_contolls.cam import CamCapture
from src.controlls.save_loader import SaveLoad
from src.controlls.task_controllers.update_task import Updator

from src.objects.loading_files import Settings, WiFi, Data
from src.res.gui.gui import MainWindow

from settings.settings import SETTINGS_PATH, DATA_FOR_GUI, LOAD_GUI, GUI_NAME


load_dotenv()

class RaspberryPiStartUp:
    def __init__(self):
        sl = SaveLoad(GUI_UPDT)
        self.close = False
        self.last_updated = datetime.now()
        self.cam_capture = CamCapture()
        self.gui_upd = Updator(GUI_NAME)
        # Load settings


        data = sl.load_from_file()
        self.settings = Settings(mqtt_host=data["mqtt_host"],
                                 mqtt_port=data["mqtt_port"],
                                 rest_host=data["rest_host"],
                                 wifi=[WiFi(ssid=x["ssid"], password=x["ssid"]) for x in data["wifi"]])

        # Start background wifi reconnection from the wifi list
        self.threads = []
        self.threads.append(Thread(target=self.wifi_connect))
        self.threads[len(self.threads) - 1].start()
        # mqtt_contolls PING
        self.MQTT = Broker(self.settings.mqtt_host, self.settings.mqtt_port)
        self.threads.append(Thread(target=self.mqtt_ping))
        self.threads[len(self.threads) - 1].start()
        # Check update
        self.threads.append(Thread(target=self.check_update))
        self.threads[len(self.threads) - 1].start()
        # Update Interface
        self.pyqt = Process(target=self.updator)
        self.pyqt.run()
        #
        self.threads.append(Thread(target=self.cam_reader))
        self.threads[len(self.threads) - 1].start()
        # if first start

        # Load Interface

        # Load Interface data
        # Ads
        # Product data
        # start ping mqtt_contolls

        # If not conected after start
        # load saved data

        # Load Interface data

        # Louch qr code reader






if __name__ == '__main__':
    RaspberryPiStartUp()
