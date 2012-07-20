from pyplasm import *
color = [0.4, 0.9, 0.6]
c = BRICK(2, 2, 2)
c2 = T(1.0, 1.0, 2.0)(c)
c3 = T(1.0, 1.0, 2.0)(c2)
VIEW(STRUCT([c, c2, c3]), color)

c = BRICK(2, 2, 2)
s = SPHERE(1.0)
VIEW(TOP([c, s]), color)
