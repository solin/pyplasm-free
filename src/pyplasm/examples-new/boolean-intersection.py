# Import PyPLaSM:
from pyplasm import *

# Intersection of three cylinders
# and a cube:
c = CUBE(2.0)
s = CYLINDER(1.0, 3.0)
s2 = R(s, 1, -PI/2)
s3 = R(s, 2, -PI/2)
out = I(c, s, s2, s3) 
VIEW(out)

# Strange object that looks link a square from one side,
# circle from another side, and triangle from the third 
# direction.
c = CUBE(2.0)
c = T(c, -1, -1, -1)
cyl = CYLINDER(1, 2)
cyl = T(cyl, 0, 0, -1)
p = CONVEXHULL([1, -1, -1], [1, 0, 1], [1, 1, -1], \
                [-1, -1, -1], [-1, 0, 1], [-1, 1, -1])
out = I(c, cyl, p)
VIEW(out)
