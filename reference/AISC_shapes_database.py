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
            if value['EDI_Std_Nomenclature'] == section_size:
                return value['d']

    def get_flange_width(self, section_size):
        for key, value in self.data.items():
            if value['EDI_Std_Nomenclature'] == section_size:
                return value['bf']


if __name__ == "__main__":
    test = AISCShapesDatabase.from_json('aisc_shapes_database_v15.json')
    value = test.get_section_depth('W44X230')
    print(value)
    value = test.get_flange_width('W44X230')
    print(value)
