#! /usr/bin/python

__author__="Marek Krzysztof Wierzba [marek.wierzba at gmail.com]"
__date__ ="$18-dic-2011 10.49.06$"

if __name__ == "__main__":
    from pyplasm import *
    from fonts import *

    # How fine should the approximation of arcs be:
    LINEARAPPROXIMATION = 12

    # Choose text:
    text = "CAD"

    # Choose font:
    #font = PARSESVGFONT("acaslonprobolditalic.svg")
    font = PARSESVGFONT("blackoakstd.svg")
    #font = PARSESVGFONT("frscript.svg")
    #font = PARSESVGFONT("jokerman.svg")
    #font = PARSESVGFONT("stencilstd.svg")
    #font = PARSESVGFONT("acaslonprobold.svg")
    #font = PARSESVGFONT("cooperblackstd.svg")
    #font = PARSESVGFONT("giddyupstd.svg")
    #font = PARSESVGFONT("matisse_.svg")
    #font = PARSESVGFONT("vivaldii.svg")
    #font = PARSESVGFONT("acaslonprosemibolditalic.svg")
    #font = PARSESVGFONT("curlz.svg")
    #font = PARSESVGFONT("itcblkad.svg")
    #font = PARSESVGFONT("mtcorsva.svg")
    MyText = TEXTWITHATTRIBUTES(TEXTALIGNMENT, TEXTANGLE, TEXTWIDTH, TEXTHEIGHT, LINEARAPPROXIMATION)

    #There are too many parenthesis here, and you should use MyText Instead of TEXT:
    #VIEW(TEXT((text)(font)))
    #This is the correct call:
    VIEW(MyText(text)(font))

    #And this is the correct way to call TEXT function:
    #VIEW(TEXT((text,LINEARAPPROXIMATION)(font)))
   
    raw_input("")
