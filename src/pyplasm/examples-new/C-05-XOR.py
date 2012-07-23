# Import PyPLaSM:
from pyplasm import *

# Create two cubes, rotate one of them,
# display them together:
c = CUBE(2.0)
c = T(c, -1, -1, 0)
c2 = R(c, 3, PI/4)
out = STRUCT(c, c2) 
VIEW(out)

# Show their intersection:
out = I(c, c2) 
VIEW(out)

# Show their XOR:
out = XOR(c, c2) 
VIEW(out)
