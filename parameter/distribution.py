#!/usr/bin/env python3

"""
<file>    distribution.py
<brief>   get best distribution
"""

from distfit import distfit
import matplotlib.pyplot as plt
import numpy as np

def optimal_distribution(X, file):
    #dfit = distfit(distr='full') # initialize model
    dfit = distfit(loc=0)
    dfit.fit_transform(X)
    dfit.plot()

    dfit.summary.to_csv(file)
    #dfit.model.to_csv(file)

if __name__ == "__main__":
    X = np.random.normal(0, 2, 1000)

    dfit = distfit()
    dfit.fit_transform(X)
    
    dfit.plot(chart='pdf')
    dfit.plot(chart='cdf')
