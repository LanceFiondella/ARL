import os
import pandas
import math

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import lambertw
from scipy.optimize import differential_evolution, minimize, fmin_cobyla, fmin_slsqp

from mystic.termination import NormalizedChangeOverGeneration as NCOG
from mystic.symbolic import generate_penalty, generate_conditions
from mystic.symbolic import generate_constraint, generate_solvers, simplify
from mystic.solvers import diffev

budget = 10**9

eps = 0.0001

data = pandas.read_excel(os.getcwd() + '/sample.xlsx')


componentIndices = [int(i) for i in str.split(input('Enter component indices:'))]


def mttf(idx,gamma):
    la = 1 / float(data['Ma'][idx])
    lb = 1 / float(data['Mb'][idx])
   
    exp_part_a = (data['c0'][idx] + data['cv'][idx]**2 * gamma)/data['mub'][idx]
    pl = ((data['c0'][idx] * np.exp(exp_part_a))/data['mub'][idx])
    w = lambertw(pl)
    b = (data['c0'][idx] * data['mud'][idx])/(data['mub'][idx] * w)
    c = la + lb * (1 - data['mud'][idx] + b)
    M = 1 / c
    return np.real(M)


def repParts(idx, gamma):
    P = ((data['L'][idx]/mttf(idx, gamma))) - eps
    return np.floor(P)


def cost(idx,gamma):
    Ci = data['c1'][idx]*(1 + repParts(idx, gamma))
    return Ci


def avail(idx, gamma):
    deno = mttf(idx, gamma) + data['MTTRi'][idx] # calling mttf twice BAD
    Ai = mttf(idx, gamma)/deno
    return Ai


def sys(gammaVec):
    product = 1.
    for idx in componentIndices:
        A = avail(idx,gammaVec[componentIndices.index(idx)])
        product *=A
    return -product


def unitCost(gammaData):
    tmp = []
    for idx in componentIndices:
        Cs = cost(idx,gammaData[componentIndices.index(idx)])
        tmp.append(Cs)
    return sum(tmp)


def eta(gammaVec):
    nGamma = (budget - sum(gammaVec))/unitCost(gammaVec)
    return nGamma

avail_ = []
budget_  = []
eta_ = []


def mysticCompute():
    for b in range(10**5, budget, 10**5):
        equations = "{} <= {}".format("+".join((["x{}".format(i) for i in range(len(componentIndices))])), b)
        cf = generate_constraint(generate_solvers(simplify(equations)))
        pf = generate_penalty(generate_conditions(equations))
        x0 = [b/len(componentIndices) for i in componentIndices]
        bounds = [(0,b) for i in componentIndices]
        result = diffev(sys, x0=x0, bounds=bounds, constraints=cf, penalty=pf, npop=40, disp=True)
        print(result)
        avail_.append(-sys(result))
        budget_.append(b)

        print(eta(result))
        eta_.append(eta(result))


mysticCompute()
plt.plot( budget_, avail_)
plt.show()
plt.plot(budget_, eta_ )
plt.show()
plt.plot(eta_, avail_)
plt.show()
