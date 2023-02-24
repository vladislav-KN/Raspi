import time

import paho.mqtt.client as paho


from settings.settings import ID_RASPI
from src.objects.mqtt_data import MqttData


class MQTTBroker:
    def __init__(self, host, port):
        self.broker = host
        self.port = port
        self.client = paho.Client("control1")  # create client object
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(self.broker, self.port)

    def send_data(self, data="", topic="ping"):
        if data == "":
            return self.client.publish(f"rasp/{topic}", f"{ID_RASPI}")
        else:
            send = MqttData(rasp_id=ID_RASPI, code=data)
            return self.client.publish(f"rasp/{topic}", f"{send.to_json()}")

    @staticmethod
    def on_disconnect(mosq, obj, rc):
        print("client disconnected ok")
    @staticmethod
    def on_publish( client, userdata, result):  # create function for callback
        print("data published \n")
        pass

    def mqtt_ping(self):
        while (True):
            self.send_data()
            time.sleep(20)
            print("AWAKE")