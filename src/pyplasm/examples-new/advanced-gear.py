from pyplasm import *

# Brass color:
color = [222/255., 218/255., 72/255.]

# Number of teeth:
N = 18

# Width of the tooth:
x0  = 8
dx1 = 1
dx2 = 2.5

# Height of the tooth:
y0  = 30
dy1 = 0.5
dy2 = 4

# Depth of the tooth:
z1 = 5
z2 = 8

# Base inner and outer radius, height:
# (Do not change these)
base_rin  = 22
base_rout = 30
base_h    = 32

# Vertices:
pts_base = [[0, 0, 0], [x0, 0, 0], [x0, y0, 0], [0, y0, 0]]
pts_mid  = [[dx1, dy1, z1], [x0 - dx1, dy1, z1], [x0 - dx1, y0 - dy1, z1], [dx1, y0 - dy1, z1]]
pts_top  = [[dx2, dy2, z2], [x0 - dx2, dy2, z2], [x0 - dx2, y0 - dy2, z2], [dx2, y0 - dy2, z2]]

# Merging the point lists:
pts = pts_base + pts_mid + pts_top

# Toothe is a convexhull of the points:
t = CONVEXHULL(*pts)

VIEW(COLOR(color)(t))

###############

# Rotate and translate the tooth:
t = R(t, 1, PI/2)
t = R(t, 3, PI/2)
t = T(t, base_rout - 0.3, -x0/2., 0)

# Calculate the angle of rotation:
angle = 2*PI/N

# Create all teeth:
gear = []
for i in range(N):
    gear.append(R(t, 3, i * angle))

VIEW(COLOR(color)(STRUCT(*gear)))

###############

# Base:
base = TUBE(base_rin, base_rout, base_h, 128)
dz = (base_h - y0)/2.
base = T(base, 0, 0, -dz)

VIEW(COLOR(color)(base))

###############

# Truncated cone:
tc1 = TRUNCONE(base_rout, base_rout - 1, 1)
tc1 = T(tc1, 0, 0, base_h)

# Regular cone:
cone = CONE(base_rout, base_rout)
cone = R(cone, 2, PI)
cone = T(cone, 0, 0, 40)

VIEW(COLOR(color)(STRUCT(tc1, cone)))

###############

# Difference of the cones:
tc = DIFF(tc1, cone)

VIEW(COLOR(color)(tc))

###############

# Put the ring on top of the base:
base = TOP(base, tc)

# Attach teeth:
gear.append(base) 

VIEW(COLOR(color)(STRUCT(*gear)))

###############

# Inner layer thickness:
inner_dr  = 3

# Create inner tube:
inner = TUBE(base_rin - inner_dr, base_rin, base_h * 0.75)
inner = T(inner, 0, 0, base_h * 0.25)

# Define three bricks:
b1 = BRICK(50, 10, 35)
b1 = T(b1, -25, -5, 0)
b2 = R(b1, 3, PI/3)
b3 = R(b2, 3, PI/3)

VIEW(COLOR(color)(STRUCT(inner, b1, b2, b3)))

###############

# Subtract all three bricks from the tube:
inner = DIFF(inner, b1)
inner = DIFF(inner, b2)
inner = DIFF(inner, b3)

VIEW(COLOR(color)(inner))

###############

# Subtract cone from inner part:
inner = DIFF(inner, cone)

# Translate the inner part:
inner = T(inner, 0, 0, -dz)

VIEW(COLOR(color)(inner))

###############

# Append inner part to gear:
gear.append(inner)

# Display the gear:
out = STRUCT(*gear)

VIEW(COLOR(color)(out))

# STL output:
import plasm_stl
filename = "gear.stl"
plasm_stl.toSTL(out, filename)
print "STL file written to", filename

