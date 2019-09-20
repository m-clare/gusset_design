import json
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from sympy import Point3D

class SteelMember(object):

    def __init__(self, d=None, tw=None, bf=None, tf=None):
        self.name = None
        self.tf = tf
        self.tw = tw
        self.d = d
        self.bf = bf

    @classmethod
    def from_json(cls, filepath):
        steel_member = cls()
        with open(filepath, 'r') as fp:
            data = json.load(fp)
            for k, v in data.items():
                setattr(steel_member, k, v)
        return steel_member

    @classmethod
    def from_AISC_database(cls, section_name, AISCDatabase):
        steel_member = cls()
        for index, member in AISCDatabase.data.items():
            if member['AISC_Manual_Label'] == section_name:
                for member, prop in member.items():
                    setattr(steel_member, member, prop)
        return steel_member

    def to_mesh_general(self, start_pt, end_pt):
        meshes = []
        x0, y0, z0 = start_pt['x'], start_pt['y'], start_pt['z']
        x1, y1, z1 = end_pt['x'], end_pt['y'], end_pt['z']
        return

    def extrude_plate(self, pts, thickness, direction):
        mesh_Point3D = []
        mesh_points = []
        if direction == 'x':
            for pt in pts:
                mesh_Point3D.append(pt.translate(-0.5 * thickness, 0, 0))
                mesh_Point3D.append(pt.translate(0.5 * thickness, 0, 0))
        if direction == 'y':
            for pt in pts:
                mesh_Point3D.append(pt.translate(0, -0.5 * thickness, 0))
                mesh_Point3D.append(pt.translate(0, 0.5 * thickness, 0))
        if direction == 'z':
            for pt in pts:
                mesh_Point3D.append(pt.translate(0, 0, -0.5 * thickness))
                mesh_Point3D.append(pt.translate(0, 0, 0.5 * thickness))
        for pt in mesh_Point3D:
            mesh_points.append({'x': float(pt.x), 'y': float(pt.y), 'z': float(pt.z)})
        return mesh_points
        

    def x_section_to_mesh(self, plane, length, frame=None):
        # DOES NOT CONSIDER LOCATION IN GLOBAL SPACE
        meshes = []
        if plane == 'xz':
            wf_pt0 = Point3D(0, 0, self.d * 0.5 - self.tw * 0.5)
            wf_pt1 = Point3D(0, 0, -(self.d * 0.5 - self.tw * 0.5))
            wf_pt2 = wf_pt0.translate(-self.bf * 0.5, 0, 0)
            wf_pt3 = wf_pt0.translate(self.bf * 0.5, 0, 0)
            wf_pt4 = wf_pt1.translate(-self.bf * 0.5, 0, 0)
            wf_pt5 = wf_pt1.translate(self.bf * 0.5, 0, 0)
            web_pl = self.extrude_plate([wf_pt0.translate(0, -length * 0.5, 0),
                                         wf_pt0.translate(0, length * 0.5, 0),
                                         wf_pt1.translate(0, -length * 0.5, 0),
                                         wf_pt1.translate(0, length * 0.5, 0)],
                                         self.tw, 'x')
            flange_pl1 = self.extrude_plate([wf_pt2.translate(0, -length * 0.5, 0),
                                             wf_pt2.translate(0, length * 0.5, 0),
                                             wf_pt3.translate(0, -length * 0.5, 0),
                                             wf_pt3.translate(0, length * 0.5, 0)],
                                             self.tf, 'z')
            flange_pl2 = self.extrude_plate([wf_pt4.translate(0, -length * 0.5, 0),
                                             wf_pt4.translate(0, length * 0.5, 0),
                                             wf_pt5.translate(0, -length * 0.5, 0),
                                             wf_pt5.translate(0, length * 0.5, 0)],
                                             self.tf, 'z')
            meshes = [web_pl, flange_pl1, flange_pl2]
        return meshes





if __name__ == "__main__":
    aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
    w40x593 = SteelMember.from_AISC_database(section_name="W40X593", AISCDatabase=aisc_db)
    test = w40x593.x_section_to_mesh('xz', 10*12)
    print(test[0])