# VAC.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# Input: position data files
# Output: Velocity Autocorrelation data file

# Note: Should come back and functionalize this code more. But I'm in a hurry.

import numpy as np
import sys, statistics, math
import filenameManipulations as fiMa
import arrayManipulations as arMa

def singleTrajectoryAnalysis(dataFile1, dataFile2):
    data1 = np.load(dataFile1)
    data2 = np.load(dataFile2)
    stats_np, corr_np, dts_np, deltas_np = VAC(data1, data2)

    prefix1 = fiMa.extractPrefix(dataFile1)
    prefix2 = fiMa.extractPrefix(dataFile2)

    VDJ_prefixes = ['R1', 'G1']
    DJDJ_prefixes = ['G1', 'G2']

    if (prefix1 in VDJ_prefixes) and (prefix2 in VDJ_prefixes):
        dataType = 'VDJ'
    elif (prefix1 in DJDJ_prefixes) and (prefix2 in DJDJ_prefixes):
        dataType = 'DJDJ'
    else:
        assert (1==0), "Improper input file prefixes. Need a pair of either R1/G1 or G1/G2"

    outStatsName = "stats_VAC_" + dataType + "_" + fiMa.stripPrefix(dataFile2)
    np.save(outStatsName, stats_np)

    outDtsName = "dts_VAC_" + dataType + "_" + fiMa.stripPrefix(dataFile2)
    np.save(outDtsName, dts_np)

    outCorrelationsName = "corr_VAC_" + dataType + "_" + fiMa.stripPrefix(dataFile2)
    np.save(outCorrelationsName, corr_np)

    outDeltasName = "deltas_VAC_" + dataType + "_" + fiMa.stripPrefix(dataFile2)
    np.save(outDeltasName, deltas_np)

    return stats_np, corr_np, dts_np, deltas_np

def VAC(data1, data2):
    (_,j) = data1.shape

    # The times for different data sets aren't necessarily going to match up, so I first need to find the timesteps shared by both data1 and data2
    times1 = list(data1[:,3])
    times2 = list(data2[:,3])
    sharedTimes = list(set(times1) & set(times2))
    lenT = len(sharedTimes)


    # Now, we calculate separation vectors only for timesteps where we have both positions
    seps = np.zeros((lenT, j))

    for a in range(lenT):
        data1index = times1.index(sharedTimes[a])
        data2index = times2.index(sharedTimes[a])
        seps[a,0:3] = data2[data2index,0:3] - data1[data1index,0:3]
        seps[a,3] = sharedTimes[a]
        if data1[data1index,4] == 1 or data2[data2index,4] == 1:
            seps[a,4] = 1
    
    # Next, we calculate unit velocities for every pair of separation vectors. This allows us to study the variation of the VAC with both the time between velocities, t, and the time over which they are averaged, delta.

    unitVels = [] # This will be a list of lists, where each item is of the form [vx vy vz delta t flag], and the velocity is normalized
    # Need to iterate over every pair of separations to fill unitVels[]

    for a in range(lenT-2):
        for b in range(a+1,lenT-1):
            thisDelta = seps[b,3] - seps[a,3]
            thisT = (seps[b,3] + seps[a,3]) / 2
            thisVel = (seps[b,0:3] - seps[a,0:3]) / thisDelta
            if seps[a,4] == 1 or seps[b,4] == 1:
                thisFlag = 1
            else:
                thisFlag = 0
            if np.linalg.norm(thisVel) != 0:
                thisUnitVel = thisVel / np.linalg.norm(thisVel)
            else:
                thisUnitVel = thisVel
            unitVels.append([thisUnitVel[0], thisUnitVel[1], thisUnitVel[2], thisDelta, thisT, thisFlag])

    # Now, to make calculating the correlations faster, it's best to organize the velocities based on delta.

    delta_list = []
    unitVels_organized = []
    len0 = len(unitVels)
    for a in range(len0):
        unitVels_organized, delta_list = arMa.dataInsert(unitVels_organized, delta_list, unitVels[a], unitVels[a][3])
    
    # Let's sort this before continuing
    unitVels_organized, delta_list = arMa.sort2D(unitVels_organized, delta_list)

    # Time to calculate correlations. Correlations will be a ListofListsofLists indexed by delta, dt, and dataType, and dts will be a ListofLists indexed by delta and dataType
    # Oh, and because of the way arMa.dataInsert3D() works, I'll be rebuilding the delta list.
    correlations = []
    dts = []
    deltas = []

    len0 = len(delta_list)

    for a in range(len0):
        len1 = len(unitVels_organized[a])
        thisDelta = delta_list[a]
        for b in range(len1):
            for c in range(b,len1):
                thisCorr = np.dot(unitVels_organized[a][b][0:3], unitVels_organized[a][c][0:3])
                thisDt = abs(unitVels_organized[a][c][4] - unitVels_organized[a][b][4])
                correlations, deltas, dts = arMa.dataInsert3D(correlations, deltas, dts, thisCorr, thisDelta, thisDt)

    # Let's sort all this before continuing

    correlations, deltas, dts = arMa.sort3D(correlations, deltas, dts)
    
    # Now to calculate the statistics. Need the meanVAC, stdDev, delta, and dt. Indexed by delta and dt.
    # This will be a list of lists of lists, since [meanVAC, stdDev, delta, dt] will be the lowest-level list, and each of these lowest-level lists will be indexed by delta and dt.
    
    stats = statsVAC(correlations, deltas, dts)

    # This function is expected to return numpy arrays, so let's convert everything now

    stats_np = arMa.makeArray3D(stats)
    corr_np = arMa.makeArray3D(correlations)
    dts_np = arMa.makeArray(dts)
    deltas_np = np.array(deltas)

        
    return stats_np, corr_np, dts_np, deltas_np

def statsVAC(correlations, deltas, dts):
    stats = []

    len0 = len(correlations)

    for a in range(len0): # a indexes delta
        stats.append([])
        len1 = len(correlations[a])
        thisDelta = deltas[a]
        for b in range(len1): # b indexes dt
            thisMeanVAC = statistics.mean(correlations[a][b])
            if len(correlations[a][b]) >= 2:
                thisStdDev = statistics.stdev(correlations[a][b])
            else:
                thisStdDev = 0.0
            thisDt = dts[a][b]
            stats[a].append([thisMeanVAC, thisStdDev, thisDelta, thisDt])
    
    return stats

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc == 3), "Improper inputs. Input syntax: python3 VAC.py [dataFile1] [dataFile2]"
    dataFile1 = str(sys.argv[1])
    dataFile2 = str(sys.argv[2])

    x = singleTrajectoryAnalysis(dataFile1, dataFile2)