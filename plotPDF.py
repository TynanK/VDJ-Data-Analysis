# plotPDF.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# Plots partial distribution functions against separations

# Command line syntax: python3 plotPDF.py [red/blue/green/all] [filenames] ...
# Where the filenames are of the form separations.npy, and [red/blue/green/all] is an optional argument
# that determines the color choice of the plot.

# red/blue/green gives shades of red/blue/green
# all is specifically for plotting all of the PDFs together, and will
# only be properly color-coded if you follow the syntax:
# python3 plotPDF.py all {num WT} {num JQ1} {num A485} {wild-type filenames} {JQ1 filenames} {A485 filenames}

# Sorry it's so complicated.

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, statistics, math, pickle, os
import filenameManipulations as fiMa
import separationDistribution as sepDis
import plotManipulations as plMa

figure_size = (10,10)
defaultBinCount = 50

def plotPDF(pdf, binCenters, fig, ax, colors, dataName, intLabel):

    ax.plot(binCenters[:], pdf[:], label=dataName, color=colors[intLabel], marker='none', linestyle='-')
    ax.set_xlabel(u"Separation [\u03BCm]")
    ax.set_ylabel("PDF")
    ax.set_title("Probability Density Function of Separations over Time")
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
        dataName = fiMa.stripExtension(file1)
        fig, ax = plotPDF(pdf, binCenters, fig, ax, colors, dataName, index)
    
    ax.legend()
    fig.tight_layout()
    
    fig.savefig("PDF.pdf")
    # pickle.dump(ax, file('PDF.pickle', 'w')) # Can reload this using pickle.load('PDF.pickle'), then plt.show()
    plt.close(fig)