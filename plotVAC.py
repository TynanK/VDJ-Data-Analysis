# plotVAC.py
# Author: Tynan Kennedy
# Date: July 30, 2020

# Plots a given VAC vs dt onto the figure and axis passed to the function
# Command line syntax: python3 plotVAC.py [filenames] ...
# Where the filenames are of the form stats.npy

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, statistics, math, pickle
import filenameManipulations as fiMa

colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']

figure_size = (10,10)

def plotVAC(stats, fig, ax, statsName, intLabel):

    ax.plot(stats[:,2], stats[:,0], label=statsName, color=colors[intLabel], marker='.', linestyle='none')
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("VAC")
    ax.set_title("Velocity Autocorrelation vs Time")
    ax.set_xlim(0, max(stats[:,2]))
    ax.set_ylim(-1.0, 1.0)
    fig.tight_layout()

    return fig, ax


if __name__ == "__main__":
    argc = len(sys.argv)
    filenames = []
    for a in range(1,argc):
        filenames.append(str(sys.argv[a]))
    
    fig, ax = plt.subplots(figsize=figure_size)

    for index in range(len(filenames)):
        stats = np.load(filenames[index])
        statsName = fiMa.stripExtension(filenames[index])
        fig, ax = plotVAC(stats, fig, ax, statsName, index)
    
    xmin, xmax = ax.get_xlim()
    ax.hlines(-0.5, xmin, xmax, linestyles='dashed', label='VAC = -0.5', color='k')
    ax.legend()
    fig.tight_layout()
    fig.savefig("VAC.pdf")
    # pickle.dump(ax, file('VAC.pickle', 'w')) # Can reload this using pickle.load('VAC.pickle'), then plt.show()
    plt.close(fig)