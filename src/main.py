import json
import subprocess
import threading
import time
from multiprocessing import Process
from threading import Thread
import urllib.request

from PyQt5.QtWidgets import QApplication
# from RPi import GPIO
from dotenv import load_dotenv
from wifi import Cell
from datetime import datetime

from src.controlls.device_contolls.cam import CamCapture
from src.controlls.save_loader import SaveLoad
from src.objects.loading_files import Settings, WiFi
from src.res.gui.gui import MainWindow
from src.controlls.task_controllers.mqtt_task import Broker
from settings.settings import SETTINGS_PATH, DATA_FOR_GUI
import numpy as np

load_dotenv()


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


class RaspberryPiStartUp:
    def __init__(self):

        self.close = False

        self.lock = threading.Lock()
        self.data_path = DATA_FOR_GUI
        self.last_updated = datetime.now()
        self.cam_capture = CamCapture()
        # Load settings

        sl = SaveLoad(SETTINGS_PATH)
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


    def interface_loader(self):
        app = QApplication([])
        ex = MainWindow()
        ex.load(os.getenv("LOAD_GUI"))

        def cloaser():
            ex.scrole()
            while (not self.close):
                time.sleep(1)
            app.exit()
            self.lock.acquire()
            self.close = False
            self.lock.release()

        t = Thread(target=cloaser)
        t.start()
        app.exec()
        t.join()
        return

    def mqtt_ping(self):
        while (True):
            self.MQTT.send_data(self.id)
            time.sleep(20)
            print("AWAKE")

    def wifi_connect(self):
        def isfloat(val):
            try:
                float(val)
                return True
            except ValueError:
                return False

        while (True):
            print("awake")
            if connect():
                time.sleep(5)
                continue
            dtype = [("sig", int), ("qua", float), ("frq", float), ("ssid", 'S33')]
            val = [(cell.signal, [int(s) for s in cell.quality.split('/') if isfloat(s)][0] /
                    [int(s) for s in cell.quality.split('/') if isfloat(s)][1],
                    [float(s) for s in cell.frequency.split() if isfloat(s)][0], cell.ssid) for cell in
                   Cell.all("wlan0")]
            wifis = np.sort(np.array(val, dtype=dtype), order=["frq", "qua"])[::-1]
            print(wifis["ssid"])
            for ssid in wifis["ssid"]:
                print(ssid.decode("utf-8"))
                if ssid.decode("utf-8") in self.wifi_dict.ssid:
                    os.system(
                        f'nmcli d wifi connect "{ssid.decode("utf-8")}" password {self.wifi_dict.get_pass(ssid.decode("utf-8"))}')
                    ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    try:
                        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
                        print(output)
                        break
                    except subprocess.CalledProcessError:
                        # grep did not match any lines
                        print("No wireless networks connected")
            time.sleep(5)


if __name__ == '__main__':
    RaspberryPiStartUp()
