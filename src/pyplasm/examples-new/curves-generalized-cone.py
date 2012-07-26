from pyplasm import *

# Bezier curve in the xy-plane:
c = BEZIER_1([1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0])

# Reference domain:
ref_domain = UNIT_SQUARE(64, 8)

# Tip of the cone:
tip = [0, 0, 2.0]

# Conical surface:
surf = CONICAL_SURFACE(tip, c)
out = MAP(ref_domain, surf)

VIEW(out)
