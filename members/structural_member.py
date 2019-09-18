import json
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase


class StructuralMember(object):

    def __init__(self):
        super(StructuralMember, self).__init__()

    @classmethod
    def from_json(cls, filepath):
        structural_member = cls()
        with open(filepath, 'r') as fp:
            data = json.load(fp)
            for k, v in data.items():
                setattr(structural_member, k, v)
        return structural_member

    @classmethod
    def from_AISC_database(cls, section_name, AISCDatabase):
        structural_member = cls()
        for index, dictionary in AISCDatabase.data.items():
            if dictionary['AISC_Manual_Label'] == section_name:
                for dictionary, properties in dictionary.items():
                    setattr(structural_member, dictionary, properties)
        return structural_member

if __name__ == "__main__":
    aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
    w40x593 = StructuralMember.from_AISC_database(section_name="W40X593", AISCDatabase=aisc_db)
    print(w40x593.tf)