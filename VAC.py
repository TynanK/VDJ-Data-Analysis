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
    stats, correlations, dts = VAC(data1, data2)

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
    np.save(outStatsName, stats)

    outDtsName = "dts_VAC_" + dataType + "_" + fiMa.stripPrefix(dataFile2)
    dts_np = np.array(dts)
    np.save(outDtsName, dts_np)

    outCorrelationsName = "corr_VAC_" + dataType + "_" + fiMa.stripPrefix(dataFile2)
    corr_np = arMa.makeArray(correlations)
    np.save(outCorrelationsName, corr_np)

    return stats, correlations, dts

def VAC(data1, data2):
    (_,j) = data1.shape
    times1 = list(data1[:,3])
    times2 = list(data2[:,3])
    sharedTimes = list(set(times1) & set(times2))
    lenT = len(sharedTimes)

    seps = np.zeros((lenT, j))

    for a in range(lenT):
        data1index = times1.index(sharedTimes[a])
        data2index = times2.index(sharedTimes[a])
        seps[a,0:3] = data2[data2index,0:3] - data1[data2index,0:3]
        seps[a,3] = sharedTimes[a]
        if data1[data1index,4] == 1 or data2[data2index,4] == 1:
            seps[a,4] = 1
    
    
    vels = np.zeros((lenT-1, j))
    for a in range(lenT-1):
        vels[a,0:3] = (seps[a+1,0:3] - seps[a,0:3]) / (seps[a+1,3] - seps[a,3])
        vels[a,3] = (seps[a+1,3] + seps[a,3]) / 2
        if seps[a+1,4] == 1 or seps[a,4] == 1:
            vels[a,4] = 1
    
    unitVels = np.zeros(vels.shape)
    unitVels[:,3:5] = vels[:,3:5]
    mags = np.linalg.norm(vels[:,0:3], axis=1)

    for a in range(lenT-1):
        if mags[a] != 0:
            unitVels[a,0:3] = vels[a,0:3] / mags[a]
    
    correlations = []
    dts = []

    for a in range(lenT-2):
        for b in range(a,lenT-1):
            dt = abs(unitVels[b,3] - unitVels[a,3])
            corr = np.dot(unitVels[b,0:3], unitVels[a,0:3])
            if dt in dts:
                dt_ind = dts.index(dt)
                correlations[dt_ind].append(corr)
            else:
                dts.append(dt)
                correlations.append([corr])
    
    dts_sorted = dts
    dts_sorted.sort()
    if dts_sorted != dts:
        correlations = [x for _,x in sorted(zip(dts, correlations))]
        dts = dts_sorted
    
    stats = np.zeros((len(dts), 3)) # meanVAC, stdDev, dt

    for a in range(len(dts)):
        stats[a,2] = dts[a]
        stats[a,0] = statistics.mean(correlations[a])
        if len(correlations[a]) >= 2:
            stats[a,1] = statistics.stdev(correlations[a])
    
    return stats, correlations, dts

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc == 3), "Improper inputs. Input syntax: python3 VAC.py [dataFile1] [dataFile2]"
    dataFile1 = str(sys.argv[1])
    dataFile2 = str(sys.argv[2])

    x = singleTrajectoryAnalysis(dataFile1, dataFile2)