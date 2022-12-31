from save_loader import SL_functions


class reserved_data(SL_functions):
    def __int__(self, file, **param):
        self.file = file
        self.Params = param
        self.Id = param['product_id']
        self.Code = param['user_code']

class product(SL_functions):
    def __int__(self, file, **param):
        self.file = file
        self.Params = param
        self.Id = param['product_id']
        self.Coil = param['coil_number']