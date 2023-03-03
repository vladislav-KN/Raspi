import time

import paho.mqtt.client as paho


from settings.settings import ID_RASPI
from src.controlls.task_controllers.settings_task import SettingsTask
from src.objects.mqtt_data import MqttData


class MQTTBroker:
    def __init__(self, set:SettingsTask):
        self.settings = set
        self.host = str(self.settings.data.mqtt_host)
        self.port = int(self.settings.data.mqtt_port)
        self.client = paho.Client("control1")  # create client object
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.on_disconnect = self.on_disconnect
        while True:
            try:
                self.client.connect(self.host,self.port)
                break
            except:
                time.sleep(10)
    def send_data(self, data="", topic="ping"):
        try:
            if self.host != str(self.settings.data.mqtt_host) or self.port != int(self.settings.data.mqtt_port):
                self.client.disconnect()
                self.host = str(self.settings.data.mqtt_host)
                self.port = int(self.settings.data.mqtt_port)
                self.client = paho.Client("control1")  # create client object
                self.client.on_publish = self.on_publish  # assign function to callback
                self.client.on_disconnect = self.on_disconnect
                self.client.connect(self.host, self.port)
            if data == "":
                return self.client.publish(f"rasp/{topic}", f"{ID_RASPI}")
            else:
                send = MqttData(rasp_id=ID_RASPI, code=data)
                return self.client.publish(f"rasp/{topic}", f"{send.to_json()}")
        except:
            ...


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