# plotManipulations.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# Just some helper functions for plotting

import numpy as np

def genRGB(colorFlag, count):
    RGB = []
    magRange = np.linspace(0.0, 0.8, num=count)
    for a in range(count):
        color_list = [magRange[a], magRange[a], magRange[a]]
        color_list[colorFlag] = 1.0
        color = tuple(color_list)
        RGB.append(color)
    return RGB