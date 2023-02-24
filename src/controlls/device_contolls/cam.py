import json
from datetime import datetime

import cv2
import requests
from pyzbar import pyzbar
from src.objects.cpture_data import ProductDO
from motor import Motors

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
            self.decode_cam(frame)

    def decode_cam(self, image) -> None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        print('reading...', end='\r')
        for barcode in barcodes:
            barcodeData = barcode.data.decode()
            barcodeType = barcode.type
            print("[" + str(datetime.now()) + "] Type:{} | Data: {}".format(barcodeType, barcodeData))
            self.check(barcodeData)

    def check(self, barcode_data: str):
        no_data = True
        for product in self.product_list:
            if barcode_data == product.key:
                Motors.rotate_list(product.line_number)
                self.mqtt.send_data(product.key)
                product.delete_from_file(barcode_data)
                no_data = False
                break
        if no_data:
            try:
                req = requests.request('GET', REQUEST_ORDERS + f"/order&{barcode_data}")
                if req.status_code < 300:
                    load = json.loads(req.text)["orders"]
                    data = ProductDO(key=barcode_data, line_number=load)
                    data.add_to_file()
                    Motors.rotate_list(load)
                    self.mqtt.send_data(barcode_data)
                    data.delete_from_file(barcode_data)
            except:
                pass