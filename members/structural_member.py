import json
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase


class StructuralMember(object):

    def __init__(name):
        self.name = name

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
            for k, v in data.items():
                setattr(self, k, v)

    @classmethod
    def from_AISC_database(cls, section_name, AISCDatabase):
        for index, dictionary in AISCDatabase.data.items():
            if dictionary['AISC_Manual_Label'] == section_name:
                for dictionary, properties in dictionary.items():
                    print(dictionary, properties)
                    setattr(cls, dictionary, properties)
        return cls

if __name__ == "__main__":
    aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
    w40x593 = StructuralMember.from_AISC_database(section_name="W40X593", AISCDatabase=aisc_db)