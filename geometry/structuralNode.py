__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


class StructuralNode(object):

    def __init__(self, x=0.0, y=0.0, z=0.0, planes={}):
        self.x = x
        self.y = y
        self.z = z
        self.planes = planes

    def get_e_c(column_depth):
    	return 0.5 * column_depth
    	pass

    def get_e_b(beam_depth):
    	pass

    def get_horizontal_gusset_force():
    	pass

    def


if __name__ == "__main__":
    test = StructuralNode(x=1.0, y=1.0, z=1.0)
    print(test.__dict__)