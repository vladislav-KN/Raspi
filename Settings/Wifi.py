from save_loader import SL_functions


class wifi:
    def __init__(self, ssid, password, file=""):
        self.file = self.__class__.__name__
        self.ssid = ssid
        self.password = password

    def get_pass(self, ssid):
        for s,p in zip(self.ssid,self.password):
            if s == ssid:
                return p
        return ""
