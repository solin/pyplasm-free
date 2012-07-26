from pyplasm import *

# Linear Bezier curve:
c1 = BEZIER_1([0, 0, 0], [0, 4, 0])

# Cubic Bezier curve:
c2 = BEZIER_1([2, 0, 0], [4, 1, 0], [0, 2, 0], [1, 3, 0])

# Reference domain with 30 times 30 subdivision:
ref_domain = UNIT_SQUARE(30, 30)

# The surface:
surf = BEZIER_2(c1, c2)
out = MAP(ref_domain, surf)

VIEW(out)

#######################

# Quadratic Bezier curve:
c1 = BEZIER_1([0, 0, 0], [-1, 1.5, 0], [0, 4, 0])

# Cubic Bezier curve:
c2 = BEZIER_1([2, 0, 0], [4, 1, 0], [0, 2, 0], [1, 3, 0])

# Reference domain with 30 times 30 subdivision:
ref_domain = UNIT_SQUARE(30, 30)

# The 2D surface:
surf = BEZIER_2(c1, c2)
out = MAP(ref_domain, surf)

VIEW(out)

#######################

# Bezier curves:
c1 = BEZIER_1([0,0,0], [5, -2, -5], [10,0,0])
c2 = BEZIER_1([0,2,0], [8,3,0], [9,2,0])
c3 = BEZIER_1([0,4,1], [7,5,-1], [8,5,1], [12,4,0])
c4 = BEZIER_1([0,6,0], [9,6,3], [10,6,-1])

# Reference domain with 30 times 30 subdivision:
ref_domain = UNIT_SQUARE(30, 30)

# The surface:
surf = BEZIER_SURFACE(c1, c2, c3, c4)
out = MAP(ref_domain, surf)

VIEW(out)

####################### Coons patch

u1 = BEZIER_1([0, 4, 0], [2.5, 3, 6], [5, 0, -6], [7.5, 0, 6], [10, 0, 0])
u2 = BEZIER_1([0, 6, 0], [2.5, 7, 6], [5, 10, -6], [7.5, 10, 6], [10, 10, 0])
v1 = BEZIER_2([0, 0, 0], [-3, 3, 3], [-3, 7, 3], [0, 10, 0])
v2 = BEZIER_2([10, 0, 0], [15, 6, 0], [10, 10, 0])

# Reference domain:
ref_domain = UNIT_SQUARE(50, 50)

# The cons patch:
surf = COONSPATCH(u1, u2, v1, v2)
out = MAP(ref_domain, surf)

VIEW(out)

#######################



