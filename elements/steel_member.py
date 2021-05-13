import json
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import translate_points
from compas.geometry import Transformation
from numpy import radians


class SteelMember(object):

    def __init__(self, section_name, start_pt=None, end_pt=None,
                 frame=None,
                 length=None,
                 connection_length=None,
                 orientation='strong-axis',
                 ):
        self.section_name = section_name
        self.start_pt = start_pt
        self.end_pt = end_pt
        self._frame = frame
        self.connection_length = connection_length
        self.length = length
        self.orientation = orientation

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value is None:
            self._frame = Frame.worldXY()
        if 'euler_angles' in value:
            if 'point' in value:
                self._frame = Frame.from_euler_angles(
                                        radians(value['euler_angles']),
                                        value['point'])
            self._frame = Frame.from_euler_angles(
                                        radians(value['euler_angles']))
        else:
            point = value[0]
            xaxis = value[1]
            yaxis = value[2]
            self._frame = Frame(point, xaxis, yaxis)

    @property
    def start_pt(self):
        return self._start_pt

    @start_pt.setter
    def start_pt(self, value):
        if value is None:
            self._start_pt = Point(0, 0, 0)
        else:
            self._start_pt = Point(*value)

    @property
    def end_pt(self):
        return self._end_pt

    @end_pt.setter
    def end_pt(self, value):
        if value is None:
            self._end_pt = Point(100, 0, 0)
        else:
            self._end_pt = Point(*value)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if value is not None:
            self._length = value
        elif self.start_pt is not None and self.end_pt is not None:
            self._length = self.start_pt.distance_to_point(self.end_pt)
        else:
            self._length = 100

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
    def from_AISC_database(cls, section_name,  AISCDatabase, data=None,
                           **kwargs):
        steel_member = cls(section_name)
        for _, member in AISCDatabase.data.items():
            if member['AISC_Manual_Label'] == section_name:
                for member, prop in member.items():
                    setattr(steel_member, member, prop)
        if data:
            for key, value in data.items():
                setattr(steel_member, key, value)
        # set other attributes
        for key, value in kwargs.items():
            setattr(steel_member, key, value)
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

    def create_plate_xy(self, pt0, pt1, length):
        c0, c2 = translate_points([pt0, pt1], Vector(0, 0, 0))
        c1, c3 = translate_points([pt0, pt1], Vector(0, 0, length))

        return [Point(*c0), Point(*c1), Point(*c2), Point(*c3)]

    def to_local_geometry_xy(self):
        if self.Type == 'W':
            # wf == 'wireframe - center line of steel element, with origin at middle'
            wf_pt0 = Point(0, self.d * 0.5 - self.tw * 0.5, 0)
            wf_pt1 = Point(0, -(self.d * 0.5 - self.tw * 0.5), 0)
            wf_pt2 = translate_points([wf_pt0], Vector(-self.bf * 0.5, 0, 0))[0]
            wf_pt3 = translate_points([wf_pt0], Vector(self.bf * 0.5, 0, 0))[0]
            wf_pt4 = translate_points([wf_pt1], Vector(-self.bf * 0.5, 0, 0))[0]
            wf_pt5 = translate_points([wf_pt1], Vector(self.bf * 0.5, 0, 0))[0]

            wf_pt2 = Point(*wf_pt2)
            wf_pt3 = Point(*wf_pt3)
            wf_pt4 = Point(*wf_pt4)
            wf_pt5 = Point(*wf_pt5)

            web_surf = self.create_plate_xy(wf_pt0, wf_pt1, self.length)
            top_flange_srf = self.create_plate_xy(wf_pt2, wf_pt3, self.length)
            bottom_flange_srf = self.create_plate_xy(wf_pt4, wf_pt5, self.length)
            web_pl = self.extrude_plate(web_surf, self.tw, 'x')
            top_flange = self.extrude_plate(top_flange_srf, self.tf, 'y')
            bottom_flange = self.extrude_plate(bottom_flange_srf, self.tf, 'y')
            return [web_pl, top_flange, bottom_flange]
        if self.Type == 'HSS':
            raise NotImplementedError
        else:
            raise NotImplementedError

    def to_global_geometry(self, world_frame=Frame.worldXY()):
        geometry = self.to_local_geometry_xy()
        transformed_geometry = []
        T = Transformation.from_frame_to_frame(self.frame, world_frame)
        for part in geometry:
            transformed_part = []
            for point in part:
                p_point = Point(point['x'], point['y'], point['z'])
                transformed_part.append(p_point.transformed(T))
            transformed_geometry.append(transformed_part)
        return transformed_geometry


if __name__ == "__main__":
    from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
    import json

    aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
    with open('../examples/sample_node.json', 'r') as fp:
        data = json.load(fp)
    beam = SteelMember.from_AISC_database("W24X62", aisc_db, data=data['beams']["W24X62"])
    column = SteelMember.from_AISC_database("W14X370", aisc_db, data=data['column']['W14X370'])
    brace = SteelMember.from_AISC_database("W14X193", aisc_db, data=data['braces']['W14X193'])
