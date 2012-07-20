from pyplasm import *

color = [0.9, 0.9, 0.9]
cube = CUBE(1)
cube2 = R(3, PI)(cube)
VIEW(STRUCT([cube, cube2]), color)

cube = CUBE(1)
cube2 = R(3, PI/4)(cube)
cube2 = R(1, PI/4)(cube2)
cube2 = T(1, 1, 1)(cube2)
VIEW(STRUCT([cube, cube2]), color)
