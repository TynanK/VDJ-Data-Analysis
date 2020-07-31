# diffusionAnalysis.py
# Author: Tynan Kennedy
# Date: July 29, 2020

# Weighted least-squares linear regression to determine Diffusion Coefficient and power law
# TO-DO: Incorporate measurement localization error. Currently only using random deviation.

import numpy as np
import sys, statistics, math


def diffusionAnalysis(stats):

    (i,j) = stats.shape
    logStats = np.zeros((i,j))
    for a in range(i):
        logStats[a,0] = math.log(stats[a,0])
        logStats[a,2] = math.log(stats[a,2])
        logStats[a,1] = stats[a,1] / abs(stats[a,0])
    weights = np.zeros(i)
    for a in range(i):
        if stats[a,1] != 0:
            weights[a] = math.pow(logStats[a,1], -2)
        else:
            weights[a] = 0

    A = fitA(logStats[:,2], logStats[:,0], weights)
    B = fitB(logStats[:,2], logStats[:,0], weights)
    dA = fitdA(logStats[:,2], weights)
    dB = fitdB(logStats[:,2], weights)
 
    D = math.exp(A) / 6.0
    dD = D * dA

    Alpha = B
    dAlpha = dB

    diffStats = np.array([Alpha, D, dAlpha, dD])

    return diffStats

def fitA(x, y, w):
    Delta = fitDelta(x, w)

    sumWX2 = 0
    sumWY = 0
    sumWX = 0
    sumWXY = 0

    for a in range(x.size):
        sumWX2 += w[a]*math.pow(x[a], 2)
        sumWY += w[a]*y[a]
        sumWX += w[a]*x[a]
        sumWXY += w[a]*x[a]*y[a]

    A = ((sumWX2 * sumWY) - (sumWX * sumWXY)) / Delta

    return A

def fitB(x, y, w):
    Delta = fitDelta(x, w)

    sumW = 0
    sumWXY = 0
    sumWX = 0
    sumWY = 0

    for a in range(x.size):
        sumW += w[a]
        sumWY += w[a]*y[a]
        sumWX += w[a]*x[a]
        sumWXY += w[a]*x[a]*y[a]
    
    B = ((sumW * sumWXY) - (sumWX * sumWY)) / Delta

    return B

def fitdA(x, w):
    Delta = fitDelta(x, w)

    sumWX2 = 0

    for a in range(x.size):
        sumWX2 += w[a]*math.pow(x[a],2)

    dA = math.sqrt(sumWX2 / Delta)

    return dA

def fitdB(x, w):
    Delta = fitDelta(x, w)

    sumW = 0

    for a in range(x.size):
        sumW += w[a]

    dB = math.sqrt(sumW / Delta)

    return dB

def fitDelta(x, w):
    sumW = 0
    sumWX2 = 0
    sumWX = 0

    for a in range(x.size):
        sumW += w[a]
        sumWX += w[a]*x[a]
        sumWX2 += w[a]*math.pow(x[a],2)
    
    Delta = sumW * sumWX2 - math.pow(sumWX, 2)

    return Delta

if __name__ == "__main__":
    argc = len(sys.argv)
    assert (argc == 5), "Incorrect number of arguments. Proper syntax: python3 diffusionAnalysis.py [stats.npy] [Output Prefix] [dt_min] [dt_max]"
    filename = str(sys.argv[1])
    dt_min = float(sys.argv[3])
    dt_max = float(sys.argv[4])
    prefix = str(sys.argv[2])

    stats = np.load(filename)
    (i,j) = stats.shape
    if dt_min <= stats[0,2]:
        mindex = 0
    else:
        for a in range(i):
            if dt_min <= stats[a,2]:
                mindex = a
                break
    if dt_max >= stats[i-1,2]:
        maxdex = i-1
    else:
        for a in range(i):
            if dt_max >= stats[i-1-a,2]:
                maxdex = i-a
                break
    
    diffStats = diffusionAnalysis(stats[mindex:maxdex,:])
    np.save(prefix + "_" + filename, diffStats)

    print(diffStats)