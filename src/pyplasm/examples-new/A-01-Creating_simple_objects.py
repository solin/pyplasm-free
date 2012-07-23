# Import PyPLaSM:
from pyplasm import *

# Cube:
c = CUBE(1)
VIEW(c)

# Brick:
c = BRICK(3, 2, 1)
VIEW(c)

# Square:
s = SQUARE(1)
VIEW(s)

# Rectangle:
r = RECTANGLE(2, 1)
VIEW(r) 

# Sphere:
s = SPHERE(3.0)
VIEW(s)

# Circle:
c = CIRCLE(5.0)
VIEW(c)

# Tetrahedron:
t = TETRAHEDRON([-1, 0, 0], [4, 0, 0], [0, 4, 1], [0, 1, 2])
VIEW(t)

# Triangle
t = TRIANGLE([1, 1], [4, 2], [2, 4])
VIEW(t)

# Prism:
# The basis can be a general 2D polygon:
B = TRIANGLE([-1, 0], [1, 0], [0, -2])
H = 2.0
p = PRISM(B, H)
VIEW(p)

# Cone:
R = 5
H = 10
cone = CONE(R, H)
VIEW(cone)

# Truncated cone:
R1 = 5
R2 = 4
H = 5
tcone = TRUNCONE(R1, R2, H)
VIEW(tcone)

# Cylinder:
cyl = CYLINDER (0.25, 1.0)
VIEW(cyl)

# Tube:
r = 0.9
R = 1.0
L = 3.0
tube = TUBE(r, R, L)
VIEW(tube)

# Torus:
r = 3.0
R = 5.0
tor = TORUS(r, R)
VIEW(tor)

# Convex hull: We will create a polygon with 
# N edges inscribed into circle of radius R.
N = 15
R = 5
L = CIRCLE_POINTS(R, N)
# The CONVEXHULL command expects bare points. 
# If you provide a list, insert asterisk in
# front of its name. 
p = CONVEXHULL(*L)
VIEW(p)











