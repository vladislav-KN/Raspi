import pickle


class SL_functions:
    def __int__(self, file, **param):
        self.file = file
    def load_from_file(self):
        with open(self.file, 'rb') as f:
             return pickle.load(f)

    def save_to_file(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        return