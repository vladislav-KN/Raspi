import paho.mqtt.client as mqtt
import pickle


mqttc = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
mqttc.connect(host, port=1883, keepalive=60, bind_address="")