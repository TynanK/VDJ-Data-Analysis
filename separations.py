# separations.py
# Author: Tynan Kennedy
# Date: July 28, 2020

# Script to calculate separations of DJ and V segments from Megan's experimental data

import numpy as np
import sys
import filenameManipulations as fiMa

def extractSeparations(R1_filename, G1_filename, G2_filename):
    R1 = np.load(R1_filename)
    G1 = np.load(G1_filename)
    G2 = np.load(G2_filename)

    DJDJ = separations(G1, G2)
    VDJ = separations(G1, R1)

    DJDJ_filename = fiMa.swapPrefix(R1_filename, "DJDJ_")
    VDJ_filename = fiMa.swapPrefix(R1_filename, "VDJ_")

    np.save(DJDJ_filename, DJDJ)
    np.save(VDJ_filename, VDJ)

    return DJDJ, VDJ

def separations(data1, data2):
    times1 = list(data1[:,3])
    times2 = list(data2[:,3])

    sharedTimes = list(set(times1) & set(times2))
    lenT = len(sharedTimes)
    seps = np.zeros((lenT, 3)) #sep, time, flag
    for a in range(lenT):
        time1index = times1.index(sharedTimes[a])
        time2index = times2.index(sharedTimes[a])
        seps[a,0] = np.linalg.norm(data1[time1index,0:3] - data2[time2index,0:3])
        assert (data1[time1index,3] == data2[time2index,3]), "Mismatched times. Look closer."
        seps[a,1] = sharedTimes[a]
        if data1[time1index,4] == 1 or data2[time2index,4] == 1:
            seps[a,2] = 1
    
    return seps

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc==4), "Incorrect number of command line arguments. Proper syntax: python3 separations.py R1_*.npy G1_*.npy G2_*.npy"
    R1_filename = str(sys.argv[1])
    G1_filename = str(sys.argv[2])
    G2_filename = str(sys.argv[3])
    x = extractSeparations(R1_filename, G1_filename, G2_filename)