from pyplasm import *
c = CUBE(2)
c = T(-1, -1, 0)(c)
c2 = R(3, PI/4.)(c)

VIEW(STRUCT([c, c2])) 


VIEW(XOR([c, c2])) 
