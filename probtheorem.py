# -*- coding: utf-8 -*-
"""
ALBSS Theoretical Computation Modules
S.lee
"""

import tkinter.messagebox as msgbox
import sympy as sp
import numpy as np

#Computation function for non-pity model
def normalcompute(probdata):
    t = sp.Symbol('t')
    #ccdf is the complimentary CDF of the probability model
    ccdf = 1-sp.prod([1-sp.exp(-t*p) for p in probdata])
    #Average aka expectation is the integration of ccdf
    avgpull = sp.integrate(ccdf, (t,0,sp.oo))
    #scmmt is the second moment of the model rv
    scmmt = 2*sp.integrate(t*ccdf, (t,0,sp.oo))
    #Variance and standard deviation can be computed from first and second moments
    stdev = sp.sqrt(scmmt - avgpull**2)
    #Compute median using crude numerical method
    medpull = mediancompute(ccdf, 2*int(avgpull))
    return (avgpull, medpull, stdev)

#Computation function for pity model
#This function often run out of time so in such case use pitycompute_numpy instead
def pitycompute(probdata, pity):
    t = sp.Symbol('t')
    #ccdf is a non-continuous function with discontinuity at the pity point
    #Therefore ccdf must be piecewise defined
    ccdf1 = 1-sp.prod([1-sp.exp(-t*p) for p in probdata])
    probdata.pop(0)
    ccdf2 = 1-sp.prod([1-sp.exp(-t*p) for p in probdata])
    avg1 = sp.integrate(ccdf1, (t,0,pity))
    avg2 = sp.integrate(ccdf2, (t,pity,sp.oo))
    avgpull = avg1+avg2
    medpull = mediancompute(ccdf1, 2*int(avgpull))
    return (avgpull, medpull)

#Computing median from complimentary CDF
#simpy solver often run out of time so we use very elementary brute force search    
def mediancompute(ccdf, myrange):
    t = sp.Symbol('t')    
    for i in range(myrange):
        if ccdf.subs(t,i) < 0.5:
            if ((ccdf.subs(t, i) + ccdf.subs(t, i-1))/2 > 0.5):
                return i
            else:
                return i-1
    msgbox.showerror("Error", "Median computation error")
    return 0

#Estimation probability from CDF and proposed build count
def probcompute(probdata, buildcount):
    t = sp.Symbol('t')
    cdf = sp.prod([1-sp.exp(-t*p) for p in probdata])
    return cdf.subs(t,buildcount)
    

#Computation function for pity model using numpy instead of simpy
#Here cutoff error must be defined to limit the integration interval
def pitycompute_numpy(probdata, pity):
    cutofferr = 0.001
    est = max(pity, int(np.log((2**len(probdata)) / cutofferr / probdata[0]) / probdata[0]))
    t = sp.Symbol('t')
    ccdf1 = 1-sp.prod([1-sp.exp(-t*p) for p in probdata])
    probdata.pop(0)
    ccdf2 = 1-sp.prod([1-sp.exp(-t*p) for p in probdata])
    f = sp.lambdify(t, ccdf1)
    avg1 = numpyintegration(f, 0, pity)
    g = sp.lambdify(t, ccdf2)
    avg2 = numpyintegration(g, pity, est)
    avgpull = avg1+avg2
    medpull = mediancompute(ccdf1, 2*int(avgpull))
    f = sp.lambdify(t, t*ccdf1)
    g = sp.lambdify(t, t*ccdf2)
    scmmt1 = 2*numpyintegration(f, 0, pity)
    scmmt2 = 2*numpyintegration(g, pity, est)
    stdev = np.sqrt(scmmt1+scmmt2 - avgpull**2)
    return (avgpull, medpull, stdev)
    

def numpyintegration(ccdf, leftlim, rightlim):
    xrange = np.arange(leftlim, rightlim+0.01, 0.01)
    yvalue = [ccdf(x) for x in xrange]
    return np.trapz(yvalue, dx = 0.01)
    
