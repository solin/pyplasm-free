from pyplasm import *

c = CUBE(1)
VIEW(c)

s = SQUARE(1)
VIEW(s)

r = RECTANGLE(2, 1)
VIEW(r) 

t = SIMPLEX(3)
VIEW(t)

t = SIMPLEX(2)
VIEW(t)

points = [[-1, 0, 0], [4, 0, 0], [0, 4, 1], [0, 1, 2]]
t = CONVEXHULL(points)
VIEW(t)

points = [[1, 1], [4, 2], [2, 4]]
t = CONVEXHULL(points)
VIEW(t)

from numpy import sin, cos, pi
N = 15
R = 5
points = []
for i in range(N):
    angle = i * 2. * pi / N
    points.append([R * cos(angle), R * sin(angle)])
p = CONVEXHULL(points)
VIEW(p)

points = [[-1, 0, 0], [1, 0, 0], [0, 2, 0], [0, 1, 1]]
t = CONVEXHULL(points)
VIEW(t)

# The basis can be a general 2D polygon:
basis = CONVEXHULL([[-1, 0], [1, 0], [0, -2]])
H = 2.0
p = PRISM(basis, H)
VIEW(p)

# Cone:
N = 128
R = 5
H = 10
cone = CONE(R, H, 64)
VIEW(cone)

# Cylinder:
cyl = CYLINDER (0.25, 1.0, 128)
VIEW(cyl)

# Tube:
r = 0.9
R = 1.0
L = 3.0
tube = TUBE(r, R, L, 128)
VIEW(tube)

# Sphere:
s = SPHERE(3.0)
VIEW(s)

# Torus:
r = 3.0
R = 5.0
tor = TORUS(r, R)
VIEW(tor)










