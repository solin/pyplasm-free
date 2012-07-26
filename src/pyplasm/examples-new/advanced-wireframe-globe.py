from pyplasm import *
from numpy import sin, cos

# Radiuses, thicknesses:
r1 = 0.95
r2 = 1.0
r_mid = 0.5 * (r1 + r2)
h = 0.5 * (r2 - r1)

# Create toruses:
t1 = TORUS(r1, r2)
t20 = TORUS(r_mid*cos(PI/6) - h, r_mid*cos(PI/6) + h)
t2 = T(t20, 0, 0, r_mid * sin(PI/6))
t3 = T(t20, 0, 0, -r_mid * sin(PI/6))
t40 = TORUS(r_mid*cos(PI/3) - h, r_mid*cos(PI/3) + h)
t4 = T(t40, 0, 0, r_mid * sin(PI/3))
t5 = T(t40, 0, 0, -r_mid * sin(PI/3))
t6 = R(t1, 1, PI/2)
t7 = R(t6, 3, PI/6)
t8 = R(t7, 3, PI/6)
t9 = R(t8, 3, PI/6)
t10 = R(t9, 3, PI/6)
t11 = R(t10, 3, PI/6)

# Put them together:
out = STRUCT(t1, t2, t3, t6, t7, t8, t9, t10, t11)

VIEW(out) 
