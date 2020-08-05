# ensembleMSD.py
# Author: Tynan Kennedy
# Date: July 29, 2020

# Calculate the MSD vs time from an ensemble of cells. Input filenames should be the separations files
# The script will check if they've already been processed, and do so if need be.

import numpy as np
import sys, statistics, os
import MSD
import arrayManipulations as arMa
import math

msd_err = 0.02

def ensembleAnalysis(filenames, dataType):
    stats = ensembleMSD(filenames)
    np.save("stats_MSD_" + dataType + "_ensemble.npy", stats)
    #dt_np = np.array(dt_ensemble)
    #np.save("dt_MSD_" + dataType + "_ensemble.npy", dt_np)
    #sd_np = arMa.makeArray(sd_ensemble)
    #np.save("sd_MSD_" + dataType + "_ensemble.npy", sd_np)
    return stats
    
def ensembleMSD(filenames):
    currentDir = os.getcwd()
    stats_ensemble = []
    dt_ensemble = []
    dt_mean_ensemble = []
    dt_std_ensemble = []
    means_ensemble = []
    stds_ensemble = []
    for file1 in filenames:
        stats_filename = currentDir + "/stats_" + file1
        if os.path.isfile(stats_filename):
            stats = np.load(stats_filename)
            dt_data = stats[:,2]
        else:
            stats, _, dt_data = MSD.singleTrajectoryAnalysis(file1)
        
        lenDt = len(dt_data)
        for dtIndex in range(lenDt):
            stats_ensemble, dt_ensemble = arMa.dataInsert(stats_ensemble, dt_ensemble, stats[dtIndex,:], dt_data[dtIndex])
            means_ensemble, dt_mean_ensemble = arMa.dataInsert(means_ensemble, dt_mean_ensemble, stats[dtIndex,0], dt_data[dtIndex])
            stds_ensemble, dt_std_ensemble = arMa.dataInsert(stds_ensemble, dt_std_ensemble, stats[dtIndex,1], dt_data[dtIndex])

    # So now, stats_ensemble is a list of lists of numpy arrays, and dt_ensemble is a list
    # The mean of mean SDs is simple to calculate. The error will be the errors summed in quadrature, divided by the number. Do this for every dt.

    assert (dt_mean_ensemble == dt_std_ensemble), "Something went wrong"

    lenDt = len(dt_ensemble)
    finalStats = np.zeros((lenDt, 3))
    for a in range(lenDt):
        finalStats[a,2] = dt_ensemble[a]
        finalStats[a,0] = 3 * statistics.mean(means_ensemble[a])
        if len(stats_ensemble[a][:][1]) != 0:
            finalStats[a,1] = 3 * sumQuad(stds_ensemble[a]) / len(stds_ensemble[a])
        else:
            finalStats[a,1] = 0.0
    
    # Oho, but what's this? We have some experimental error that makes the y-intercept non-zero!
    # I tried assuming it's the same for every cell type, but that might be incorrect.
    # We'll extrapolate it from a linear fit of the first 7 non-zero dts, then subtract it.

    if dt_ensemble[0] == 0:
        dt_slice = dt_ensemble[1:8]
        statSlice = finalStats[1:8,0]
    else:
        dt_slice = dt_ensemble[0:7]
        statSlice = finalStats[0:7,0]
    
    linearFit = np.polyfit(dt_slice, statSlice, 1)
    intercept = linearFit[0]
    finalStats[:,0] = finalStats[:,0] - intercept

    
    return finalStats
    
def sumQuad(data):
    sumQ = 0
    for a in range(len(data)):
        sumQ += math.pow(data[a],2)
    return math.sqrt(sumQ)
    


def ensembleMSDalltogether(filenames):
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
        stats[a,0] = 3 * statistics.mean(sd_ensemble[a])
        stats[a,1] = 3 * statistics.stdev(sd_ensemble[a])

    # Oho, but what's this? We have some experimental error that makes the y-intercept non-zero!
    # I tried assuming it's the same for every cell type, but that might be incorrect.
    # We'll extrapolate it from a linear fit of the first 7 non-zero dts, then subtract it.

    if dt_ensemble[0] == 0:
        dt_slice = dt_ensemble[1:8]
        statSlice = stats[1:8,0]
    else:
        dt_slice = dt_ensemble[0:7]
        statSlice = stats[0:7,0]
    
    linearFit = np.polyfit(dt_slice, statSlice, 1)
    intercept = linearFit[0]
    stats[:,0] = stats[:,0] - intercept


    return stats

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
        filenames.append(dataType + "_" + str(nums[a]) + ".npy")
    
    x = ensembleAnalysis(filenames, dataType)