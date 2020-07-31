# VDJ-Data-Analysis
Code for analysing experimental data

So far, I've written code that can do the following:

1. Import data
    -Load CSV files into numpy arrays
    -If data points are missing, flag for interpolation
    -Iterate through array, looking for flags. When found, find next non-flagged entry, and interpolate values for all points in between
2. Calculate separations
3. Calculate mean-squared displacement vs time
    -Keep track of number of data points for uncertainty calculation in scaling fit
    -Do an uncertainty-weighted fit for diffusion coefficient and exponent
    -Plots of time- and velocity-averaged MSD for each condition
4. Calculate velocity autocorrelations
    -Again, be mindful of uncertainties
    -Kees and Olga spoke of the depth of the dip, for which the theoretical maximum is -0.5. Make sure to note this depth on each plot
5. Plot time-distributions of V-DJ distances for each trajectory, colored to match the trajectories themselves. Compare degree of overlap for JQ1 trajectories vs wild type


Currently in the debugging stage.
