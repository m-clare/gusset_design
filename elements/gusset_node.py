from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.visualization.mesh import PlateMesh
from gusset_design.elements.steel_member import SteelMember
from gusset_design.elements.structural_node import StructuralNode
from gusset_design.elements.gusset_plate import GussetPlate
import plotly.graph_objs as go

import json

__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


class GussetNode(StructuralNode):

    def __init__(self, beams=[], braces=[], column=[], gussets=[]):
        super(GussetNode, self).__init__()

        self.beams = beams
        self.braces = braces
        self.column = column
        self.gussets = gussets
        self.AISC_db = AISCShapesDatabase.from_json(
                       '../gusset_design/reference/aisc_shapes_database_v15.json')

    # @property
    # def member_meshes(self):
    #     component_types = [self.beams, self.braces, self.column]
    #     member_meshes = []
    #     for members in component_types:
    #         print("2")
    #         for member in members:
    #             member_geo = member.to_global_geometry()
    #             for part in member_geo:
    #                 print("3")
    #                 new_mesh = PlateMesh.from_geometry(part, to_dict=True)
    #                 print("4")
    #                 member_meshes.append(new_mesh)
    #     self._member_meshes = member_meshes
    #     return self._member_meshes

    # @member_meshes.setter
    # def member_meshes(self,):
    #     print("1")
        

    @classmethod
    def from_json(cls, filepath):
        gusset_node = cls()
        with open(filepath, 'r') as fp:
            data = json.load(fp)
            for k, v in data.items():
                if k == 'beams':
                    for beam, values in v.items():
                        name = beam
                        gusset_node.beams.append(
                            SteelMember.from_AISC_database(
                                name, gusset_node.AISC_db, data=values))
                if k == 'column':
                    for col, values in v.items():
                        name = col
                        gusset_node.column.append(
                            SteelMember.from_AISC_database(
                                name, gusset_node.AISC_db, data=values))
                if k == 'braces':
                    for brace, values in v.items():
                        name = brace
                        gusset_node.braces.append(
                            SteelMember.from_AISC_database(
                                name, gusset_node.AISC_db, data=values))
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
        component_types = [self.beams, self.column, self.braces]
        member_meshes = []
        for members in component_types:
            for member in members:
                member_geo = member.to_global_geometry()
                for part in member_geo:
                    new_mesh = PlateMesh.from_geometry(part, to_dict=True)
                    member_meshes.append(new_mesh)
        # fig = go.Figure(data=member_meshes)
        # fig.update_layout(scene_aspectmode='data')
        # fig.show()
        return member_meshes

if __name__ == "__main__":
    test = GussetNode.from_json('../examples/sample_node.json')
    print(test.beams[0].__dict__)
    print(test.column[0].__dict__)
    print(test.to_meshes())
    # print(test.to_meshes())
    