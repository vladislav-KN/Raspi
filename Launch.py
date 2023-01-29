import json
import subprocess
import threading
import time
from threading import Thread
import urllib.request

import cv2
import requests
from PyQt5.QtWidgets import QApplication
#from RPi import GPIO
from dotenv import load_dotenv
from pyzbar import pyzbar
from wifi import Cell, Scheme
from datetime import datetime
from GuiInterface import MainWindow
from MQTT.mqtt import brocker
from Settings.LoadingFiles import Settings, wifi as wf_dict, Data
import numpy as np
import os
from Settings.save_loader import SL_functions


load_dotenv()
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
        self.close = False
        self.camera = cv2.VideoCapture(0)
        self.data_list = []
        self.lock = threading.Lock()
        self.data_path = os.getenv("DATA_FOR_INTERFACE")
        self.last_updated = datetime.now()

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
        self.threads.append(Thread(target=self.check_update))
        self.threads[len(self.threads) - 1].start()
        #Update Interface
        self.threads.append(Thread(target=self.updator))
        self.threads[len(self.threads) - 1].start()
        #
        self.threads.append(Thread(target=self.cam_reader))
        self.threads[len(self.threads) - 1].start()
                # if first start



                #Load Interface

                #Load Interface data
                    #Ads
                    #Product data
                # start ping MQTT

            #If not conected after start
                # load saved data


                    # Load Interface data

        #Louch qr code reader

    def cam_reader(self):
        while True:
        # Read current frame
            ret, frame = self.camera.read()
            im = self.decodeCam(frame)
    def decodeCam(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        print('reading...', end='\r')
        for barcode in barcodes:
            barcodeData = barcode.data.decode()
            barcodeType = barcode.type
            print("[" + str(datetime.now()) + "] Type:{} | Data: {}".format(barcodeType, barcodeData))
            self.Check(barcodeData)
        return image
    def Check(self, barcodeData):
        print(barcodeData)
        time.sleep(10)
        if(barcodeData in self.data_list):
            return
            #k = requests.request('GET', self.settings.rest_host+f"/order&{barcodeData}")
           # self.RotateMotor(k)

    #def RotateMotor(self, motorNum):
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(motorNum, GPIO.OUT)

        #GPIO.output(motorNum, True)
       # time.sleep(5)
       # GPIO.output(motorNum, False)
        #GPIO.cleanup()
        #time.sleep(5)

    def check_update(self):
        while (True):
            time.sleep(10)
            sl = SL_functions(os.getenv("DATA_FOR_GUI"))
            new_dict = {"elem":[]}
            # json = requests.request('GET', self.settings.rest_host+"/data")
            # if sl.load_from_file() != json.text:
            for item, i in zip(sl.load_from_file()["elements"], range(len(sl.load_from_file()["elements"]))):
                d = Data(**item)
                d.create_img(i)
                new_dict["elem"].append({"folder":i,"name":d.name,"price":d.price})
            with open(os.getenv("LOAD_GUI"), 'w') as f:
                json.dump(new_dict, f, sort_keys=True, indent=4)
            self.lock.acquire()
            self.close = True
            self.lock.release()


    def updator(self):
        while(True):
            new_thread = Thread(target=self.interface_loader())
            new_thread.start()
            new_thread.join()

    def interface_loader(self):
        app = QApplication([])
        ex = MainWindow()
        ex.load(os.getenv("LOAD_GUI"))
        def cloaser():
            while(not self.close):
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
