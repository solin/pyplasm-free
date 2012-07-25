from pyplasm import *

grid1 = GRID([1])
grid2 = GRID([2])

out = POWER(grid1, grid2)
VIEW(out)
