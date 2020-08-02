# separationDistribution.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# This script will take as inputs a separations trajectory and a number of bins, and generate the PDF of separations

# It two possible input syntaxes, based on an optional first input. If the first parameter is "batch", it's type 1. Otherwise it's type 2.

# Type 1: python3 separationDistribution.py batch [dataType] [numCells] [binCount]
# This will perform the analysis of trajectory files of the form [dataType]_[1-numCells].npy. ex: VDJ_1.npy, VDJ_2.npy, ...., VDJ_[numCells].npy
# binCount is just the number of points to use in the X grid of the gaussian kernel. Increasing it won't screw things up like it would for a histogram.

# Type 2: python3 separationDistribution.py [binCount] [filename(s)]
# This will perform the analysis on the specific files listed. binCount means the same as before

# The goal is to quantify the degree of overlap between trajectories.

import numpy as np
import sys, os, statistics
import filenameManipulations as fiMa
import scipy.stats

def singleTrajectoryAnalysis(filename, binCount):
    data = np.load(filename)

    PDF, binCenters = separationDistribution(data, binCount)

    np.save("PDF_" + filename, PDF)
    np.save("binCenters_" + filename, binCenters)
    return PDF, binCenters



def separationDistribution(data, binCount):

    separations = data[:,0]
    minSep = 0.99 * min(separations)
    maxSep = 1.01 * max(separations)
    binEdges = np.linspace(minSep, maxSep, num=binCount+1)
    binCenters = (binEdges[1:] + binEdges[0:binCount]) / 2.0

    kernel = scipy.stats.gaussian_kde(separations,bw_method=0.2)

    PDF = kernel.evaluate(binCenters)

    return PDF, binCenters

# Below are some deprecated functions from my initial histogram implementation. Then I remembered kernels exist.

def addToBins(bins, binEdges, datum):
    binCount = bins.size
    for a in range(binCount):
        if datum >= binEdges[a] and datum < binEdges[a+1]:
            bins[a] += 1
            break
    return bins

def normalize(bins, binEdges):
    binCount = bins.size
    binWidths = binEdges[1:] - binEdges[0:binCount]
    integral = 0
    for a in range(binCount):
        integral += bins[a] * binWidths[a]
    return bins / integral

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc >= 3), "Improper inputs. Please see separationDistribution.py for your input options."
    if str(sys.argv[1]) == "batch":
        dataType = str(sys.argv[2])
        numCells = int(sys.argv[3])
        binCount = int(sys.argv[4])
        filenames = []
        for a in range(1,numCells+1):
            filenames.append(dataType + "_" + str(a) + ".npy")
    else:
        binCount = int(sys.argv[1])
        filenames = []
        for a in range(2,argc):
            filenames.append(sys.argv[a])

    for a in range(len(filenames)):
        x = singleTrajectoryAnalysis(filenames[a], binCount)