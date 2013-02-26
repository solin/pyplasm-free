from pyplasm import *

# Create a cube of size 2:
c = CUBE(2)

# Move it so that center lies at origin:
c = T(c, -1, -1, -1)

# Create a brick via scaling:
b = S(c, 0.75, 0.75, 2)

# Create a list of 64 rotated bricks.
L = []
alpha = 360.0 / 64
for i in range(64):
  L.append(R(b, 3, i*alpha))

# Create a cylinder by intersecting
# all bricks in list L:
b = I(*L)
  
# Create two additional cylinders via rotation:
b2 = RDEG(b, 2, 90)
b3 = RDEG(b, 1, 90)

# Subtract the three cylinders from the cube:
o = DIFF(c, b, b2, b3)

# View the result:
VIEW(o)
