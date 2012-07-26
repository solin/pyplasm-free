from pyplasm import *

# Cubic Bezier curve in the xy-plane:
c = BEZIER_1([1,1,0], [-1,1,0], [1,-1,0], [-1,-1,0])

# Reference domain:
ref_domain = UNIT_SQUARE(64, 1)

# Height:
H = 2.0

# Directional vector:
vec = [0, 0, H]

# Product geometry:
surf = CYLINDRICAL_SURFACE(c, vec)
out = MAP(ref_domain, surf)

VIEW(out)
