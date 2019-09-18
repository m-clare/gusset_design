from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.members.structural_member import StructuralMember
from gusset_design.geometry.gusset_plate import GussetPlate

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam = StructuralMember.from_AISC_database('W16X26', aisc_db)
column = StructuralMember.from_AISC_database('W14X145', aisc_db)
brace = StructuralMember.from_AISC_database('HSS10X10X5/16', aisc_db)
gusset = GussetPlate('i', 36., 36., 125, brace, column, 'strong axis', beam)
