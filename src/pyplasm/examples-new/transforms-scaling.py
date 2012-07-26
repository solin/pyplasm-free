# Import PyPLaSM:
from pyplasm import *

# Let us define a sample object first:
R = 1.0
H = 0.3
cyl = CYLINDER (R, H)
VIEW(cyl)

# Scale it in the first axial direction only:
cyl1 = SCALE(cyl, 2, 1, 1)
VIEW(cyl1)

# Scale it in the second axial direction only:
cyl2 = SCALE(cyl, 1, 2, 1)
VIEW(cyl2)

# Scale it in the third axial direction only:
cyl3 = SCALE(cyl, 1, 1, 2)
VIEW(cyl3)

# Scale it in the first and third axial directions:
cyl4 = SCALE(cyl, 2, 1, 4)
VIEW(cyl4)

# Scale in all three directions at once.
cyl5 = SCALE(cyl, 2.0, 0.5, 4.0)
VIEW(cyl5)

