# importDataSet.py
# Author: Tynan Kennedy
# Date: July 31, 2020

# This script simply takes as input the number of cells, and imports all data assuming standard filenames

import numpy as np
import importData
import sys

def importDataSet(timestep, numCells):
    cellNumbers = list(range(1,numCells+1))
    R1_files = []
    G1_files = []
    G2_files = []
    for num in cellNumbers:
        R1_files.append("R1_" + str(num) + ".csv")
        G1_files.append("G1_" + str(num) + ".csv")
        G2_files.append("G2_" + str(num) + ".csv")
    for a in range(numCells):
        importData.importData(R1_files[a], timestep)
        importData.importData(G1_files[a], timestep)
        importData.importData(G2_files[a], timestep)
    return

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc == 3), "Imporoper inputs. Proper syntax: python3 importDataSet.py timestep numCells"
    timestep = float(sys.argv[1])
    numCells = int(sys.argv[2])
    importDataSet(timestep, numCells)