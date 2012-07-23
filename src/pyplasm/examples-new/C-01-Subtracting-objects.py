# Import PLaSM:
from pyplasm import *

# Display objects together:
c = CUBE(2.0)
s = CYLINDER(1.0, 3.0)
out = STRUCT(c, s) 
VIEW(out)

# Subtract them:
out = DIFF(c, s) 
VIEW(out)

# One more example:
c = CUBE(2.0)
s = CYLINDER(1.0, 3.0)
s2 = R(s, 1, -PI/2)
s3 = R(s, 2, -PI/2)
out = STRUCT(c, s, s2, s3) 
VIEW(out)

# Subtract the cylinders
# from the cube:
out = DIFF(c, s, s2, s3) 
VIEW(out)

