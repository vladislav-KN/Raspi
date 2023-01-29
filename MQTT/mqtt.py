import paho.mqtt.client as paho

from MQTT.mqtt_data import mqtt_data


class brocker:
    def __init__(self, host, port):
        self.broker = host
        self.port = port
        self.client = paho.Client("control1")  # create client object
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(self.broker, self.port)
    def send_data (self,id, data="", topic="ping"):
        if(data == ""):
            return self.client.publish(f"rasp/{topic}", f"{id}")
        else:
            send = mqtt_data(id, data)
            return self.client.publish(f"rasp/{topic}", f"{send.to_json()}")
    def on_disconnect(client, mosq, obj, rc):
        print("client disconnected ok")
    def on_publish(self, client, userdata, result):  # create function for callback
        print("data published \n")
        pass