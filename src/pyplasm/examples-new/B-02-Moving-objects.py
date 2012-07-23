# Import PyPLaSM:
from pyplasm import *

c = CUBE(1.0)
c2 = T(c, 1.5, 0.0, 0.0)
VIEW(c2)

s = SPHERE(1.0)
s2 = T(s, 1.0, 2.0, 0.0)
VIEW(s2)

s = SPHERE(1.0)
s3 = T(s, -1.0, 1.0, 4.0)
VIEW(s3)









