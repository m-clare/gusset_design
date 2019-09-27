from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.elements.steel_member import SteelMember
from gusset_design.elements.gusset_plate import GussetPlate
from gusset_design.visualization.mesh import PlateMesh
import plotly.graph_objs as go
from compas.geometry import Frame
from numpy import radians


aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam_frame = Frame.from_euler_angles([radians(90), 0, 0])
beam = SteelMember.from_AISC_database('W24X62',
                                      frame=beam_frame,
                                      start_pt=[0, 0, 0],
                                      end_pt=[120, 0, 0],
                                      AISCDatabase=aisc_db)
column_frame = Frame.from_euler_angles([0, 0, radians(90)], point=[0, 0, 100])
column = SteelMember.from_AISC_database('W14X370',
                                        frame=column_frame,
                                        length=200.,
                                        start_pt=[0, 0, -100],
                                        end_pt=[0, 0, 100],
                                        AISCDatabase=aisc_db,
                                        orientation='weak-axis')
brace_frame = Frame.from_euler_angles([radians(37.6), 0, 0])
brace = SteelMember.from_AISC_database('W14X193',
                                       frame=brace_frame,
                                       start_pt=[0, 0, 0],
                                       end_pt=[100, 100, 0],
                                       AISCDatabase=aisc_db)
gusset = GussetPlate('i', 24.5, 34., 31, 1., brace, column, beam, brace_angle=37.6)

gusset.frame = beam.frame

gusset_geo = gusset.to_global_geometry()

mesh_info = []
col_geo = column.to_global_geometry()
beam_geo = beam.to_global_geometry()
brace_geo = brace.to_global_geometry()
print(col_geo)
print(len(col_geo))
print(len(beam_geo))
print(len(brace_geo))

geometries = [col_geo, beam_geo, brace_geo, gusset_geo]
# flatten geometries
meshes = []
for geometry in geometries:
    for part in geometry:
        new_mesh = PlateMesh.from_geometry(part, to_dict=True)
        meshes.append(new_mesh)




fig = go.Figure(data=meshes)
fig.update_layout(scene_aspectmode='data')
fig.show()

# gusset.set_brace_angle = 37.6
# print(gusset.gusset_points)

# gusset_data = gusset.to_plotly_xy()
# gusset_mesh = gusset.to_local_mesh()
# print(gusset_mesh)
# part = PlateMesh.from_geometry(gusset_mesh)
# test_part = part.to_dict()


# fig = go.Figure(data=[test_part])
# fig.update_layout(scene_aspectmode='data'
#                   )
# fig.show()
# fig = go.Figure(data=[gusset_data])
# fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
# fig.show()
