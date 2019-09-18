# Gusset Plate Design and Visualization General Notes

## Attributes
- Grid Intersection
- Level
- Quadrant + Brace Angle (8 possible)
- Forces (global) - horizontal and vertical

## Failure States/Checks
- Axial force +/-
- Moment
- In Plane Shear
- OOP Shear
- Whitmore section
- Stress Interaction (Von Mises?)
- Shear and Moment DCR
- Web local yielding - J10.2
- Web local crippling - J10.3
- Column interface stresses

## Geometric/Material Limits
- plate thicknesses
- 3 inch offset thing? how is this codified

## Visualization Notes
- include visualization of geometry parameters for design
- 3D potential visualization
- quadrants based on XY plane 

### Design Guide Notes
- KISS Method - all vertical force goes to column/gusset interface, all horizontal force goes to beam/gusset interface - not the most economical
- Parallel Force Method - 
- Uniform Force Method

### Geometric Constraints - Gusset Plates
- 3 inch offset for edge of gusset from column
- 3 inch offset for edge of gusset from beam
- 2 inch offset from column to brace connection
- 6 inch offset from beam to brace connection
- 3 inch offset either side of brace (shoulder)

### Geometric Constraints - Forces
- 3 Force Polygons
- alpha and beta are unknowns
- beam control point is fixed (x, y)
- H is known and line of action for H is known
- P is known and line of action for P is known
- V is known and line of action for V is known
