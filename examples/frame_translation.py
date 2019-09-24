from compas.geometry import Transformation
from compas.geometry import Frame

f1 = Frame([1, 0, 0], [0, 1, 0], [0, 0, 1])
f2 = Frame([0, 0, 1], [0, 1, 0], [-1, 0, 0])
T = Transformation.from_frame_to_frame(f1, f2)
print(T)