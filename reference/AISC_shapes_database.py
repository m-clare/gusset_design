import json

class AISCShapesDatabase(object):

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls(data)

    def get_section_depth(self, section_size):
        for key, value in self.data.items():
            if value['AISC_Manual_Label'] == section_size:
                return value['d']

    def get_flange_width(self, section_size):
        for key, value in self.data.items():
            if value['AISC_Manual_Label'] == section_size:
                return value['bf']

