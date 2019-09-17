from gusset_design.reference.AISC_shapes_database import AISCShapesDatabase
from gusset_design.members.structural_member import StructuralMember

aisc_db = AISCShapesDatabase.from_json('../reference/aisc_shapes_database_v15.json')
beam = StructuralMember.from_AISC_database()
