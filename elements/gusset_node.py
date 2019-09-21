from gusset_design.members.steel_member import SteelMember
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.visualization.mesh import PlateMesh
from structural_node import StructuralNode
from gusset_plate import GussetPlate
import json


__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


class GussetNode(StructuralNode):

    def __init__(self, beams=[], braces=[], column=[], gussets=None):
        super(GussetNode, self).__init__()

        self.beams = beams
        self.braces = braces
        self.column = column
        self.gussets = gussets
        self.AISC_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')

        self.meshes = []

    @classmethod
    def from_json(cls, filepath):
        gusset_node = cls()
        with open(filepath, 'r') as fp:
            data = json.load(fp)
            for k, v in data.items():
                if k == 'beams':
                    for beam in v:
                        name = beam['name'],
                        s_pt = beam['start_pt'],
                        e_pt = beam['end_pt']
                        gusset_node.beams.append(SteelMember.from_AISC_database(name, s_pt, e_pt, gusset_node.AISC_db))
                if k == 'column':
                    for col in v:
                        name = col['name'],
                        s_pt = col['start_pt'],
                        e_pt = col['end_pt']
                        gusset_node.column.append(SteelMember.from_AISC_database(name, s_pt, e_pt, gusset_node.AISC_db))
                if k == 'brace':
                    for brace in v:
                        name = brace['name'],
                        s_pt = brace['start_pt'],
                        e_pt = brace['end_pt']
                        gusset_node.brace.append(SteelMember.from_AISC_database(name, s_pt, e_pt, gusset_node.AISC_db))
        return gusset_node

    @classmethod
    def to_json():
        pass

    def add_beam(self, beam):
        self.beams.append[beam]
        return

    def add_column(self, column):
        pass

    def add_brace(self, brace):
        pass

    def add_gusset(self, beam, brace, column):
        gusset = GussetPlate
        self.gussets.append[gusset]
        pass

    def add_gusset_from_json(self, filepath):
        pass


    def check_connection_framing_compatibility():
        '''
        Check quadrants of gusset node to ensure that all framing columms
        and beams are compatible
        '''
        pass

    def check_gusset_compatibility():
        '''
        Check thickness of top and bottom gusset framing into column and take largest thickness
        '''
        pass

    def to_meshes(self):
        pass

if __name__ == "__main__":
    test = GussetNode.from_json('../examples/sample_node.json')
    print(test.__dict__)