from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.members.structural_member import StructuralMember

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam = StructuralMember.from_AISC_database('W16X26', aisc_db)
column = StructuralMember.from_AISC_database('W14X145', aisc_db)
brace = StructuralMember.from_AISC_database('HSS10X10X5/16', aisc_db)

print(brace.__dict__)
