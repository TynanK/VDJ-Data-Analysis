# separations.py
# Author: Tynan Kennedy
# Date: July 28, 2020

# Script to calculate separations of DJ and V segments from Megan's experimental data

import numpy as np
import sys
import filenameManipulations as fiMa

def separations(data1, data2):
    (i1,j1) = data1.shape
    (i2,j2) = data2.shape
    assert (i1==i2 and j1==j2), "Data indices don't match."

    seps = np.zeros((i1, 3)) #sep, time, flag
    for a in range(i1):
        seps[a,0] = np.linalg.norm(data1[a,0:3] - data2[a,0:3])
        assert (data1[a,4] == data2[a,4]), "Mismatched times. Look closer."
        seps[a,1] = data1[a,4]
        if data1[a,5] == 1 or data2[a,5] == 1:
            seps[a,2] = 1
    
    return seps

if __name__ == "__main__":
    assert (sys.argv==4), "Incorrect number of command line arguments. Proper syntax: python3 separations.py R1_*.npy G1_*.npy G2_*.npy"
    R1_filename = str(sys.argv[1])
    G1_filename = str(sys.argv[2])
    G2_filename = str(sys.argv[3])
    R1 = np.load(R1_filename)
    G1 = np.load(G1_filename)
    G2 = np.load(G2_filename)

    DJDJ = separations(G1, G2)
    VDJ = separations(G1, R1)

    DJDJ_filename = fiMa.swapPrefix(R1_filename, "DJDJ")
    VDJ_filename = fiMa.swapPrefix(R1_filename, "VDJ")

    np.save(DJDJ_filename, DJDJ)
    np.save(VDJ_filename, VDJ)