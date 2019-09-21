from gusset_design.members.steel_member import SteelMember
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.visualization.mesh import PlateMesh
import plotly.graph_objects as go

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
w40x593 = SteelMember.from_AISC_database(section_name="W18X55", AISCDatabase=aisc_db)
test = w40x593.x_section_to_mesh('xz', 10*12)
test2 = w40x593.x_section_to_mesh('xy', 10*12)
test_mesh_info = []
for part in test:
    print(part)
    new_part = PlateMesh.from_geometry(part)
    test_mesh = new_part.to_dict()
    test_mesh_info.append(test_mesh)
for part in test2:
    new_part = PlateMesh.from_geometry(part)
    test_mesh = new_part.to_dict()
    test_mesh_info.append(test_mesh)

fig = go.Figure(data=test_mesh_info)
fig.update_layout(scene_aspectmode='data'
                  )
fig.show()
