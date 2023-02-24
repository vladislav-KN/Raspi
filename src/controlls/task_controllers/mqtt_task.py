import paho.mqtt.client as paho

from mqtt_task.mqtt_data import MqttData
from settings.settings import ID_RASPI

class Broker:
    def __init__(self, host, port):
        self.broker = host
        self.port = port
        self.client = paho.Client("control1")  # create client object
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(self.broker, self.port)
    def send_data (self, data="", topic="ping"):
        if(data == ""):
            return self.client.publish(f"rasp/{topic}", f"{ID_RASPI}")
        else:
            send = MqttData(ID_RASPI, data)
            return self.client.publish(f"rasp/{topic}", f"{send.to_json()}")
    def on_disconnect(client, mosq, obj, rc):
        print("client disconnected ok")
    def on_publish(self, client, userdata, result):  # create function for callback
        print("data published \n")
        pass