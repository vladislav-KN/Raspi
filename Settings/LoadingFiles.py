import os

import qrcode
import requests


class Settings(object):
    def __init__(self, mqtt_host="0.0.0.0", mqtt_port=0, rest_host="", file=""):
        self.file = "Settings/"+self.__class__.__name__
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.rest_host = rest_host



class wifi:
    def __init__(self, ssid, password, file=""):
        self.file = "Settings/" + self.__class__.__name__
        self.ssid = ssid
        self.password = password

    def get_pass(self, ssid):
        for s,p in zip(self.ssid,self.password):
            if s == ssid:
                return p
        return ""
class Data:
    def __init__(self, png, name,price,link):
        self.png = png
        self.name = name
        self.price = price
        self.link = link
    def create_img(self, id):
        if not os.path.exists(f"Res/imgs/{id}"):
            os.makedirs(f"Res/imgs/{id}")
        if self.link:
            img = qrcode.make(self.link)
            img.save(f"Res/imgs/{id}/qr.png")
        if self.png:
            img_data = requests.get(self.png).content
            with open(f'Res/imgs/{id}/img.png', 'wb') as handler:
                handler.write(img_data)