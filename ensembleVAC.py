# ensembleVAC.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# Performs Velocity Autocorrelation analysis for many cells.
# Won't repeat analysis that has already been done. Imports if existing.

import numpy as np
import sys, statistics, os
import arrayManipulations as arMa
import filenameManipulations as fiMa
import VAC

def ensembleAnalysis(filenames, dataType):
    stats, corr_ensemble, dt_ensemble = ensembleVAC(filenames, dataType)
    np.save("stats_VAC_" + dataType + "_ensemble.npy", stats)
    dt_np = np.array(dt_ensemble)
    np.save("dt_VAC_" + dataType + "_ensemble.npy", dt_np)
    corr_np = arMa.makeArray(corr_ensemble)
    np.save("corr_VAC_" + dataType + "_ensemble.npy", corr_np)
    return stats, corr_ensemble, dt_ensemble

def ensembleVAC(filenames, dataType):
    currentDir = os.getcwd()
    corr_ensemble = []
    dt_ensemble = []
    for file3 in filenames:
        dt_filename = currentDir + "/dt_" + file3
        corr_filename = currentDir + "/corr_" + file3
        if os.path.isfile(dt_filename) and os.path.isfile(corr_filename):
            dt_data = np.load(dt_filename)
            corr_data = np.load(corr_filename)
        else:
            if dataType == 'VDJ':
                file1 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "R1_")
                file2 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "G1_")
            elif dataType == 'DJDJ':
                file1 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "G1_")
                file2 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "G2_")
            else:
                assert (1==0), "Improper dataType"
            
            stats, corr_data, dt_data = VAC.singleTrajectoryAnalysis(file1, file2)
    
        (i,_) = corr_data.shape
        k = dt_data.size
        assert (i==k), "corr and dt data mismatch in: " + file3

        corr_list = arMa.makeListOfLists(corr_data)
        dt_list = list(dt_data)

        corr_ensemble, dt_ensemble = arMa.mergeLists(corr_ensemble, dt_ensemble, corr_list, dt_list)

    stats = np.zeros((len(dt_ensemble), 3))
    for a in range(len(dt_ensemble)):
        stats[a,2] = dt_ensemble[a]
        stats[a,0] = statistics.mean(corr_ensemble[a])
        stats[a,1] = statistics.stdev(corr_ensemble[a])

    return stats, corr_ensemble, dt_ensemble

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc == 3), "Incorrect input format. Proper syntax: python3 ensembleVAC.py [DJDJ/VDJ] [# cells]"
    dataType = str(sys.argv[1])
    numCells = int(sys.argv[2])

    assert (dataType == "DJDJ" or dataType == "VDJ"), "Improper data type chosen. Please choose either DJDJ or VDJ"
    assert (numCells >= 1), "Please choose a positive, integer number of cells"
    nums = list(range(1,numCells+1))
    filenames = []
    for a in range(len(nums)):
        filenames.append("VAC_" + dataType + "_" + str(nums[a]) + ".npy")
    
    x = ensembleAnalysis(filenames, dataType)