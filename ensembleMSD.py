# ensembleMSD.py
# Author: Tynan Kennedy
# Date: July 29, 2020

# Calculate the MSD vs time from an ensemble of cells. Input filenames should be the separations files
# The script will check if they've already been processed, and do so if need be.

import numpy as np
import sys, statistics, os
import MSD
import arrayManipulations as arMa


def ensembleAnalysis(filenames, dataType):
    stats, sd_ensemble, dt_ensemble = ensembleMSD(filenames)
    np.save("stats_MSD_" + dataType + "_ensemble.npy", stats)
    dt_np = np.array(dt_ensemble)
    np.save("dt_MSD_" + dataType + "_ensemble.npy", dt_np)
    sd_np = arMa.makeArray(sd_ensemble)
    np.save("sd_MSD_" + dataType + "_ensemble.npy", sd_np)
    return stats, sd_ensemble, dt_ensemble
    


def ensembleMSD(filenames):
    currentDir = os.getcwd()
    sd_ensemble = []
    dt_ensemble = []
    for file1 in filenames:
        dt_filename = currentDir + "/dt_" + file1
        sd_filename = currentDir + "/sd_" + file1
        if os.path.isfile(dt_filename) and os.path.isfile(sd_filename):
            dt_data = np.load(dt_filename)
            sd_data = np.load(sd_filename)
        else:
            stats, sd_data, dt_data = MSD.singleTrajectoryAnalysis(file1)
        
        (i,_) = sd_data.shape
        k = dt_data.size
        assert (i==k), "sd and dt data mismatch in: " + file1

        sd_list = arMa.makeListOfLists(sd_data)
        dt_list = list(dt_data)
        
        sd_ensemble, dt_ensemble = arMa.mergeLists(sd_ensemble, dt_ensemble, sd_list, dt_list)
            
    stats = np.zeros((len(dt_ensemble), 3)) # msd, std, dt
    for a in range(len(dt_ensemble)):
        stats[a,2] = dt_ensemble[a]
        stats[a,0] = statistics.mean(sd_ensemble[a])
        stats[a,1] = statistics.stdev(sd_ensemble[a])

    return stats, sd_ensemble, dt_ensemble

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc == 3), "Incorrect input format. Proper syntax: python3 ensembleMSD.py [DJDJ/VDJ] [# cells]"
    dataType = str(sys.argv[1])
    numCells = int(sys.argv[2])

    assert (dataType == "DJDJ" or dataType == "VDJ"), "Improper data type chosen. Please choose either DJDJ or VDJ"
    assert (numCells >= 1), "Please choose a positive, integer number of cells"
    nums = list(range(1,numCells+1))
    filenames = []
    for a in range(len(nums)):
        filenames.append(dataType + "_" + str(nums[a]) + ".py")
    
    x = ensembleAnalysis(filenames, dataType)