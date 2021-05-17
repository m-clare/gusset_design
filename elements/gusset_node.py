from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.visualization.mesh import PlateMesh
from gusset_design.elements.steel_member import SteelMember
from gusset_design.elements.gusset_plate import GussetPlate
import plotly.graph_objs as go

import os 
import json

__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

class GussetNode(object):

    def __init__(self, beams=[], braces=[], column=[], gussets=[]):
        super(GussetNode, self).__init__()
        self.x = 0
        self.y = 0
        self.z = 0
        self.beams = beams
        self.braces = braces
        self.column = column
        self.gussets = gussets
        self.AISC_db = AISCShapesDatabase.from_json(dir_path + '/../reference/aisc_shapes_database_v15.json')

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

    def add_gusset(self, beam, brace, column):
        gusset = GussetPlate(beam, brace, column)
        self.gussets.append[gusset]

    def get_brace_angle(self, brace, column):
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
        return member_meshes
