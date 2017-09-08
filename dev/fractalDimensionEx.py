#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 10:25:45 2017

example of power law alpha (or fractal dimension 'D') parameter
estimation using the data from avalanche
"""
import numpy as np
import matplotlib.pyplot as plt

#Note: Nvoxels comes from avalanche.py, and corresponds to the number of
#voxels in a particular avalance:

#num parameter shouldn't greatly influence the estimate
scales=np.logspace(0.5, np.log(max(Nvoxels)+1), num=100, endpoint=True, base=np.exp(1))

#Determine the Density, P(s), of avalanches per bin:
hist, bin_edges = np.histogram(Nvoxels, bins=scales, density='true')

#for plotting and predicting, use mean of adjacent the log(bin)
#since we have more bins than hist data, this also reduces the vector
#size to match the hist data returned above.
lscales = (np.log(scales[1:])+np.log(scales[:-1]))/2
#remove zeros:
lscales = lscales[hist>0]
hist = hist[hist>0]

x = np.polyfit(x=lscales,y=np.log(hist),deg=1)
#fractal dimension is the first coefficient returned:
D = x[0]

plt.scatter(x=lscales,y=np.log(hist))