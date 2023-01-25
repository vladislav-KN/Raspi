import subprocess
import time
from threading import Thread
import urllib.request
import requests
from PyQt5.QtWidgets import QApplication
from wifi import Cell, Scheme
import sys

from GuiInterface import MainWindow
from MQTT.mqtt import brocker
from Settings.Settings import Settings
from Settings.Wifi import wifi as wf_dict
import numpy as np
import os

from Settings.save_loader import SL_functions


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False
class raspberry_pi_start_up:
    def __init__(self):
        self.id = getserial()
        #Load settings
        s = Settings()
        sl = SL_functions(s.file)
        self.settings = Settings(**sl.load_from_file())
        #Wi-Fi initialization
        sl.file = "Settings/wifi"
        self.wifi_dict = wf_dict(**sl.load_from_file())
        print(self.wifi_dict.ssid)
        #Start backgroud wifi reconection from the wifi list
        self.threads = []
        self.threads.append(Thread(target=self.wifi_connect))
        self.threads[len(self.threads) - 1].start()
        #MQTT PING
        self.MQTT = brocker(self.settings.mqtt_host, self.settings.mqtt_port)
        self.threads.append(Thread(target=self.mqtt_ping))
        self.threads[len(self.threads) - 1].start()
        # Check update
        self.threads.append(self.interface_loader())
        self.threads[len(self.threads) - 1].start()
        #Load Interface

                # if first start



                #Load Interface

                #Load Interface data
                    #Ads
                    #Product data
                # start ping MQTT

            #If not conected after start
                # load saved data
                    # Load Interface

                    # Load Interface data

        #Louch qr code reader
    def updator(self):
        while(True):

    def interface_loader(self):
        app = QApplication([])
        ex = MainWindow()
        ex.load()
        def cloaser():
            while (True):
                if os.path.exists("close"):
                    app.exit()
                    os.remove("close")
                    break
                time.sleep(1)
        t = Thread(target=cloaser)
        t.start()
        app.exec()
        return
    def mqtt_ping(self):
        while(True):
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
        while(True):
            print("awake")
            if connect():
                time.sleep(5)
                continue
            dtype = [("sig", int), ("qua", float), ("frq", float), ("ssid", 'S33')]
            val = [(cell.signal, [int(s) for s in cell.quality.split('/') if isfloat(s)][0] /
                    [int(s) for s in cell.quality.split('/') if isfloat(s)][1],
                    [float(s) for s in cell.frequency.split() if isfloat(s)][0], cell.ssid) for cell in Cell.all("wlan0")]
            wifis = np.sort(np.array(val, dtype=dtype), order=["frq", "qua"])[::-1]
            print(wifis["ssid"])
            for ssid in wifis["ssid"]:
                print(ssid.decode("utf-8"))
                if ssid.decode("utf-8") in self.wifi_dict.ssid:
                    os.system(f'nmcli d wifi connect "{ssid.decode("utf-8")}" password {self.wifi_dict.get_pass(ssid.decode("utf-8"))}')
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
    raspberry_pi_start_up()
