__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'

class GussetPlate(object):

    def __init__(self, quadrant='i', brace_angle, brace,
                 column, column_orientation, beam):
        self.quadrant = 'i'
        self.brace_angle = self.adjust_brace_angle(brace_angle)
        self.brace = brace
        self.column = column
        self.column_orientation = column_orientation
        self.beam = beam
        
    def adjust_brace_angle(self, brace_angle):
        '''
        Adjust brace angle for gusset plates in quadrant iii and iv
        '''
        if brace_angle > 180 or brace_angle < 0:
            raise ValueError
        if brace_angle > 90:
            brace_angle = 180 - brace_angle

    def calculate_eb(self, eb=None):
        if eb:
            self.eb = eb
        else:
            eb = self.beam.d * 0.5
        return eb

    def calculate_ec(self, ec=None):
        if ec:
            self.ec = ec
            return ec
        elif orientation:
            if column_orientation == 'strong axis':
                return self.column.d * 0.5
            if column_orientation == 'weak axis':
                return self.column.bf * 0.5
        else:
            raise ValueError


    def calculate_beta_bar(self):
        pass

    def calculate_alpha_bar(self):
        pass

    def calculate_K_prime(self):
        pass

    def calculate_D(self):
        pass

    def calculate_K(self):
        pass

    def calculate_beta(self):
        pass

    def calculate_alpha(self):
        pass

    def calculate_r(self):
        pass

    # utilize geometric limits

if __name__ == "__main__":

