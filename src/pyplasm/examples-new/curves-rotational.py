from pyplasm import *

# Sample Bezier profile in the xz-plane: 
parabola = BEZIER_1([0, 0, 0], [2, 0, 0], [3, 0, 4])
  
# Reference domain with 2*PI for angle:
ref_domain = REF_DOMAIN(1, 2*PI, 32, 64)

# Rotate about the z-axis:
surf = ROTATIONAL_SURFACE(parabola)
out = MAP(ref_domain, surf)

VIEW(out)

########## Solidification ###########

out = JOIN(out)

VIEW(out)
