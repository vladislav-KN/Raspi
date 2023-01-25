class Settings(object):
    def __init__(self, mqtt_host="0.0.0.0", mqtt_port=0, file=""):
        self.file = self.__class__.__name__
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port



