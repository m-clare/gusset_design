from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.members.steel_member import SteelMember
from gusset_design.elements.gusset_plate import GussetPlate
import plotly.graph_objs as go

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam = SteelMember.from_AISC_database('W24X62', start_pt=[0, 0, 0], end_pt=[120, 0, 0], AISCDatabase=aisc_db)
column = SteelMember.from_AISC_database('W14X370', start_pt=[0, 0, -100], end_pt=[0, 0, 100], AISCDatabase=aisc_db)
brace = SteelMember.from_AISC_database('W14X193', start_pt=[0, 0, 0], end_pt=[100, 100, 0], AISCDatabase=aisc_db)
column.orientation = 'weak-axis'

gusset = GussetPlate('i', 24.5, 34., 31, brace, column, beam)
gusset.set_brace_angle = 37.6
print(gusset.brace_angle)
print(gusset.design_angle)
force = gusset.calculate_interface_forces(861, as_dict=True)

test = gusset.gusset_points()
print(gusset.gusset_points)

x, y = gusset.to_plotly_xy()
fig = go.Figure(data=[{'x': x, 'y': y}])
fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
fig.show()
