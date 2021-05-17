from numpy import tan
from numpy import sin
from numpy import cos
from numpy import radians

# Compas classes
from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Vector

# Compas methods
from compas.geometry import angle_points
from compas.geometry import translate_points_xy
from compas.geometry import translate_points
from compas.geometry import offset_line
from compas.geometry import intersection_line_line_xy
from compas.geometry import distance_point_point
from compas.geometry import mirror_points_line
from compas.geometry import Transformation

__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


class GussetPlate(object):

    def __init__(self, brace, column, beam,
                 quadrant='i', width=24, height=24,
                 thickness=0.5,
                 brace_angle=None,
                 frame=None,
                 eb=None,   # eb and ec currently do not work for
                 ec=None):  # overriding property declaration
        self._quadrant = quadrant
        self._work_point = [0, 0, 0]
        self._brace = brace
        self._column = column
        self._beam = beam
        self.frame = frame
        self._width = width
        self._height = height
        self._thickness = thickness
        self._eb = eb
        self._ec = ec
        self._gusset_points = []
        self._offset = 3.
        self._brace_CL = None
        self._brace_angle = brace_angle

        # Make these private?
        self.connection_length = self.brace.connection_length
        self.gusset_lines = []

    # Properties

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def thickness(self):
        return self._thickness

    @property
    def brace(self):
        return self._brace

    @property
    def column(self):
        return self._column

    @property
    def beam(self):
        return self._beam

    @property
    def work_point(self):
        return self._work_point

    @property
    def offset(self):  # -> Make as input
        return self._offset

    @property
    def brace_angle(self):
        return self._brace_angle

    @brace_angle.setter
    def brace_angle(self, value):
        if value is not None:
            self._brace_angle = value
        else:
            self._brace_angle = angle_points(self.column.end_pt,
                                             self.work_point,
                                             self.brace.end_pt, deg=True)

    @property
    def design_angle(self):
        '''
        Adjust brace angle for gusset plates in quadrant iii and iv
        Brace angle is measured from column line to brace line < 90 degrees
        '''
        if self.brace_angle > 180 or self.brace_angle < 0:
            raise ValueError
        if self.brace_angle > 90:
            self._design_angle = 180 - self.brace_angle
        else:
            self._design_angle = self.brace_angle
        return self._design_angle

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value is not None:
            self._frame = Frame(value[0], value[1], value[2])
        else:
            brace_frame = self.brace.frame
            self._frame = brace_frame

    @property
    def eb(self, value=None):
    '''
    Current setup is for CL of beam for handling eb
    '''
        if not value:
            if self._beam.Type == 'HSS':
                self._eb = self.beam.Ht * 0.5
            else:
                self._eb = self.beam.d * 0.5
        else:
            self._eb = value
        return self._eb

    @property
    def ec(self):
        if self.column.orientation == 'strong-axis':
            self._ec = self.column.d * 0.5
        if self.column.orientation == 'weak-axis':
            self._ec = self.column.bf * 0.5
        return self._ec

    @property
    def beta_bar(self):
        self._beta_bar = self.height * 0.5
        return self._beta_bar

    @property
    def alpha_bar(self):
        self._alpha_bar = self.width * 0.5
        return self._alpha_bar

    @property
    def K_prime(self):
        self._K_prime = self.alpha_bar * (tan(radians(self.design_angle)) +
                                          self.alpha_bar / self.beta_bar)
        return self._K_prime

    @property
    def D(self):
        self._D = tan(radians(self.design_angle)) ** 2. + \
                 (self.alpha_bar / self.beta_bar) ** 2.
        return self._D

    @property
    def K(self):
        self._K = self.eb * tan(radians(self.design_angle)) - self.ec
        return self._K

    @property
    def beta(self):
        self._beta = (self.K_prime -
                      self.K * tan(radians(self.design_angle))) / self.D
        return self._beta

    @property
    def alpha(self):
        self._alpha = (self.K_prime * tan(radians(self.design_angle)) +
                       self.K * (self.alpha_bar / self.beta_bar) ** 2.) \
                       / self.D
        return self._alpha

    @property
    def r(self):
        self._r = ((self.alpha + self.ec) ** 2. +
                   (self.beta + self.eb) ** 2.) ** 0.5
        return self._r

    def get_gusset_pts_and_guidelines(self):
        pt0 = list(Point(self.eb, self.ec))
        pt1 = translate_points_xy([pt0], Vector(self.width, 0, 0))[0]
        pt2 = translate_points_xy([pt1], Vector(0, self.offset, 0))[0]
        pt6 = translate_points_xy([pt0], Vector(0, self.height, 0))[0]
        pt5 = translate_points_xy([pt6], Vector(self.offset, 0, 0))[0]

    # Gusset geometry points
    @property
    def gusset_points(self):
    '''
    Gusset points defined in Q1 of XY plane: all transformation done wrt
    this system.
    '''

        pt0 = list(Point(self.eb, self.ec))
        pt1 = translate_points_xy([pt0], Vector(self.width, 0, 0))[0]
        pt2 = translate_points_xy([pt1], Vector(0, self.offset, 0))[0]
        pt6 = translate_points_xy([pt0], Vector(0, self.height, 0))[0]
        pt5 = translate_points_xy([pt6], Vector(self.offset, 0, 0))[0]

        # Brace CL
        brace_vector = Vector(sin(radians(self.design_angle)),
                              cos(radians(self.design_angle)), 0)
        brace_vector.unitize()
        brace_vector.scale(100)
        brace_pt = translate_points_xy([self.work_point], brace_vector)[0]
        test = brace_vector.copy()
        test.scale(1)
        brace_pt_out = translate_points_xy([self.work_point], test)[0]
        brace_CL = Line(self.work_point, brace_pt)


        self.gusset_lines.append(Line(self.work_point, brace_pt_out))

        brace_vector.unitize()
        brace_vector.scale(self.connection_length)


        # Brace shoulder lines
        brace_depth = self.get_brace_depth()
        column_offset = brace_depth * 0.5 + self.offset
        beam_offset = -(brace_depth * 0.5 + self.offset)
        column_line = Line(pt5, Point(pt5[0], 0, 0))
        beam_line = Line(pt2, Point(0, pt2[1], 0))

        self.gusset_lines.append(column_line)
        self.gusset_lines.append(beam_line)

        def get_brace_points(offset_value, offset_member,
                             brace_CL, brace_vector, offset_dir='+'):
            offset_brace = offset_line(brace_CL, offset_value)
            if offset_dir == '+':
                offset_brace_signed = offset_line(brace_CL, offset_value - self.offset)
            elif offset_dir == '-':
                offset_brace_signed = offset_line(brace_CL, offset_value + self.offset)
            else: 
                raise ValueError

            brace_member_int = intersection_line_line_xy(offset_brace,
                                                         offset_member)
            brace_pt = translate_points_xy([brace_member_int], brace_vector)[0]
            pt_mirrored = mirror_points_line([brace_pt], brace_CL)
            line_segment = Line(brace_pt, pt_mirrored)
            pt_CL = intersection_line_line_xy(line_segment, brace_CL)
            pt_distance = distance_point_point(self.work_point, pt_CL)
            return line_segment, pt_distance, offset_brace, offset_brace_signed

        column_line, col_dist, os_brace_column, os_column = get_brace_points(column_offset, column_line,
                                                 brace_CL, brace_vector, offset_dir='+')
        beam_line, beam_dist, os_brace_beam, os_beam = get_brace_points(beam_offset, beam_line,
                                                brace_CL, brace_vector, offset_dir='-')

        self.gusset_lines.append(os_brace_column)
        self.gusset_lines.append(os_brace_beam)
        self.gusset_lines.append(os_column)
        self.gusset_lines.append(os_beam)
        self.gusset_lines.append(column_line)
        self.gusset_lines.append(beam_line)

        if col_dist > beam_dist:
            pt3 = column_line[1]
            pt4 = column_line[0]
        else:
            pt3 = beam_line[0]
            pt4 = beam_line[1]

        # TODO: set check to make sure gusset is non concave
        # (i.e. force points to line between pt2 and pt5)
        # Points list to point
        pt0 = Point(pt0[0], pt0[1], pt0[2])
        pt1 = Point(pt1[0], pt1[1], pt1[2])
        pt2 = Point(pt2[0], pt2[1], pt2[2])
        pt6 = Point(pt6[0], pt6[1], pt6[2])
        pt5 = Point(pt5[0], pt5[1], pt5[2])

        self._gusset_points = [pt0, pt1, pt2, pt3, pt4, pt5, pt6]
        return self._gusset_points

    # Methods
    def calculate_column_interface_forces(self, brace_force, as_dict=False):
    '''
    Column interface forces assume moments at interfaces per
    Analysis of Existing Diagonal Brace Connections AISC Steel Manual 13-10
    '''
        V_c = self.beta * brace_force / self.r
        H_c = self.ec * brace_force / self.r
        M_c = H_c * (self.beta - self.beta_bar)
        if as_dict:
            return {'V_c': V_c, 'H_c': H_c, 'M_c': M_c}
        return V_c, H_c, M_c

    def calculate_beam_interface_forces(self, brace_force, as_dict=False):
    '''
    Beam interface forces assume moments at interfaces per
    Analysis of Existing Diagonal Brace Connections AISC Steel Manual 13-10
    '''
        V_b = self.eb * brace_force / self.r
        H_b = self.alpha * brace_force / self.r
        M_b = V_b * (self.alpha - self.alpha_bar)
        if as_dict:
            return {'V_b': V_b, 'H_b': H_b, 'M_b': M_b}
        return V_b, H_b, M_b

    def calculate_interface_forces(self, brace_force, as_dict=False):
        V_c, H_c, M_c = self.calculate_column_interface_forces(brace_force)
        V_b, H_b, M_b = self.calculate_beam_interface_forces(brace_force)
        if as_dict:
            return {'V_c': V_c, 'H_c': H_c, 'M_c': M_c,
                    'V_b': V_b, 'H_b': H_b, 'M_b': M_b}
        return V_c, H_c, M_c, V_b, H_b, M_b

    def get_brace_depth(self):
        if self.brace.orientation == 'strong-axis':
            if self.brace.Type == 'W':
                return self.brace.d
            if self.brace.Type == 'HSS':
                return self.brace.Ht
        if self.brace.orientation == 'weak-axis':
            if self.brace.Type == 'W':
                return self.brace.bf
            if self.brace.Type == 'HSS':
                return self.brace.B
        else:
            raise ValueError

    def to_plotly_xy(self):
        x, y = [], []
        for point in self.gusset_points:
            x.append(point[0])
            y.append(point[1])
        x.append(x[0])
        y.append(y[0])
        gusset_guidelines = []
        gusset_data = {'x': x, 'y': y}
        gusset_guidelines.append(gusset_data)
        for line in self.gusset_lines:
            pt0 = line[0]
            pt1 = line[1]
            gusset_guideline = {'x': [pt0[0], pt1[0]], 'y': [pt0[1], pt1[1]]}
            gusset_guidelines.append(gusset_guideline)
        return gusset_guidelines

    def to_local_geometry_xy(self):
        mesh_Point3D = []
        mesh_points = []
        for pt in self.gusset_points:
            mesh_Point3D.append(translate_points([pt], Vector(0, 0, -0.5 * self.thickness))[0])
            mesh_Point3D.append(translate_points([pt], Vector(0, 0, 0.5 * self.thickness))[0])
        for pt in mesh_Point3D:
            mesh_points.append({'x': float(pt[0]), 'y': float(pt[1]), 'z': float(pt[2])})
        return [mesh_points]

    def to_global_geometry(self, world_frame=Frame.worldXY()):
        geometry = self.to_local_geometry_xy()
        transformed_geometry = []
        gusset_local_frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
        T1 = Transformation.from_frame_to_frame(gusset_local_frame, self.frame)
        T2 = Transformation.from_frame_to_frame(self.frame, world_frame)
        transformed_part = [] # default
        for part in geometry:
            transformed_part = []
            for point in part:
                p_point = Point(point['x'], point['y'], point['z'])
                transformed_part.append(p_point.transformed(T1))
        transformed_geometry.append(transformed_part)
        return transformed_geometry
