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

_, obc, obb, oc, ob, bls = gusset.gusset_points()
print(gusset.gusset_points)

x, y = gusset.to_plotly_xy()
fig = go.Figure(data=[{'x': x, 'y': y},
                      {'x': [obc[0][0], obc[1][0]],
                       'y': [obc[0][1], obc[1][1]]},
                       {'x': [obb[0][0], obb[1][0]],
                       'y': [obb[0][1], obb[1][1]]},
                       {'x': [oc[0][0], oc[1][0]],
                       'y': [oc[0][1], oc[1][1]]},
                       {'x': [ob[0][0], ob[1][0]],
                       'y': [ob[0][1], ob[1][1]]},
                       {'x': [bls[0][0], bls[1][0]],
                       'y': [bls[0][1], bls[1][1]]}])
fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
fig.show()
