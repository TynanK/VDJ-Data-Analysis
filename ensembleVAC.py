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
    stats_np, corr_np, dt_np, delta_np = ensembleVAC(filenames, dataType)
    np.save("stats_VAC_" + dataType + "_ensemble.npy", stats_np)
    np.save("dts_VAC_" + dataType + "_ensemble.npy", dt_np)
    np.save("corr_VAC_" + dataType + "_ensemble.npy", corr_np)
    np.save("deltas_VAC_" + dataType + "_ensemble.npy", delta_np)
    return stats_np, corr_np, dt_np, delta_np

def ensembleVAC(filenames, dataType):
    currentDir = os.getcwd()
    corr_ensemble = []
    dt_ensemble = []
    delta_ensemble = []
    for file3 in filenames:
        dt_filename = currentDir + "/dt_" + file3
        corr_filename = currentDir + "/corr_" + file3
        deltas_filename = currentDir + "/deltas_" + file3
        if os.path.isfile(dt_filename) and os.path.isfile(corr_filename) and os.path.isfile(deltas_filename):
            dt_data = np.load(dt_filename)
            corr_data = np.load(corr_filename)
            delta_data = np.load(deltas_filename)
        else:
            if dataType == 'VDJ':
                file1 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "R1_")
                file2 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "G1_")
            elif dataType == 'DJDJ':
                file1 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "G1_")
                file2 = fiMa.swapPrefix(fiMa.stripPrefix(file3), "G2_")
            else:
                assert (1==0), "Improper dataType"
            
            stats, corr_data, dt_data, delta_data = VAC.singleTrajectoryAnalysis(file1, file2)
    
        corr_list = arMa.makeListofListsofLists(corr_data)
        dt_list = arMa.makeListOfLists(dt_data)
        delta_list = list(delta_data)

        corr_ensemble, delta_ensemble, dt_ensemble = arMa.mergeLists3D(corr_ensemble, delta_ensemble, dt_ensemble, corr_list, delta_list, dt_list)

    stats = VAC.statsVAC(corr_ensemble, delta_ensemble, dt_ensemble)

    # This function is expected to return numpy arrays, so let's convert everything now
    stats_np = arMa.makeArray3D(stats)
    corr_np = arMa.makeArray3D(corr_ensemble)
    dt_np = arMa.makeArray(dt_ensemble)
    delta_np = np.array(delta_ensemble)

    return stats_np, corr_np, dt_np, delta_np

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