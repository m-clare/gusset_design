import json
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import translate_points
from compas.geometry.xforms.transformation import Transformation

class SteelMember(object):

    def __init__(self, name, start_pt=None, end_pt=None,
                frame=None,
                length=None,
                orientation='strong-axis',
                 d=None, tw=None, bf=None, tf=None):
        self.name = name
        self.start_pt = Point(start_pt[0], start_pt[1], start_pt[2])
        self.end_pt = Point(end_pt[0], end_pt[1], end_pt[2])
        self.frame = frame
        self.length = length
        self.orientation = orientation
        self.tf = tf
        self.tw = tw
        self.d = d
        self.bf = bf

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value == None:
            self._frame = Frame.worldXY()
        else:
            point = value[0]
            xaxis = value[1]
            yaxis = value[2]
            self._frame = Frame(point, xaxis, yaxis)

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        if value is not None:
            self._length = value
        if self.start_pt is not None and self.end_pt is not None:
            self._length = self.start_pt.distance_to_point(self.end_pt)
        else:
            self._length = 100.



    
    @classmethod
    def from_data(cls, data):
        steel_member = cls()

    @classmethod
    def from_json(cls, filepath):
        steel_member = cls()
        with open(filepath, 'r') as fp:
            data = json.load(fp)
            for k, v in data.items():
                setattr(steel_member, k, v)
        return steel_member

    @classmethod
    def from_AISC_database(cls, section_name,  AISCDatabase,
                           frame=None,
                           start_pt=None, end_pt=None):
        steel_member = cls(section_name, start_pt, end_pt, frame)
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
                mesh_Point3D.append(translate_points([pt], Vector(-0.5 * thickness, 0, 0))[0])
                mesh_Point3D.append(translate_points([pt], Vector(0.5 * thickness, 0, 0))[0])
        if direction == 'y':
            for pt in pts:
                mesh_Point3D.append(translate_points([pt], Vector(0, -0.5 * thickness, 0))[0])
                mesh_Point3D.append(translate_points([pt], Vector(0, 0.5 * thickness, 0))[0])
        if direction == 'z':
            for pt in pts:
                mesh_Point3D.append(translate_points([pt], Vector(0, 0, -0.5 * thickness))[0])
                mesh_Point3D.append(translate_points([pt], Vector(0, 0, 0.5 * thickness))[0])
        for pt in mesh_Point3D:
            mesh_points.append({'x': float(pt[0]), 'y': float(pt[1]), 'z': float(pt[2])})
        return mesh_points

    def create_plate(self, pt0, pt1, length):
        c0, c2 = translate_points([pt0, pt1], Vector(0, 0, 0))
        c1, c3 = translate_points([pt0, pt1], Vector(0, 0, length))

        # make into points --- this should be a feature in the Point class WTF
        c0 = Point(c0[0], c0[1], c0[2])
        c1 = Point(c1[0], c1[1], c1[2])
        c2 = Point(c2[0], c2[1], c2[2])
        c3 = Point(c3[0], c3[1], c3[2])
        return [c0, c1, c2, c3]
       
    def to_local_mesh_xy(self):
        if self.Type == 'W':
            # wf == 'wireframe - center line of steel element, with origin at middle'
            wf_pt0 = Point(0, self.d * 0.5 - self.tw * 0.5, 0)
            wf_pt1 = Point(0, -(self.d * 0.5 - self.tw * 0.5), 0)
            wf_pt2 = translate_points([wf_pt0], Vector(-self.bf * 0.5, 0, 0))[0]
            wf_pt3 = translate_points([wf_pt0], Vector(self.bf * 0.5, 0, 0))[0]
            wf_pt4 = translate_points([wf_pt1], Vector(-self.bf * 0.5, 0, 0))[0]
            wf_pt5 = translate_points([wf_pt1], Vector(self.bf * 0.5, 0, 0))[0]

            wf_pt2 = Point(wf_pt2[0], wf_pt2[1], wf_pt2[2])
            wf_pt3 = Point(wf_pt3[0], wf_pt3[1], wf_pt3[2])
            wf_pt4 = Point(wf_pt4[0], wf_pt4[1], wf_pt4[2])
            wf_pt5 = Point(wf_pt5[0], wf_pt5[1], wf_pt5[2])

            web_surf = self.create_plate(wf_pt0, wf_pt1, self.length)
            top_flange_srf = self.create_plate(wf_pt2, wf_pt3, self.length)
            bottom_flange_srf = self.create_plate(wf_pt4, wf_pt5, self.length)
            web_pl = self.extrude_plate(web_surf, self.tw, 'x')
            top_flange = self.extrude_plate(top_flange_srf, self.tf, 'y')
            bottom_flange = self.extrude_plate(bottom_flange_srf, self.tf, 'y')
            return [web_pl, top_flange, bottom_flange]
        if self.Type == 'HSS':
            raise NotImplementedError
        else:
            raise NotImplementedError

    def to_global_mesh(self, meshes,
                       world_frame=Frame.worldXY()):
        transformed_meshes = []
        T = Transformation.from_frame_to_frame(self.frame, world_frame)
        for mesh in meshes:
            transformed_mesh = []
            for point in mesh:
                p_point = Point(point['x'], point['y'], point['z'])
                transformed_mesh.append(p_point.transformed(T))
            transformed_meshes.append(transformed_mesh)
        return transformed_meshes










if __name__ == "__main__":
    pass
    # aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
    # w40x593 = SteelMember.from_AISC_database(section_name="W40X593", AISCDatabase=aisc_db)
    # test = w40x593.x_section_to_mesh('xz', 10*12)
    # print(test[0])