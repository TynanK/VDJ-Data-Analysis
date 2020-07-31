# importData.py
# Author: Tynan Kennedy
# Date: July 28, 2020

# Script to import experimental VDJ data from CSV files, formatted by Megan Aubrey

import numpy as np
import sys, csv
import filenameManipulations as fiMa

def importData(filename, timestep):
    timeStepColumn = getLastColumnNumber(filename)
    rawData = np.genfromtxt(filename, delimiter=',', usecols=(0,1,2,timeStepColumn), missing_values='', filling_values=-1)
    flaggedData = flagMissing(rawData)
    trimmedData = trimMissingEnds(flaggedData)
    interpolatedData = interpolateMissing(trimmedData)
    timedData = stepsToTime(interpolatedData, timestep)
    newName = fiMa.swapExtension(filename, 'npy')
    np.save(newName, timedData)
    return timedData

def getLastColumnNumber(filename):
    # Assumes there will be a timestep 1
    with open(filename) as f:
        csvreader = csv.reader(f, delimiter=",")
        for row in csvreader:
            return len(row) - 1


def flagMissing(rawData):
    (i, j) = rawData.shape
    flaggedData = np.zeros((i,j+1))
    flaggedData[:,0:j] = rawData
    for a in range(i):
        if (rawData[a,0]==float(-1)):
            flaggedData[a,j] = 1
    return flaggedData

def trimMissingEnds(flaggedData):
    (i,j) = flaggedData.shape
    if flaggedData[0,j-1] == 1:
        a = 1
        firstData = -1
        while firstData == -1:
            if flaggedData[a,j-1] != 1:
                firstData == a
            else:
                a += 1
        flaggedData = flaggedData[firstData:,:]
    if flaggedData[i-1,j-1] == 1:
        a = i-2
        lastData = -1
        while lastData == -1:
            if flaggedData[a,j-1] != 1:
                lastData = a
            else:
                a -= 1
        flaggedData = flaggedData[:lastData+1,:]
    
    return flaggedData
    

def interpolateMissing(flaggedData):
    (i, j) = flaggedData.shape
    interpolatedData = np.zeros((i,j))

    a = 0
    while a < i:
        if flaggedData[a,j-1] != 1:
            interpolatedData[a,:] = flaggedData[a,:]
            a += 1
        else:
            startFlag = a
            b = a + 1
            endFlag = -1
            while endFlag == -1:
                if flaggedData[b,j-1] == 1:
                    b += 1
                else:
                    endFlag = b
            interpolatedData[startFlag:endFlag,:] = interpolate(flaggedData[startFlag-1:endFlag+1,:])
            a = endFlag
    return interpolatedData
    

def interpolate(dataRange):
    (i,j) = dataRange.shape
    start = dataRange[0,:]
    end = dataRange[i-1,:]
    slope = (end[0:3] - start[0:3]) / (end[3] - start[3])
    interpolatedDataRange = np.zeros((i-2,j))
    for a in range(1,i-1):
        interpolatedDataRange[a-1,0:3] = dataRange[0,0:3] + ( slope * (dataRange[a,3] - dataRange[0,3]) )
        interpolatedDataRange[a-1,3:] = dataRange[a,3:]
    return interpolatedDataRange

def stepsToTime(data, timestep):
    (_,j) = data.shape
    data[:,j-2] = data[:,j-2] * timestep
    return data

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc >= 3), "Incorrect number of command line arguments. Proper syntax: python3 importData.py timestep [filenames]"
    filenames = []
    timestep = float(sys.argv[1])
    for a in range(2,argc):
        filenames.append(str(sys.argv[a]))
    for file1 in filenames:
        importData(file1, timestep)