from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.members.steel_member import SteelMember
from gusset_design.elements.gusset_plate import GussetPlate
from gusset_design.visualization.mesh import PlateMesh
import plotly.graph_objs as go

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam = SteelMember.from_AISC_database('W24X62', start_pt=[0, 0, 0], end_pt=[120, 0, 0], AISCDatabase=aisc_db)
column = SteelMember.from_AISC_database('W14X370', start_pt=[0, 0, -100], end_pt=[0, 0, 100], AISCDatabase=aisc_db)
brace = SteelMember.from_AISC_database('W14X193', start_pt=[0, 0, 0], end_pt=[100, 100, 0], AISCDatabase=aisc_db)
column.orientation = 'weak-axis'

gusset = GussetPlate('i', 24.5, 34., 31, 1., brace, column, beam)
gusset.set_brace_angle = 37.6
print(gusset.gusset_points)

gusset_data = gusset.to_plotly_xy()
gusset_mesh = gusset.to_local_mesh()
print(gusset_mesh)
part = PlateMesh.from_geometry(gusset_mesh)
test_part = part.to_dict()


fig = go.Figure(data=[test_part])
fig.update_layout(scene_aspectmode='data'
                  )
fig.show()
# fig = go.Figure(data=[gusset_data])
# fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
# fig.show()
