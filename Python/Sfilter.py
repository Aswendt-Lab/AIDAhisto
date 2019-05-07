""""
Created on 17.01.2019

@authors: Niklas Pallast
Department of Neurology, University Hospital Cologne

AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology
"""

import numpy as np

def getfilters(size,dark_peaks):
    NF = 13 # Number of filters
    SUP = size
    F = np.zeros([SUP, SUP, NF])

    F[:,:, 0]=makefilter(SUP, 2, 1)
    F[:,:, 1]=makefilter(SUP, 4, 1)
    F[:,:, 2]=makefilter(SUP, 4, 2)
    F[:,:, 3]=makefilter(SUP, 6, 1)
    F[:,:, 4]=makefilter(SUP, 6, 2)
    F[:,:, 5]=makefilter(SUP, 6, 3)
    F[:,:, 6]=makefilter(SUP, 8, 1)
    F[:,:, 7]=makefilter(SUP, 8, 2)
    F[:,:, 8]=makefilter(SUP, 8, 3)
    F[:,:, 9]=makefilter(SUP, 10, 1)
    F[:,:, 10]=makefilter(SUP, 10, 2)
    F[:,:, 11]=makefilter(SUP, 10, 3)
    F[:,:, 12]=makefilter(SUP, 10, 4)



    return F

def makefilter(sup, sigma, tau):
    hsup = (sup - 1) / 2
    [x, y] =np.meshgrid(np.arange(-hsup,hsup+1),np.arange(-hsup,hsup+1))
    r = (x * x + y * y)**0.5
    f = np.cos(r * (np.pi * tau / sigma)) * np.exp(-(r * r) / (2 * sigma * sigma))
    f = f - np.mean(f)
    f = f/(np.sum(np.abs(f)))
    return f
