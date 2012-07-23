# Import PyPLaSM:
from pyplasm import *

# Union of three cylinders and a cube:
c = CUBE(2.0)
s = CYLINDER(1.0, 3.0)
s2 = R(s, 1, -PI/2)
s3 = R(s, 2, -PI/2)
out = U(c, s, s2, s3) 
VIEW(out)
