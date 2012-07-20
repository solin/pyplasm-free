# Let us define a sample object first:
from pyplasm import *
R = 1.0
H = 0.3
cyl = CYLINDER (R, H)
VIEW(cyl)

# Scale it in the first axial direction only:
cyl1 = SCALE(2, 1, 1)(cyl)
VIEW(cyl1)
# Scale it in the second axial direction only:
cyl2 = SCALE(1, 2, 1)(cyl)
VIEW(cyl2)

# Scale it in the third axial direction only:
cyl3 = SCALE(1, 1, 2)(cyl)
VIEW(cyl3)

# Scale it in the first and third axial directions:
cyl4 = SCALE(2, 1, 4)(cyl)
VIEW(cyl4)

# Scale in all three directions at once.
cyl5 = SCALE(2.0, 0.5, 4.0)(cyl)
VIEW(cyl5)

