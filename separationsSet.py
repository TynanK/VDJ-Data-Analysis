# separationsSet.py
# Author: Tynan Kennedy
# Date: July 31, 2020

# Extract separations for an entire data set at once

import numpy as np
import separations
import sys

def separationsSet(numCells):
    cellNumbers = list(range(1,numCells+1))
    R1_files = []
    G1_files = []
    G2_files = []
    for num in cellNumbers:
        R1_files.append("R1_" + str(num) + ".npy")
        G1_files.append("G1_" + str(num) + ".npy")
        G2_files.append("G2_" + str(num) + ".npy")
    for a in range(numCells):
        _,_ = separations.extractSeparations(R1_files[a], G1_files[a], G2_files[a])
    return

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc == 2), "Imporoper inputs. Proper syntax: python3 separationsSet.py numCells"
    numCells = int(sys.argv[1])
    separationsSet(numCells)