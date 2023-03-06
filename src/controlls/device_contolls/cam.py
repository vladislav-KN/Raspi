import json
import time
from datetime import datetime

import cv2
import requests
from pyzbar import pyzbar

#from src.controlls.device_contolls.motor import Motors
from src.controlls.task_controllers.mqtt_task import MQTTBroker
from src.controlls.task_controllers.orders_task import OrderTask
from src.objects.cpture_data import ProductDO


from settings.settings import REQUEST_ORDERS


class CamCapture:
    orders: OrderTask

    def __init__(self, cam, client: MQTTBroker, data: OrderTask) -> None:
        self.camera = cam
        self.orders = data
        self.mqtt = client

    def cam_reader(self) -> None:
        while True:
            # Read current frame
            ret, frame = self.camera.read()
            im = self.decode_cam(frame)
            time.sleep(1)


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
        for product in self.orders.data:

            if barcode_data == product.key:
                #Motors.rotate_list(product.line_number)
                time.sleep(30)
                print("complete")
                self.mqtt.send_data(product.key, "order")
                product.delete_from_file(barcode_data)
                self.orders.data.remove(product)
                no_data = False
                break
        if no_data:
            try:
                req = requests.request('GET', REQUEST_ORDERS + f"/order&{barcode_data}")
                if req.status_code < 300:
                    load = json.loads(req.text)["orders"]
                    data = ProductDO(key=barcode_data, line_number=load)
                    data.add_to_file()
                    self.orders.data.append(data)
                    #Motors.rotate_list(load)
                    time.sleep(30)
                    self.orders.data.remove(data)
                    data.delete_from_file(barcode_data)
                    self.mqtt.send_data(barcode_data, "order")

            except:
                pass
