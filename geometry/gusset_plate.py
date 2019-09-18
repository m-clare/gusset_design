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
        self._eb = None
        self._ec = None
        self._beta_bar = None
        self._alpha_bar = None
        self._K_prime = None
        self._K = None
        self._D = None
        self._beta = None
        self._alpha = None
        self._r = None

    @property
    def brace_angle(self):
        '''
        Adjust brace angle for gusset plates in quadrant iii and iv
        '''
        if self._brace_angle > 180 or self._brace_angle < 0:
            raise ValueError
        if self._brace_angle > 90:
            self._brace_angle = 180 - self._brace_angle
        return self._brace_angle

    @brace_angle.setter
    def brace_angle(self, value):
        self._brace_angle = value

    @property
    def eb(self):  # NEED TO ADD IN OPTION FOR SETTING eb in definition
        if self._beam.Type == 'HSS':
            self._eb = self._beam.Ht * 0.5
        else:
            self._eb = self._beam.d * 0.5
        return self._eb

    @property
    def ec(self):
        if self._column_orientation == 'strong axis':
            self._ec = self._column.d * 0.5
        if self._column_orientation == 'weak axis':
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
        self._K_prime = self.alpha_bar * tan(radians(self.brace_angle)) + \
                       self.alpha_bar / self.beta_bar
        return self._K_prime

    @property
    def D(self):
        self._D = tan(radians(self.brace_angle)) ** 2. + \
                 (self.alpha_bar / self.beta_bar) ** 2.
        return self._D

    @property
    def K(self):
        self._K = self.eb * tan(radians(self.brace_angle)) - self.ec
        return self._K

    @property
    def beta(self):
        self._beta = self.K_prime - \
                    self.K * tan(radians(self.brace_angle)) / self.D
        return self._beta

    @property
    def alpha(self):
        self._alpha = (self.K_prime * tan(radians(self.brace_angle)) +
                       self.K * (self.alpha_bar / self.beta_bar) ** 2.) \
                      / self.D
        return self._alpha

    @property
    def r(self):
        self._r = ((self.alpha + self.ec) ** 2. +
                   (self.beta + self.eb) ** 2.) ** 0.5

    # utilize geometric limits

if __name__ == "__main__":
    pass

