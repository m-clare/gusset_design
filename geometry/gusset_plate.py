from numpy import tan
from numpy import radians

__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


class GussetPlate(object):

    def __init__(self, quadrant, width, height, brace_angle, brace,
                 column, column_orientation, beam):
        self._quadrant = quadrant
        self._brace_angle = brace_angle
        self._brace = brace
        self._column = column
        self._column_orientation = column_orientation
        self._beam = beam
        self._width = width
        self._height = height

    # Properties

    @property
    def brace_angle(self):
        return self._brace_angle

    @brace_angle.setter
    def set_brace_angle(self, value):
        self._brace_angle = value

    @property
    def column_orientation(self):
        return self._column_orientation

    @column_orientation.setter
    def set_column_orientation(self, value):
        self._column_orientation = value

    @property
    def design_angle(self):
        '''
        Adjust brace angle for gusset plates in quadrant iii and iv
        '''
        if self.brace_angle > 180 or self.brace_angle < 0:
            raise ValueError
        if self.brace_angle > 90:
            self._design_angle = 180 - self.brace_angle
        else:
            self._design_angle = self.brace_angle
        return self._design_angle

    @property
    def eb(self):  # NEED TO ADD designTION FOR SETTING eb in definition
        if self._beam.Type == 'HSS':
            self._eb = self._beam.Ht * 0.5
        else:
            self._eb = self._beam.d * 0.5
        return self._eb

    @property
    def ec(self):
        if self.column_orientation == 'strong axis':
            self._ec = self._column.d * 0.5
        if self.column_orientation == 'weak axis':
            self._ec = self._column.bf * 0.5
        return self._ec

    @property
    def beta_bar(self):
        self._beta_bar = self._height * 0.5
        return self._beta_bar

    @property
    def alpha_bar(self):
        self._alpha_bar = self._width * 0.5
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

    # Methods
    def calculate_column_interface_forces(self, brace_force, as_dict=False):
        V_c = self.beta * brace_force / self.r
        H_c = self.ec * brace_force / self.r
        M_c = H_c * (self.beta - self.beta_bar)
        if as_dict:
            return {'V_c': V_c, 'H_c': H_c, 'M_c': M_c}
        return V_c, H_c, M_c

    def calculate_beam_interface_forces(self, brace_force, as_dict=False):
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

    # utilize geometric limits

if __name__ == "__main__":
    pass

