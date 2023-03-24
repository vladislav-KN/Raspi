import os
import time
from typing import Optional
import numpy as np

from src.controlls.task_controllers.settings_task import SettingsTask
from src.objects.loading_files import WiFi
import urllib.request
from wifi import Cell
import subprocess


class WifiTask:
    host_checker: str
    settings: SettingsTask

    def __init__(self, set: SettingsTask, htc='https://google.com'):
        self.host_checker = htc
        self.settings = set

    def connect(self):
        try:
            urllib.request.urlopen(self.host_checker)
            return True
        except:
            return False

    def wifi_connect(self):
        def isfloat(val):
            try:
                float(val)
                return True
            except ValueError:
                return False

        while (True):
            print("awake")
            if self.connect():
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
                for wifi in self.settings.data.wifi:
                    if ssid.decode("utf-8") == wifi.ssid:
                        os.system(
                            f'nmcli d wifi connect "{ssid.decode("utf-8")}" password {wifi.password}')
                        time.sleep(10)
                        ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        try:
                            output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
                            print(output)
                            break
                        except subprocess.CalledProcessError:
                            # grep did not match any lines
                            print("No wireless networks connected")
            time.sleep(5)
