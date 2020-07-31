# MSD.py
# Author: Tynan Kennedy
# Date: July 28, 2020

# Calculate Mean-Squared Displacement vs time for an individual separation trajectory

import numpy as np
import sys, statistics
import arrayManipulations as arMa

def singleTrajectoryAnalysis(filename):
    data = np.load(filename)
    stats, sd_all, dt_all = MSD(data)
    np.save("stats_MSD_" + filename, stats)
    dt_np = np.array(dt_all)
    np.save("dt_MSD_" + filename, dt_np)
    sd_np = arMa.makeArray(sd_all)
    np.save("sd_MSD_" + filename, sd_np)
    return stats, sd_all, dt_all

def MSD(data):
    (i,j) = data.shape
    sd_all = []
    dt_all = []
    for a in range(i-1):
        for b in range(a,i-1):
            dt = abs(data[b,1] - data[a,1])
            sd = math.pow((data[b,0] - data[a,0]), 2)
            if dt in dt_all:
                dt_ind = dt_all.index(dt)
                sd_all[dt_ind].append(sd)
            else:
                dt_all.append(dt)
                sd_all.append([sd])
    dt_all_sorted = dt_all.sort()
    if dt_all_sorted != dt_all:
        sd_all = [x for _,x in sorted(zip(dt_all,sd_all))]
        dt_all = dt_all_sorted
    stats = np.zeros((len(dt_all), 3)) # msd, std, dt
    for a in range(len(dt_all)):
        stats[a,2] = dt_all[a]
        stats[a,0] = statistics.mean(sd_all[a])
        stats[a,1] = statistics.stdev(sd_all[a])

    return stats, sd_all, dt_all

if __name__ == "__main__":
    assert (sys.argv==2), "Incorrect number of command line arguments. Proper syntax: python3 MSD.py trajectory
    filename = str(sys.argv[1])
    x = singleTrajectoryAnalysis(filename)