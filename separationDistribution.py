# separationDistribution.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# This script will take as inputs a separations trajectory and a number of bins, and generate the PDF of separations

# The goal is to quantify the degree of overlap between trajectories.

import numpy as np
import sys, os, statistics
import filenameManipulations as fiMa

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
    bins = np.zeros(binCount)

    len0 = separations.size
    for a in range(len0):
        bins = addToBins(bins, binEdges, separations[a])

    PDF = normalize(bins, binEdges)

    return PDF, binCenters

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
    assert (len(sys.argv) == 3), "Improper inputs. Proper syntax: python3 separationDistribution.py [separations file] [binCount]"
    filename = str(sys.argv[1])
    binCount = int(sys.argv[2])

    x = singleTrajectoryAnalysis(filename, binCount)