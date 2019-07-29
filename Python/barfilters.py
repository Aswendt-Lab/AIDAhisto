""""
Created on 17.01.2019

@authors: Niklas Pallast
Department of Neurology, University Hospital Cologne

AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology
"""

import numpy as np

def getfilters(size,dark_peaks):
    SUP=size
    SCALEX=[1,2,4]
    NORIENT=6
    NBAR = np.size(SCALEX) * NORIENT
    NF = NBAR
    F = np.zeros([SUP, SUP, NF])
    hsup = (SUP - 1) / 2
    [x, y] = np.meshgrid( np.arange(-hsup,hsup+1) , np.arange(hsup,-hsup-1,-1))
    orgpts = np.reshape(np.concatenate((x,y), axis=None),[2 ,np.size(x)])

    count = 0
    for scale in range(0, np.size(SCALEX)):
        for orient in range(0, NORIENT):
            angle = np.pi * orient / NORIENT
            c = np.cos(angle)
            s = np.sin(angle)
            tempMatrix = np.array([[c, -s], [s, c]])
            rotpts = tempMatrix.dot(orgpts)
            F[:, :, count] = makefilter(SCALEX[scale], 0, 2, rotpts, SUP)
            count = count + 1



    return F



def makefilter(scale,phasex,phasey,pts,sup):
  gx=gauss1d(3*scale,0,pts[0,:],phasex)
  gy=gauss1d(scale,0,pts[1,:],phasey)
  f=normalise(np.reshape(gx*gy,[sup,sup]))
  return f

def gauss1d(sigma,mean,x,ord):
  x=x-mean
  num=x*x
  variance=sigma**2
  denom=2*variance
  g = np.exp(-num / denom) / (np.pi * denom) ** 0.5
  if ord==1:
      g = -g * (x / variance)
  if ord==2:
      g=g*((num-variance)/(variance**2))
  return g

def normalise(f):
    f=f-np.mean(f)
    f=f/np.sum(np.abs(f))
    return f

