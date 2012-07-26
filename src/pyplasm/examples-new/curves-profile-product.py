from pyplasm import *

# Vertical shape:
c1 = BEZIER_1([0, 0, 0], [2, 0, 5])

# Base shape in the xy-plane:
c2 = BEZIER_2([-1, 0, 0], [0, 3, 0], [1, 0, 0])

# Reference domain:
ref_domain = UNIT_SQUARE(64, 64)

# Profile product surface: 
surf = PPSURFACE(c1, c2)
out = MAP(ref_domain, surf)

VIEW(out)

######## Example 2 ##########

# Vertical shape:
c1 = BEZIER_1([0, 0, 0], [2, 0, 0], [0, 0, 4], [1, 0, 5])

# Base shape in the xy-plane:
c2 = BEZIER_2([0, 0, 0], [3, 0, 0], [3, 3.5, 0], [0, 3, 0])

# Reference domain:
ref_domain = UNIT_SQUARE(64, 64)

# Profile product surface: 
surf = PPSURFACE(c1, c2)
out = MAP(ref_domain, surf)

VIEW(out)

