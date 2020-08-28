# ensembleMSD.py
# Author: Tynan Kennedy
# Date: July 29, 2020

# Calculate the MSD vs time from an ensemble of cells. Input filenames should be the separations files
# The script will check if they've already been processed, and do so if need be.
# THIS SCRIPT TAKES AS INPUTS RADIAL MSD DATA, AND OUTPUTS GENOMIC MSD DATA. BEWARE!
# EXPLANATION: I calculate the genomic MSD by estimating the measurement error's effect on the MSD. I do this by estimating the value of MSD at time dt=0, using
# a linear fit of the smallest 7 values of dt. Then I subtract this value from every point except dt=0.
# Because this involves a fit, I thought it best to do at the stage where we've compiled the most data to minimize uncertainty.

import numpy as np
import sys, statistics, os
import MSD
import arrayManipulations as arMa
import math

msd_err = 0.02

def ensembleAnalysis(filenames, dataType):
    stats = ensembleMSDalltogether(filenames)
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
    # dt_mean_ensemble = []
    # dt_std_ensemble = []
    # means_ensemble = []
    # stds_ensemble = []
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
            # means_ensemble, dt_mean_ensemble = arMa.dataInsert(means_ensemble, dt_mean_ensemble, stats[dtIndex,0], dt_data[dtIndex])
            # stds_ensemble, dt_std_ensemble = arMa.dataInsert(stds_ensemble, dt_std_ensemble, stats[dtIndex,1], dt_data[dtIndex])

    # So now, stats_ensemble is a list of lists of numpy arrays, and dt_ensemble is a list
    # We will perform a weighted average of each MSD in the ensemble, with the weights equal to the inverse of the variance for each point

    # assert (dt_mean_ensemble == dt_std_ensemble), "Something went wrong"
    lenDt = len(dt_ensemble)
    finalStats = np.zeros((lenDt, 3))
    if dt_ensemble[0] == 0:
        for a in range(1,lenDt):
            finalStats[a,2] = dt_ensemble[a]
            thisMean, thisSD = weightedMean(stats_ensemble[a])
            finalStats[a,0] = 3 * thisMean # Multiple of three comes from converting the radial MSD to the genomic MSD.
            finalStats[a,1] = 3 * thisSD

    else:
        for a in range(lenDt):
            finalStats[a,2] = dt_ensemble[a]
            thisMean, thisSD = weightedMean(stats_ensemble[a])
            finalStats[a,0] = 3 * thisMean # Multiple of three comes from converting the radial MSD to the genomic MSD.
            finalStats[a,1] = 3 * thisSD
  
    # Oho, but what's this? We have some experimental error that makes the y-intercept non-zero!
    # I tried assuming it's the same for every cell type, but that might be incorrect.
    # We'll extrapolate it from a linear fit of the first 7 non-zero dts, then subtract it.

    if dt_ensemble[0] == 0:
        dt_slice = dt_ensemble[1:8]
        statSlice = finalStats[1:8,0]
        linearFit = np.polyfit(dt_slice, statSlice, 1)
        intercept = linearFit[0]
        finalStats[1:,0] = finalStats[1:,0] - intercept
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
    
def weightedMean(stats_list): # Replaced dataList, standardDeviationList
    lenList = len(stats_list)
    dataList = []
    standardDeviationList = []
    for a in range(lenList):
        thisArray = stats_list[a]
        dataList.append(thisArray[0])
        standardDeviationList.append(thisArray[1])
    weightsList = []
    for a in range(len(standardDeviationList)):
        # weightsList.append(1.0)
        if standardDeviationList[a] != 0:
            weightsList.append(math.pow(standardDeviationList[a] / dataList[a], -2))
        else:
            weightsList.append(0.0)
    sumW = sum(weightsList)
    assert (sumW != 0), "Sum of weights equals 0. How'd you manage to do that?"
    assert (len(dataList) == len(weightsList)), "Mismatched list lengths"
    meanData = 0
    for a in range(len(dataList)):
        meanData += dataList[a]*weightsList[a]/sumW
    sdOfMean = math.sqrt(1 / sumW)
    return meanData, sdOfMean

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
        stats[a,1] = 3 * statistics.stdev(sd_ensemble[a]) / math.sqrt(len(sd_ensemble[a]))

    # Oho, but what's this? We have some experimental error that makes the y-intercept non-zero!
    # I tried assuming it's the same for every cell type, but that might be incorrect.
    # We'll extrapolate it from a linear fit of the first 7 non-zero dts, then subtract it.

    if dt_ensemble[0] == 0:
        dt_slice = dt_ensemble[1:8]
        statSlice = stats[1:8,0]
        linearFit = np.polyfit(dt_slice, statSlice, 1)
        intercept = linearFit[0]
        stats[1:,0] = stats[1:,0] - intercept
        stats[1:,1] = stats[1:,1] + intercept
    else:
        dt_slice = dt_ensemble[0:7]
        statSlice = stats[0:7,0]
        linearFit = np.polyfit(dt_slice, statSlice, 1)
        intercept = linearFit[0]
        stats[:,0] = stats[:,0] - intercept
        stats[:,1] = stats[:,1] + intercept

    # Stats: [dtIndex] [MSD | stddev | dt]

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