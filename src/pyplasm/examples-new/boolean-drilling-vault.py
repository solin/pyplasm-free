# Import PLaSM:
from pyplasm import *

# Define main vault body:
body = BRICK(1, 1, 1.2)
interior = BRICK(0.86, 0.95, 1.06)
interior = T(interior, 0.07, 0, 0.07)
body = DIFF(body, interior)

# Top part:
top = CONVEXHULL([0, 0, 1.2], [1, 0, 1.2], [1, 1, 1.2], [0, 1, 1.2], [0.01, 0.01, 1.21], \
                 [0.99, 0.01, 1.21], [0.99, 0.99, 1.21], [0.01, 0.99, 1.12])

# Shelves:
shelf = BRICK(1, 0.85, 0.02)
shelf1 = T(shelf, 0, 0.1, 0.4)
shelf2 = T(shelf1, 0, 0, 0.4)

# Front door:
door = BRICK(0.84, 0.05, 1.04)
door = T(door, 0.08, 0, 0.08)
door_frame = BRICK(0.86, 0.03, 1.06)
door_frame = T(door_frame, 0.07, 0.02, 0.07)

# Truncated cone under the handles:
tcone = TRUNCONE(0.14, 0.13, 0.02)
tcone = R(tcone, 1, PI/2)
tcone = T(tcone, 0.5, 0, 0.6)

# Cylinder that holds the handles:
cyl = CYLINDER(0.07, 0.1)
cyl = R(cyl, 1, PI/2)
cyl = T(cyl, 0.5, 0, 0.6)

# Small truncated cone at the handles:
stcone = TRUNCONE(0.07, 0.06, 0.01)
stcone = R(stcone, 1, PI/2)
stcone = T(stcone, 0.5, -0.1, 0.6)

# Handles:
h1 = CYLINDER(0.022, 0.3)
ts = TRUNCONE(0.022, 0.017, 0.01)
ts = T(ts, 0, 0, 0.3)
h1 = U(h1, ts)
h1 = R(h1, 1, PI/24)
h1 = R(h1, 2, -7*PI/24)
h2 = R(h1, 2, -2*PI/3)
h3 = R(h2, 2, -2*PI/3)
h1 = T(h1, 0.5, -0.06, 0.6)
h2 = T(h2, 0.5, -0.06, 0.6)
h3 = T(h3, 0.5, -0.06, 0.6)

# Bolts:
b1 = CONVEXHULL([0.81, 0, 0.19], [0.83, 0, 0.17], [0.97, 0, 0.17], [0.97, 0, 0.26], \
                [0.83, 0, 0.26], [0.81, 0, 0.24], [0.815, -0.01, 0.195], [0.835, -0.01, 0.175], \
                [0.965, -0.01, 0.175], [0.965, -0.01, 0.255], [0.835, -0.01, 0.255], [0.815, -0.01, 0.235])
b2 = T(b1, 0, 0, 0.77)

# Bolt cylinder:
bc = CYLINDER(0.015, 0.1, 16)
bc1 = T(bc, 0.925, -0.009, 0.165)
bc2 = T(bc1, 0, 0, 0.77)

# Small bolt sphere:
sbc = SPHERE(0.01, [8, 8])
sbc = R(sbc, 1, PI/2)
sbc1 = T(sbc, 0.845, -0.01, 0.195)
sbc2 = T(sbc1, 0, 0, 0.035)
sbc3 = T(sbc1, 0, 0, 0.77)
sbc4 = T(sbc3, 0, 0, 0.035)

# Vertical handle:
vh = CYLINDER(0.02, 0.5, 16)
vh = T(vh, 0.15, -0.04, 0.35)

# Vertical handle supports:
vh0 = CYLINDER(0.015, 0.06, 16)
vh0 = R(vh0, 1, PI/2)
vh0 = T(vh0, 0.15, 0.02, 0.4)
vh1 = T(vh0, 0, 0, 0.4)

# Put everything together:
rest = STRUCT(top, shelf1, shelf2, door, door_frame, tcone, cyl, stcone, h1, h2, h3, b1, \
              b2, bc1, bc2, sbc1, sbc2, sbc3, sbc4, vh, vh0, vh1)
vault = STRUCT(body, rest)
VIEW(vault)

# Define drill:
drill = CYLINDER(0.1, 0.5)
tip = CONE(0.1, 0.1)
drill = TOP(drill, tip)
drill = R(drill, 2, -PI/2)
drill = T(drill, -0.7, 0.5, 0.55)
VIEW(STRUCT(body, rest, drill))

# Put drill through the wall:
drill = T(drill, 0.3, 0, 0)
VIEW(STRUCT(body, rest, drill))

# Remove the drill:

# WRONG WAY:
#drilled_vault = DIFF(vault, drill)
#VIEW(STRUCT(drilled_vault))

# CORRECT:
drilled_body = DIFF(body, drill)
VIEW(STRUCT(drilled_body, rest))
