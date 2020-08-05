# plotSeparationDistribution.py
# Author: Tynan Kennedy
# Date: August 1, 2020

# Plots a given separation vs t onto the figure and axis passed to the function

# Command line syntax: python3 plotSeparationDistribution.py {red/blue/green} [filenames] ...
# Where the filenames are of the form [DJDJ/VDJ]_*.npy, and {red/blue/green/all} is an optional argument
# that determines the color choice of the plot.

# red/blue/green gives shades of red/blue/green
# all is specifically for plotting all of the trajectories together, and will
# only be properly color-coded if you follow the syntax:
# python3 plotSeparationDistribution.py all {num WT} {num JQ1} {num A485} {wild-type filenames} {JQ1 filenames} {A485 filenames}

# Sorry it's so complicated.

# THE AXIS LIMITS HAVE TEMPORARILY BEEN HARD-CODED!!!!

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, statistics, math, pickle, os
import filenameManipulations as fiMa
import separationDistribution as sepDis
import plotManipulations as plMa

figure_size = (10,7)
defaultBinCount = 500

def plotSeparationDistribution(pdf, binCenters, fig, ax, colors, pdfName, intLabel):
    dataType = fiMa.extractPrefix(pdfName)
    ax.plot(binCenters, pdf, label=pdfName, color=colors[intLabel], marker='None', linestyle='-')
    ax.set_xlabel(u"Separation [\u03BCm]")
    ax.set_ylabel("PDF")
    ax.set_title("Probability Density Function of " + dataType + " Separations")
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
        assert (argc - 1 <= len(colors)), "Not enough default colors. Please update plotSeparationDistribution.py"        
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

    currentDir = os.getcwd()
    for index in range(len(filenames)):
        file1 = filenames[index]
        pdfFile = currentDir + "/PDF_" + file1
        binFile = currentDir + "/binCenters_" + file1
        if os.path.isfile(pdfFile) and os.path.isfile(binFile):
            pdf = np.load(pdfFile)
            binCenters = np.load(binFile)
        else:
            pdf, binCenters = sepDis.singleTrajectoryAnalysis(file1, defaultBinCount)
        pdfName = fiMa.stripExtension(filenames[index])
        fig, ax = plotSeparationDistribution(pdf, binCenters, fig, ax, colors, pdfName, index)
    
    # Temporary, just for presentation
    ax.set_xlim(0.0, 2.25)
    ax.set_ylim(0, 9)

    ax.legend(loc = 'upper right')
    fig.tight_layout()
    
    fig.savefig("PDF_trajectory.png")
    plt.close(fig)