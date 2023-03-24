import os
from typing import Optional

import qrcode
import requests
from pydantic import BaseModel


class WiFi(BaseModel):
    ssid: str
    password: str


class Settings(BaseModel):
    mqtt_host: str
    mqtt_port: int
    rest_host: str
    wifi: Optional[list[WiFi]]

    def get_wifi_pass(self, ssid: str) -> str:
        for wifi in self.wifi:
            if wifi.ssid == ssid:
                return wifi.password
        return ""


class GuiData(BaseModel):
    png: str
    name: str
    price: str
    link: str

    def create_img(self, folder_name: int) -> None:
        if not os.path.exists(os.getcwd()+f"/src/res/imgs/{folder_name}"):
            os.makedirs(os.getcwd() +f"/src/res/imgs/{folder_name}")
        if self.link:
            img = qrcode.make(self.link)
            img.save(os.getcwd() +f"/src/res/imgs/{folder_name}/qr.png")
        if self.png:
            img_data = requests.get(self.png).content
            with open(os.getcwd()+f'/src/res/imgs/{folder_name}/img.png', 'wb') as handler:
                handler.write(img_data)
