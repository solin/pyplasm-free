from pyplasm import *

def p(point):
    x = point[0]
    return [x, 0, 0]

def q(point):
    x = point[0]
    return [0, 1, x]

# Unit square covered with a 32x32 Cartesian grid:  
ref_domain = UNIT_SQUARE(32, 32)

# Creating the ruled surface:
surf = RULED_SURFACE(p, q)
out = MAP(ref_domain, surf)

VIEW(out)

######### Spiral #########

# Import sine and cosine from Numpy:
from numpy import sin, cos

def p(point):
    x = point[0]
    return [0, 0, 0.5*x]
  
def q(point):
    x = point[0]
    return [cos(x), sin(x), 0]

# Reference domain:  
ref_domain = REF_DOMAIN(8*PI, 5, 128, 16)

# Creating the ruled surface:
surf = RULED_SURFACE(p, q)
out = MAP(ref_domain, surf)

VIEW(out)

######## Straight cylinder ##########

# Import sine and cosine from Numpy:
from numpy import sin, cos

# Cylinder radius:
r = 3.0

# Cylinder height:
h = 10.0

def p(point):
    x = point[0]
    return [r*cos(x), r*sin(x), 0]
  
def q(point):
    x = point[0]
    return [0, 0, 1]

# Reference domain:  
ref_domain = REF_DOMAIN(2*PI, h, 64, 1)

# Creating the ruled surface:
surf = RULED_SURFACE(p, q)
out = MAP(ref_domain, surf)

VIEW(out)

######## CURVED cylinder #########

# Import since and cosine from Numpy:
from numpy import sin, cos

# Cylinder radius:
r = 3.0

# Cylinder height:
h = 10.0

# Angular shift:
alpha = 0.7 * PI

def p(point):
    x = point[0]
    return [r*cos(x), r*sin(x), 0]
  
def q(point):
    x = point[0]
    return [r/h * (cos(x + alpha) - cos(x)), r/h * (sin(x + alpha) - sin(x)), 1]

# Reference domain::  
ref_domain = REF_DOMAIN(2*PI, h, 64, 32)

# Creating the ruled surface:
surf = RULED_SURFACE(p, q)
out = MAP(ref_domain, surf)

VIEW(out)

####### Spanning arbitrary 3D curves  - example 1 ########

# Import sine from Numpy:
from numpy import sin

# Define two 3D curves:
def c1(x):
    return [x, 0, sin(x)]

def c2(x):
    return [x, 2*PI, (x/PI - 1)**2]
  
def p(point):
    x = point[0]
    return c1(x)
  
# Return a vector pointing from one curve to the other:
def q(point):
    x = point[0]
    return [c2(x)[0] - c1(x)[0], c2(x)[1] - c1(x)[1], c2(x)[2] - c1(x)[2]]
  
# Reference domain:
ref_domain = REF_DOMAIN(2*PI, 1, 64, 1)

# Creating the ruled surface:
surf = RULED_SURFACE(p, q)
out = MAP(ref_domain, surf)

VIEW(out)

####### Spanning arbitrary 3D curves  - example 1 ########

# Import sine and cosine from Numpy:
from numpy import sin, cos

# Define two 3D curves:
def c1(t):
    return [cos(t), sin(t), PI - t]

def c2(t):
    return [cos(PI + t), sin(PI + t), PI - t]
  
def p(point):
    x = point[0]
    return c1(x)
  
# Return a vector pointing from one curve to the other:
def q(point):
    x = point[0]
    return [c2(x)[0] - c1(x)[0], c2(x)[1] - c1(x)[1], c2(x)[2] - c1(x)[2]]
  
# Reference domain:
ref_domain = REF_DOMAIN(PI, 1, 64, 30)

# Creating the ruled surface:
surf = RULED_SURFACE(p, q)
out = MAP(ref_domain, surf)

VIEW(out)



