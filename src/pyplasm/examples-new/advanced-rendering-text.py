from pyplasm import *

import sys
sys.path.append("/home/pavel/repos/pyplasm/src/pyplasm/examples-new/fonts/")
from fonts import PARSESVGFONT, TEXTWITHATTRIBUTES

# Choose text:
text = "Welcome!"

# Select font:
#font = PARSESVGFONT("fonts/acaslonprobolditalic.svg")
#font = PARSESVGFONT("fonts/blackoakstd.svg")
#font = PARSESVGFONT("fonts/frscript.svg")           # looks like hand-written
#font = PARSESVGFONT("fonts/jokerman.svg")
#font = PARSESVGFONT("fonts/stencilstd.svg")
#font = PARSESVGFONT("fonts/acaslonprobold.svg")
#font = PARSESVGFONT("fonts/cooperblackstd.svg")
#font = PARSESVGFONT("fonts/giddyupstd.svg")         # looks like hand-written
#font = PARSESVGFONT("fonts/matisse_.svg")
#font = PARSESVGFONT("fonts/vivaldii.svg")           # italic - like
#font = PARSESVGFONT("fonts/acaslonprosemibolditalic.svg")
font = PARSESVGFONT("fonts/curlz.svg")
#font = PARSESVGFONT("fonts/itcblkad.svg")
#font = PARSESVGFONT("fonts/mtcorsva.svg")

# Color:
color = [0, 0.99, 0]

# Text width and height:
tw = 1.0
th = 1.0

# Text angle:
ta = 0

# Piecewise-linear approximation of arcs:
linapp = 4

# Text alignment:
text_align = 'left'

# Render the text:
MyText = TEXTWITHATTRIBUTES(text_align, ta, tw, th, linapp)

# Display the result:
VIEW(MyText(text)(font), color)
