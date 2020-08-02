# plotVAC.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# Arguments: numDelta minDelta maxDelta maxDt [filenames]
# numDelta: The script draws plots for multiple values of Delta for each filename. This parameter sets the maximum number to draw for each file. The actual number drawn can be less, if there aren't enough between minDelta and maxDelta.
# minDelta: The minimum value of Delta to use. If this is less than the lowest value of Delta in the data set, that value supercedes minDelta.
# maxDelta: The maximum value of Delta to use. If this is more than the largest value of Delta in the data set, that value supercedes maxDelta.
# maxDt:    The maximum value of Dt (the x-axis) to plot to. Data will be truncated beyond this value. No need to specify minDt, since it will always be zero.
# [filenames]: These should be files output by VAC.py or ensembleVAC.py. Specifically, stats_VAC_*.npy. The script will fetch any relevant dts_VAC_*.npy and deltas_VAC_*.npy files.

# Note: this will output TWO plots. One of VAC vs dt, and one of VAC vs dt/delta

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, statistics, math, pickle
import filenameManipulations as fiMa
import arrayManipulations as arMa
import plotManipulations as plMa

figure_size = (10,10)

def plotVAC(fig, ax, x_vals, y_vals, statsName, intLabel, colors):

    ax.plot(x_vals, y_vals, label=statsName, color=colors[intLabel], marker='.', linestyle='none')
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("VAC")
    ax.set_title("Velocity Autocorrelation vs Time")
    ax.set_ylim(-1.0, 1.0)
    fig.tight_layout()

    return fig, ax

def truncateAboveIndex(list1, maxVal): # Returns the index, not the new list!!! Horribly named, I know.
    list_sorted = list1
    list_sorted.sort()
    assert (list_sorted == list1), "Error: Attempted to truncate an unsorted list"
    maxList = max(list1)
    if maxVal >= maxList:
        return len(list1)
    else:
        for a in len(list1):
            if maxVal < list1[a]:
                return a

def truncateBelowIndex(list1, minVal): # Returns the index, not the new list!!! Horribly named, I know.
    list_sorted = list1
    list_sorted.sort()
    assert (list_sorted == list1), "Error: Attempted to truncate an unsorted list"
    minList = min(list1)
    if minVal <= minList:
        return 0
    else:
        for a in len(list1):
            if minVal > list1[a]:
                return a+1

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc >= 6), "Error: not enough arguments. Proper syntax: python3 plotVAC.py  [numDelta] [minDelta] [maxDelta] [maxDt] [filenames...]"
    assert (argc < 9), "Error: too many files. Sorry, I haven't yet built this to handle more."
    filenames = []
    numDelta = int(sys.argv[1])
    minDelta = float(sys.argv[2])
    maxDelta = float(sys.argv[3])
    maxDt = float(sys.argv[4])

    for a in range(5,argc):
        filenames.append(str(sys.argv[a]))
    
    fig1, ax1 = plt.subplots(figsize=figure_size)
    fig2, ax2 = plt.subplots(figsize=figure_size)

    for fileIndex in range(len(filenames)):
        stats_np = np.load(filenames[fileIndex])
        dts_np = np.load(fiMa.swapPrefix(filenames[fileIndex], "dts_"))
        deltas_np = np.load(fiMa.swapPrefix(filenames[fileIndex], "deltas_"))
        statsName = fiMa.stripPrefix(fiMa.stripExtension(filenames[fileIndex]))

        stats_list = arMa.makeListofListsofLists(stats_np)
        dts_list = arMa.makeListOfLists(dts_np)
        deltas_list = list(deltas_np)

        maxDeltaIndex = truncateAboveIndex(deltas_list, maxDelta)
        minDeltaIndex = truncateBelowIndex(deltas_list, minDelta)

        deltas_truncated = deltas_list[minDeltaIndex:maxDeltaIndex]
        dts_truncated = dts_list[minDeltaIndex:maxDeltaIndex]
        stats_truncated = stats_list[minDeltaIndex:maxDeltaIndex]

        lenDeltas = len(deltas_truncated)
        if numDelta >=  lenDeltas:
            thisNumDelta = lenDeltas
        else:
            thisNumDelta = numDelta
        
        colors = plMa.genRGB(fileIndex, thisNumDelta)

        delta_Indices = list( np.linspace(0,lenDeltas, num=thisNumDelta, dtype=int))
        for deltaIndex in delta_Indices:
            thisDelta = deltas_truncated[deltaIndex]
            theseDts = dts_truncated[deltaIndex]

            maxDtIndex = truncateAboveIndex(theseDts, maxDt)
            theseDts_truncated = theseDts[0:maxDtIndex]
            theseRescaledDts = theseDts_truncated / thisDelta
            thisNumDts = len(theseDts)
            these_Stats = stats_truncated[deltaIndex][0:maxDtIndex]
            theseVACs = []
            for dtIndex in range(thisNumDts):
                theseVACs.append( these_Stats[dtIndex][0] )
            thisName = statsName + "_delta_{0:6.4f}s".format(thisDelta)
            fig1, ax1 = plotVAC(fig1, ax1, theseDts_truncated, theseVACs, thisName, deltaIndex, colors)
            fig2, ax2 = plotVAC(fig2, ax2, theseRescaledDts, theseVACs, thisName, deltaIndex, colors)
            

    ax1.set_title("Velocity Autocorrelation vs Time")
    ax2.set_title("Velocity Autocorrelation vs Rescaled Time")
    ax1.set_xlim(0.0, maxDt)
    ax2.set_xlim(0.0, maxDt / minDelta)
    ax1.hlines(-0.5, 0.0, maxDt, linestyles='dashed', label='VAC = -0.5', color='k')
    ax2.hlines(-0.5, 0.0, maxDt / minDelta, linestyles='dashed', label='VAC = -0.5', color='k')
    ax1.legend(loc='best')
    ax2.legend(loc='best')
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig("VAC_vs_time.pdf")
    fig2.savefig("VAC_vs_rescaledTime.pdf")
    plt.close(fig1)
    plt.close(fig2)