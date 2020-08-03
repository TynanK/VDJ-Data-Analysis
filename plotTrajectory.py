# plotTrajectory.py
# Author: Tynan Kennedy
# Date: August 1, 2020

# Plots a given separation vs t onto the figure and axis passed to the function
# Command line syntax: python3 plotMSD.py {red/blue/green} [filenames] ...
# Where the filenames are of the form [DJDJ/VDJ]_*.npy, and {red/blue/green/all} is an optional argument
# that determines the color choice of the plot.

# red/blue/green gives shades of red/blue/green
# all is specifically for plotting all of the trajectories together, and will
# only be properly color-coded if you follow the syntax:
# python3 plotTrajectory.py all {num WT} {num JQ1} {num A485} {wild-type filenames} {JQ1 filenames} {A485 filenames}

# Sorry it's so complicated.

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, statistics, math, pickle
import filenameManipulations as fiMa
import plotManipulations as plMa

figure_size = (10,7)

def plotTrajectory(seps, fig, ax, colors, sepsName, intLabel):
    dataType = fiMa.extractPrefix(sepsName)
    ax.plot(seps[:,1], seps[:,0], label=sepsName, color=colors[intLabel], marker='None', linestyle='-')
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(u"Separation [\u03BCm]")
    ax.set_title(dataType + " Separation vs Time")
    fig.tight_layout()

    return fig, ax

if __name__ == "__main__":
    argc = len(sys.argv)
    colorFlag = -1
    if str(sys.argv[1]) == 'red':
        colorFlag = 0
    elif str(sys.argv[1]) == 'blue':
        colorFlag = 2
    elif str(sys.argv[1]) == 'green':
        colorFlag = 1
    elif str(sys.argv[1]) == 'all':
        colorFlag = 3
        numWT = int(sys.argv[2])
        numJQ1 = int(sys.argv[3])
        numA485 = int(sys.argv[4])

    filenames = []
    if colorFlag == -1:
        colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
        assert (argc - 1 <= len(colors)), "Not enough default colors. Please update plotMSD.py"        
        for a in range(1,argc):
            filenames.append(str(sys.argv[a]))
    elif colorFlag == 3:
        colors = plMa.genRGB(0, numWT) + plMa.genRGB(2, numJQ1) + plMa.genRGB(1, numA485)
        for a in range(5,argc):
            filenames.append(str(sys.argv[a]))
    else:
        colors = plMa.genRGB(colorFlag, argc - 2)
        for a in range(2,argc):
            filenames.append(str(sys.argv[a]))
    
    fig, ax = plt.subplots(figsize=figure_size)

    for index in range(len(filenames)):
        seps = np.load(filenames[index])
        sepsName = fiMa.stripExtension(filenames[index])
        fig, ax = plotTrajectory(seps, fig, ax, colors, sepsName, index)
    
    ax.legend(loc='upper right')
    fig.tight_layout()
    
    fig.savefig("Trajectory.png")
    plt.close(fig)