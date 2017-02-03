import json
import os



class Configurator:
    def __init__(self, filename=os.path.abspath("../config.json")): # TODO better path for default config
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.conf = read_json(filename)

    def access(self, path:str):
        parts = path.split(".")
        # TODO recursion into path e.g. a.b.c -> conf['a']['b']['c'] -> Can be achieved as the resulting is either obj or primitive?

def read_json(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        return data