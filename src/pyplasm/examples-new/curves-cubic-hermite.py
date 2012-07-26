from pyplasm import *

# First curve:
c1 = CUBIC_HERMITE_1([0, 0, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0])

# Second curve:
c2 = CUBIC_HERMITE_1([1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0])

# Slope vector for the first curve:
s1 = [1, 0, 1]

# Slope vector for the second curve:
s2 = [1, 0, 1]

# Reference domain:
ref_domain = UNIT_SQUARE(32, 32)

# Cubic Hermite surface:
surf = CUBIC_HERMITE_2(c1, c2, s1, s2)
out = MAP(ref_domain, surf)

VIEW(out)

########## Example 2 #########

# First curve:
c1 = CUBIC_HERMITE_1([0, 0, 0], [0, 1, 0], [1, 1, 0], [-1, 1, 0])

# Second curve:
c2 = CUBIC_HERMITE_1([1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0])

# Slope vector for the first curve:
s1 = [1, 0, 1]

# Slope vector for the second curve:
s2 = [1, 0, 1]

# Reference domain:
ref_domain = UNIT_SQUARE(32, 32)

# Cubic Hermite surface:
surf = CUBIC_HERMITE_2(c1, c2, s1, s2)
out = MAP(ref_domain, surf)

VIEW(out)

######### Example 3 #########

# First curve:
c1 = CUBIC_HERMITE_1([0, 0, 0], [0, 1, 0], [1, 1, 0], [-1, 1, 0])

# Second curve:
c2 = CUBIC_HERMITE_1([1, 0, 0], [1, 1, 0], [0, 1, 1], [0, 1, 1])

# Slope vector for the first curve:
s1 = [1, 0, 1]

# Slope vector for the second curve:
s2 = [1, 0, 1]

# Reference domain:
ref_domain = UNIT_SQUARE(32, 32)

# Cubic Hermite surface:
surf = CUBIC_HERMITE_2(c1, c2, s1, s2)
out = MAP(ref_domain, surf)

VIEW(out)

######### Example 4 #########

# First (outer) curve:
c1 = CUBIC_HERMITE_1([1, 0, 0], [0, 1, 0], [0, 3, 0], [-3, 0, 0])

# Second (inner) curve:
c2 = CUBIC_HERMITE_1([0.5, 0, 0], [0, 0.5, 0], [0, 1, 0], [-1, 0, 0])

# Slope vector for the outer curve:
s1 = [0, 0, 1]

# Slope vector for the inner curve:
s2 = [-1, -1, -1]

# Reference domain:
ref_domain = UNIT_SQUARE(32, 32)

# The 3D object:
surf = CUBIC_HERMITE_2(c1, c2, s1, s2)
out = MAP(ref_domain, surf)

VIEW(out)


