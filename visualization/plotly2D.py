import plotly.graph_objects as go


class PlotlyLineXY(object):

    def __init__(self, x=None, y=None, line=None):

        self._type = 'scatter'
        self._x = x
        self._y = y
        self._line = line

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
    def line(self):
        return self._line

    @line.setter
    def line(self, line_dict):
        self._line = line_dict

    @property
    def dash(self):
        return self._dash

    @dash.setter
    def dash(self, value):
        self._dash = value
    
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @classmethod
    def from_geometry(cls, points, line={'dash': None, 'color': 'black'},
                      to_dict=True):
        lineXY = cls()
        x = points['x']
        y = points['y']
        lineXY.x = x
        lineXY.y = y
        lineXY.line = line
        if to_dict:
            return lineXY.to_dict()
        else:
            return lineXY

    @classmethod
    def from_data(cls):
        pass

    @classmethod
    def from_json(cls):
        pass

    def to_dict(self):
        return dict(type=self.type,
                    x=self.x, y=self.y,
                    line=self.line)
    