from pyplasm import *

# Column radius and height:
r = 1.0
h = 12.0

# Create one column:
basis = BRICK(2*r*1.2, 2*r*1.2, h/12.0) 
trunk = CYLINDER(r, (10.0/12.0)*h)
capital = basis
beam = S(capital, 3, 1, 1) 
column = TOP(TOP(TOP(basis, trunk), capital), beam)

# Number of columns in one row:
n = 4

# Create gable:
triangle = TRIANGLE([0, 0], [n*3*2*r*1.2, 0], [n*3*r*1.2, h/2])
prism = PRISM(triangle, r*1.2)
gable = R(prism, 1, PI/2)

# Column row:
colrow = column
for i in range(n-1):
   colrow = RIGHT(colrow, column)

# Portal:
portal = TOP(colrow, gable)

# Number of inner column rows:
m = 4

# Temple base as a list:
temple_base = [portal]
for i in range(1, m+1):
    temple_base.append(T(colrow, 0, 6*i, 0))
temple_base.append(T(portal, 0, 6*(m+1), 0))

# Convert it to an object:
temple_base = STRUCT(*temple_base)

# Create a 2D plate for the temple to stand on:
ground = FOOTPRINT(STRUCT(temple_base))

# Secondary roof beams:
x_intervals = GRID(14 * [0.6, -1.2])
y_intervals = GRID([-0.7] + 5 * [-1, 5])
z_interval = GRID([-13, 0.6])
secondary_beams = POWER(POWER(x_intervals, y_intervals), z_interval)

# Put all parts together:
out = STRUCT(temple_base, secondary_beams, ground)

# Display results:
VIEW(out)
