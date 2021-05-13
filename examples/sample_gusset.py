from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.elements.steel_member import SteelMember
from gusset_design.elements.gusset_plate import GussetPlate
from gusset_design.visualization.mesh import PlateMesh
import plotly.graph_objs as go
from compas.geometry import Frame
from numpy import radians
from compas.geometry import Transformation
from compas.geometry import Frame
from gusset_design.visualization.plotly2D import PlotlyLineXY

f1 = Frame([1, 0, 0], [0, 1, 0], [0, 0, 1])
f2 = Frame([0, 0, 1], [0, 1, 0], [-1, 0, 0])
T = Transformation.from_frame_to_frame(f1, f2)

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
                                       connection_length=31.,
                                       AISCDatabase=aisc_db)

gusset = GussetPlate(brace, column, beam, 'i', 24.5, 34., 1., brace_angle=37.6)

force_dict = gusset.calculate_interface_forces(400., as_dict=True)
print(force_dict)


# gusset.frame = Frame.from_euler_angles([radians(90), 0, radians(90)])
# gusset.frame = column.frame
# print(column.orientation)
gusset_geo = gusset.to_global_geometry()
gusset_lines = gusset.to_plotly_xy()

gusset_line_data = []
for line in gusset_lines:
    if gusset_lines.index(line) == 0:
        line_info = PlotlyLineXY.from_geometry(line)
    else:
        line_info = PlotlyLineXY.from_geometry(line, line={'color':'gray', 
            'dash':'dash'})
    gusset_line_data.append(line_info)

print(len(gusset_lines))
fig = go.Figure(data=gusset_line_data)
# colorway = ['gray'] * (len(gusset_lines) - 1)
# colorway.insert(0, 'black')
# fig.update_data(mode='lines')
fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  showlegend=False)
fig.update_xaxes(showgrid=False, zeroline=False)
fig.update_yaxes(showgrid=False, zeroline=False)
fig.show()

mesh_info = []
col_geo = column.to_global_geometry()
beam_geo = beam.to_global_geometry()
brace_geo = brace.to_global_geometry()
# print(col_geo)
# print(len(col_geo))
# print(len(beam_geo))
# print(len(brace_geo))

# print(gusset.ec)
# print(column.bf * 0.5)
# print(column.d * 0.5)

# print(gusset.gusset_lines)

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
fig = go.Figure(data=[gusset_data])
fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
fig.show()
