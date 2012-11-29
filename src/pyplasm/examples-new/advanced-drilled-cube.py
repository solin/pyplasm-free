from pyplasm import *

# Create a cube of size 2:
c = CUBE(2)
# Create a cylinder of radius 0.75 and height 4:
cyl = CYLINDER(0.75, 4)
# Translate the cube by -1 in each axial direction:
c = T(c, -1, -1, -1)
# Translate the cylinder by -2 in the z-direction:
cyl = T(cyl, 0, 0, -2)
# Subtract cylinder from the cube:
c = DIFF(c, cyl)
# Rotate the cylinder by 90 degrees about the x-axis:
cyl = R(cyl, 1, PI/2)
# Subtract the cylinder from the cube:
c = DIFF(c, cyl)
# Rotate the cylinder by 90 degrees about the z-axis:
cyl = R(cyl, 3, PI/2)
# Subtract the cylinder from the cube:
c = DIFF(c, cyl)
# View the result. 
VIEW(c)

# STL output:
import plasm_stl
filename = "drilled-cube.stl"
plasm_stl.toSTL(c, filename)
print "STL file written to", filename
