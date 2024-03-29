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
import arrayManipulations as arMa


figure_size = (10,7)

def plotTrajectory(seps, fig, ax, colors, sepsName, intLabel):
    dataType = fiMa.extractPrefix(sepsName)
    ax.plot(seps[:,1], seps[:,0], label=sepsName, color=colors[intLabel], marker='None', linestyle='-')
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(u"Separation [\u03BCm]")
    #ax.set_title(dataType + " Separation vs Time")
    # THIS IS A TEMPORARY CHANGE TO MAKE A PARTICULAR PLOT
    # COMMENT IT BACK OUT AFTER YOU'RE DONE
    ax.set_title("Separation vs Time")
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
    fig1, ax1 = plt.subplots(figsize=figure_size)

    for index in range(len(filenames)):
        seps = np.load(filenames[index])
        smoothSeps = arMa.smooth(seps,5)
        sepsName = fiMa.stripExtension(filenames[index])
        fig, ax = plotTrajectory(seps, fig, ax, colors, sepsName, index)
        fig1, ax1 = plotTrajectory(smoothSeps, fig1, ax1, colors, sepsName, index)
        
    
    lineX = np.linspace(0.0, 400.0)
    lineY = np.zeros(lineX.shape)
    for a in range(lineX.size):
        lineY[a] = 0.126
    ax.plot(lineX, lineY, linestyle='--', color='k',label="Encounter Threshold", marker='None')
    ax1.plot(lineX, lineY, linestyle='--', color='k',label="Encounter Threshold", marker='None')

    #TEMPORARILY HARD-CODED YLIMS. Feel free to revert or adjust if you need to.
    ax.set_ylim(0.0, 2.0)
    ax1.set_ylim(0.0, 2.0)

    #TEMPORARILY REMOVED THE LEGEND. UNCOMMENT THIS ONCE THE PARTICULAR PLOT IS DONE.
    #ax.legend(loc='upper right')

    fig.tight_layout()
    fig1.tight_layout()

    fig.savefig("Trajectory.png")
    fig1.savefig("Trajectory_smooth.png")
    
    plt.close(fig)
    plt.close(fig1)