import plotly.graph_objects as go


class PlateMesh(object):

    def __init__(self, x=None, y=None, z=None):

        self._type = 'mesh3d'
        self._x = x
        self._y = y
        self._z = z
        self._alphahull = 0
        self._color = 'grey'

    @property
    def type(self):
        return self._type

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    @property
    def alphahull(self):
        return self._alphahull

    @property
    def color(self):
        return self._color

    @classmethod
    def from_geometry(cls, points, to_dict=False):
        plate = cls()
        x = []
        y = []
        z = []
        for point in points:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        plate.x = x
        plate.y = y
        plate.z = z
        if to_dict:
            return plate.to_dict()
        else:
            return plate

    @classmethod
    def from_data(cls):
        pass

    @classmethod
    def from_json(cls):
        pass

    def to_dict(self):
        return dict(type=self.type,
                    x=self.x, y=self.y, z=self.z,
                    alphahull=self.alphahull, color=self.color)






if __name__ == "__main__":
    x = [7, 7, 10, 15, 33, 31, 31, 7, 7, 10, 15, 33, 31, 31]
    y = [12, 38.5, 38.5, 48, 38, 15, 12, 12, 38.5, 38.5, 48, 38, 15, 12]
    z = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    test = PlateMesh(x, y, z)

    # fig = go.Figure(data=[test.mesh])
    fig = go.Figure(data=[test.mesh])
    print(fig._data)
    fig.show()