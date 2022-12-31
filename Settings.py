from save_loader import SL_functions


class Settings(SL_functions):
    def __int__(self, file, **param):
        self.file = file
        self.host = param['host']
        self.Params = param


