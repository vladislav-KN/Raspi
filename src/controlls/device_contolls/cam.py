import json
from datetime import datetime

import cv2
import requests
from pyzbar import pyzbar
from src.objects.cpture_data import ProductDO
from motor import Motors
from src.controlls.task_controllers.mqtt_task import Broker
from settings.settings import REQUEST_ORDERS


class CamCapture:
    product_list: list[ProductDO]

    def __init__(self, client: Broker, data: list[ProductDO]) -> None:
        self.camera = cv2.VideoCapture(0)
        self.product_list = data
        self.mqtt = client

    def cam_reader(self) -> None:
        while True:
            # Read current frame
            ret, frame = self.camera.read()
            self.decodeCam(frame)

    def decode_cam(self, image) -> None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        print('reading...', end='\r')
        for barcode in barcodes:
            barcodeData = barcode.data.decode()
            barcodeType = barcode.type
            print("[" + str(datetime.now()) + "] Type:{} | Data: {}".format(barcodeType, barcodeData))
            self.Check(barcodeData)

    def check(self, barcode_data: str):
        for product in self.product_list:
            if barcode_data == product.Key:
                Motors.rotate_list(product.LineNumber)
                self.mqtt.send_data(product.Key)

                break
            else:
                try:
                    load = json.loads(requests.request('GET', REQUEST_ORDERS + f"/order&{barcode_data}").text)
                    Motors.rotate_list(load["orders"])
                    self.mqtt.send_data(barcode_data)
                    break
                except:

                    pass
