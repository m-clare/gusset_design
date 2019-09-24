import plotly.graph_objects as go


class PlateMesh(object):

    def __init__(self, x=None, y=None, z=None):

        self._type = 'mesh3d'
        self.x = x
        self.y = y
        self.z = z
        self._alphahull = 0
        self._color = 'grey'

    @property
    def type(self):
        return self._type
    
    @property
    def alphahull(self):
        return self._alphahull

    @property
    def color(self):
        return self._color

    @classmethod
    def from_geometry(cls, points):
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

    def to_plotly_go(self):
        pass






if __name__ == "__main__":
    x = [7, 7, 10, 15, 33, 31, 31, 7, 7, 10, 15, 33, 31, 31]
    y = [12, 38.5, 38.5, 48, 38, 15, 12, 12, 38.5, 38.5, 48, 38, 15, 12]
    z = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    test = PlateMesh(x, y, z)

    # fig = go.Figure(data=[test.mesh])
    fig = go.Figure(data=[test.mesh])
    print(fig._data)
    fig.show()