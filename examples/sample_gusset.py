from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.members.steel_member import SteelMember
from gusset_design.elements.gusset_plate import GussetPlate

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam = SteelMember.from_AISC_database('W24X94', start_pt=[0, 0, 0], end_pt=[120, 0, 0], AISCDatabase=aisc_db)
column = SteelMember.from_AISC_database('W14X257', start_pt=[0, 0, -100], end_pt=[0, 0, 100], AISCDatabase=aisc_db)
brace = SteelMember.from_AISC_database('W24X94', start_pt=[0, 0, 0], end_pt=[100, 100, 0], AISCDatabase=aisc_db)


gusset = GussetPlate('i', 24.5, 28., 18, brace, column, beam)
force = gusset.calculate_interface_forces(861, as_dict=True)

print(gusset.get_gusset_points())
