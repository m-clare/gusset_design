from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.members.structural_member import StructuralMember
from gusset_design.elements.gusset_plate import GussetPlate

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam = StructuralMember.from_AISC_database('W24X94', aisc_db)
column = StructuralMember.from_AISC_database('W14X257', aisc_db)
brace = StructuralMember.from_AISC_database('HSS10X10X5/16', aisc_db)
gusset = GussetPlate('i', 24.5, 28., brace, 'strong axis', 42.3, column, 'strong axis', beam)

print(gusset.__dict__)
print(gusset.r)
force = gusset.calculate_interface_forces(861, as_dict=True)
print(gusset.pt6)