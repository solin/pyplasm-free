from pyplasm import *

c = CUBE(2)
s = CYLINDER(1.5, 3, 128)

VIEW(STRUCT([c, s]))

o = DIFF([c, s])
VIEW(o)

o2 = DIFF([s, c])
VIEW(o2)
