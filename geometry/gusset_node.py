from structural_node import StructuralNode
from gusset_plate import GussetPlate

__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


class GussetNode(StructuralNode):

    def __init__(self):
        super(GussetNode, self).__init__()

    def from_json():
        pass

    def to_json():
        pass

    def add_gusset():
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

if __name__ == "__main__":
    test = GussetNode()
    print(test.__dict__)