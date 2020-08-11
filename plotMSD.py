# plotMSD.py
# Author: Tynan Kennedy
# Date: July 29, 2020

# Plots a given MSD vs dt onto the figure and axis passed to the function
# Command line syntax: python3 plotMSD.py {red/blue/green} [filenames] ...
# Where the filenames are of the form stats.npy, and {red/blue/green/all} is an optional argument
# that determines the color choice of the plot.

# red/blue/green gives shades of red/blue/green
# all is specifically for plotting all of the MSD trajectories together, and will
# only be properly color-coded if you follow the syntax:
# python3 plotMSD.py all {num WT} {num A485} {num JQ1} {wild-type filenames} {A485 filenames} {JQ1 filenames} 

# Sorry it's so complicated.

# WARNING: TEMPORARILY HARD-CODED TO CUT OFF PLOTS ABOVE X=200S

import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rc('font', family='monospace')
import matplotlib.pyplot as plt
import sys, statistics, math, pickle, os
import filenameManipulations as fiMa
import plotManipulations as plMa

figure_size = (10,7)

def plotMSD(stats, fig, ax, colors, statsName, intLabel):
    
    ax.loglog(stats[:,2], stats[:,0], label=statsName, color=colors[intLabel], marker='.', linestyle='None')
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(u"MSD [\u03BCm^2]")
    ax.set_title("Mean-Squared Displacement vs Time")
    ax.set_xlim(2, 200)
    #ax.set_ylim(0.01, 1.00)
    fig.tight_layout()

    return fig, ax

def plotDiffFit(diffFit, fig, ax):
    xvals = np.linspace(diffFit[4], diffFit[5], num=100, dtype=float)
    yvals = np.zeros(xvals.size)
    for a in range(xvals.size):
        yvals[a] = diffusionEquation(diffFit[0], diffFit[2], xvals[a])
    
    ax.loglog(xvals, yvals, label='_nolegend_', marker='None', color='k', linestyle='--')

    return fig, ax


def diffusionEquation(alpha, D, t):
    return 6*D*math.pow(t,alpha)

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
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
        assert (argc - 1 <= len(colors)), "Not enough default colors. Please update plotMSD.py"        
        for a in range(1,argc):
            filenames.append(str(sys.argv[a]))
    elif colorFlag == 3:
        colors = plMa.genRGB(0, numWT) + plMa.genRGB(1, numA485) + plMa.genRGB(2, numJQ1)
        for a in range(5,argc):
            filenames.append(str(sys.argv[a]))
    else:
        colors = plMa.genRGB(colorFlag, argc - 2)
        for a in range(2,argc):
            filenames.append(str(sys.argv[a]))
    
    fig, ax = plt.subplots(figsize=figure_size)

    diffFits = []
    currentDir = os.getcwd()
    for index in range(len(filenames)):
        stats = np.load(filenames[index])
        statsName = fiMa.stripPrefix(fiMa.stripExtension(filenames[index]))

        statsNamePrefix = fiMa.extractPrefix(statsName)
        if statsNamePrefix == "VDJ" or statsNamePrefix == "DJDJ":
            statsNameSuffix = fiMa.stripPrefix(statsName)
            statsLabel = "{0:{width}s}, {1:4s}".format(statsNameSuffix, statsNamePrefix, width=4) # COME BACK AND FIX THIS WIDTH LATER
        else:
            statsLabel = statsName

        fig, ax = plotMSD(stats, fig, ax, colors, statsLabel, index)
        diffFilename = currentDir + "/diff_" + filenames[index]
        if os.path.isfile(diffFilename):
            diffFit = np.load(diffFilename)
            fig, ax = plotDiffFit(diffFit, fig, ax)
            diffFits.append([statsLabel, colors[index]] + list(diffFit[0:4]))

    numFits = len(diffFits)
    diffRowColors = []
    diffRowLabels = []
    diffColLabels = [" ", u"\u03B1", u"D [\u03BCm^2 / s]"]
    diffCellText = []
    for a in range(numFits):
        diffRowColors.append(diffFits[a][1])
        diffRowLabels.append(diffFits[a][0])
        alphaString = u"{0:3.2f} \u00B1 {1:3.2f}".format(diffFits[a][2], diffFits[a][3])
        DString = u"{0:5.4f} \u00B1 {1:5.4f}".format(diffFits[a][4], diffFits[a][5])
        diffCellText.append([diffFits[a][0], alphaString, DString])

    ax.table(cellText=diffCellText, cellLoc='center', colWidths=[0.1, 0.2, 0.2], colLabels=diffColLabels, loc='upper left', edges='BR')
    
    ax.legend(loc = 'upper right')
    fig.tight_layout()
    
    fig.savefig("MSD.png")
    # pickle.dump(ax, file('MSD.pickle', 'w')) # Can reload this using pickle.load('MSD.pickle'), then plt.show()
    plt.close(fig)