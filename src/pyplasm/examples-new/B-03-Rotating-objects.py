# Import PyPLaSM:
from pyplasm import *

# Rotate a cube about its edge:
c = CUBE(1)
c2 = R(c, 3, PI)
VIEW(STRUCT(c, c2))

# Rotation and translation:
c = CUBE(1)
c2 = R(c, 3, PI/4)
c2 = R(c2, 1, PI/4)
c2 = T(c2, 1, 1, 1)
VIEW(STRUCT(c, c2))
