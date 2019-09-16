from structuralNode import StructuralNode

__author__ = ['Maryanne Wachter', ]
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'mclare@utsv.net'
__status__ = 'Development'
__date__ = 'Sept 16, 2019'


class GussetNode(StructuralNode):

    def __init__(self, *args, **kwargs):
        super(StructuralNode, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    test = GussetNode(x=0, y=0, z=0)
    print(test.__dict__)