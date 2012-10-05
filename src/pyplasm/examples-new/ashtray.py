from pyplasm import *

# Outer cylinder:
Rout = 0.10
Hout = 0.03
cyl_outer = CYLINDER(Rout, Hout, 128)

# Inner cylinder
Rin = 0.08
bt = 0.005
cyl_inner = CYLINDER(Rin, Hout, 128)
cyl_inner = T(cyl_inner, 0, 0, bt)

# Subtract inner cylinder from outer:
out = DIFF(cyl_outer, cyl_inner)

# Tiny cylinder to cut off the radiuses:
Rtiny = 0.02
Htiny = 2 * Rout + 0.02
cyl = CYLINDER(Rtiny, Htiny)

# Lay the first cylinder horizontall over the ashtray:
cyl1 = T(cyl, 0, 0, -Htiny/2.)
cyl1 = R(cyl1, 2, PI/2)
cyl1 = T(cyl1, 0, 0, Rtiny + Hout/2.0)

# Just rotate by 90 degrees about the z axis:
cyl2 = R(cyl1, 3, PI/2)

# Cutting off the radiuses at once
out = DIFF(out, cyl1, cyl2)
 
# Display the result:
VIEW(out)

# STL output:
import plasm_stl
plasm_stl.toSTL(out)
