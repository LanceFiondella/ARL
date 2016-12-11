# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:21:52 2016

@author: sbhat
"""

# -*- coding: utf-8 -*-

import math
import numpy as np

from scipy.special import lambertw
from scipy.optimize import differential_evolution

#   Budget Allocation
budget = 1e9
#   Epsilon - Small positive constant
eps = 0.001

#   Component Description
'''
    L       --> Lifecycle
    c1      --> Cost to replace subsystem
    Ma      --> Initial A-mode failure rate (In paper it is Lamba A)
    Mb      --> Initial B-mode failure rate (In paper it is Lamda B)
    c0      --> Cost of operating TAAF phase (TAAf - Test, analyze, and fix)
    mub     --> Average value of cost increment
    mud     --> Average B-mode failure fix effectiveness factor
    cv      --> Coefficient of variationof initial B-mode failures
    gamma   --> Cost to achieve desired MTBEFF (Mean time between essential function failure)
'''
#   Equation Number 11
#   MTTF as a function of reliability investment 
def mttf(comp):
    la = 1 / float(comp['Ma'])
    lb = 1 / float(comp['Mb'])
    exp_part_a = ((comp['c0'] + (math.pow(comp['cv'], 2) * comp['gamma']))/comp['mub'])
    pl = ((comp['c0'] * math.exp(exp_part_a))/comp['mub'])
    w = lambertw(pl)
    b = (comp['c0'] * comp['mud'])/(comp['mub'] * w)
    c = la + lb * (1 - comp['mud'] + b)
    M = 1 / c
    return(np.real(M))

#   Equation Number 12
#   Maximizing the fleet size through reliability investment
#   Number of replacements parts over system lifecycle.
def repParts(comp):
    #   P --> Number of subsystem i replacements over system lifecycle.
    P = ((comp['L'] / mttf(comp))) - eps
    return P

#   Equation Number 13
#   Define single component replacement costs and part replacement costs over system lifecycle. 
def cost(comp):
    #   Ci --> Cost of subsystem i over system lifecycle
    Ci = comp['c1']*(1 + repParts(comp))
    return Ci

#   Equation Number 16
#   Maximize the fleet size on a fixed budget by striking the best balance between subsystem reliability improvement investments and part replacement costs.
def n(x):
    #   Component a values
    comp_a = {'L': 20000, 'c1': 200000, 'Ma': 1000, 'Mb': 100, 'c0': 1000000, 'mub': 5000000, 'mud': 0.9, 'cv': 1, 'gamma': x[0]}
    #   Component b values
    comp_b = {'L': 20000, 'c1': 75000, 'Ma': 500, 'Mb': 200, 'c0': 8000000, 'mub': 4000000, 'mud': 0.8, 'cv': 1, 'gamma': x[1]}
    
    #   Equation Number 14
    #   Cs --> Cost of n subsystems over system lifecycle   
    Cs = cost(comp_a) + cost(comp_b)
    #print(Cs)
    return ((-budget + (x[0] + x[1])) / (cost(comp_a) + cost(comp_b)))
def execute():
    bounds = [(0, budget), (0, budget)]
    #   Differential evolution finds the global maximum of a multivariate function.
    result = differential_evolution(n, bounds, maxiter=4000)
 #   return(result.x, result.fun)
    return (result.fun)