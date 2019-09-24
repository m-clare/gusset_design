from gusset_design.members.steel_member import SteelMember
from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.visualization.mesh import PlateMesh
from compas.geometry import Frame
from numpy import radians

import plotly.graph_objects as go

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam_frame = Frame.from_euler_angles([0, 0, 0])
beam = SteelMember.from_AISC_database(section_name="W18X55",
                                      frame=beam_frame,
                                      start_pt=[0, 0, 0],
                                      end_pt=[120, 0, 0],
                                      AISCDatabase=aisc_db)
beam_frame2 = Frame.from_euler_angles([0, radians(90), 0])
beam2 = SteelMember.from_AISC_database(section_name="W18X55",
                                      frame=beam_frame2,
                                      start_pt=[0, 0, 0],
                                      end_pt=[120, 0, 0],
                                      AISCDatabase=aisc_db)

brace_frame = Frame.from_euler_angles([radians(45), 0, 0])
brace = SteelMember.from_AISC_database(section_name="W18X55",
                                       frame=brace_frame,
                                       start_pt=[0, 0, 0],
                                       end_pt=[120, 120, 0],
                                       AISCDatabase=aisc_db)
column = SteelMember.from_AISC_database(section_name="W18X55",
         frame=[[0, 0, 120], [1., 0, 0], [0, 0, -1]],
         start_pt=[0, -120, 0],
         end_pt=[0, 120, 0],
         AISCDatabase=aisc_db)
test_mesh_info = []
print(beam.length)
column_meshes = column.to_local_mesh_xy()
beam_meshes = beam.to_local_mesh_xy()
beam2_meshes = beam2.to_local_mesh_xy()
brace_meshes = brace.to_local_mesh_xy()
test = column.to_global_mesh(column_meshes)
test2 = beam.to_global_mesh(beam_meshes)
test3 = brace.to_global_mesh(brace_meshes)
test4 = beam2.to_global_mesh(beam2_meshes)
for part in test:
    new_part = PlateMesh.from_geometry(part)
    test_mesh = new_part.to_dict()
    test_mesh_info.append(test_mesh)
for part in test2:
    new_part = PlateMesh.from_geometry(part)
    test_mesh = new_part.to_dict()
    test_mesh_info.append(test_mesh)
for part in test3:
    new_part = PlateMesh.from_geometry(part)
    test_mesh = new_part.to_dict()
    test_mesh_info.append(test_mesh)
for part in test4:
    new_part = PlateMesh.from_geometry(part)
    test_mesh = new_part.to_dict()
    test_mesh_info.append(test_mesh)


fig = go.Figure(data=test_mesh_info)
fig.update_layout(scene_aspectmode='data'
                  )
fig.show()
