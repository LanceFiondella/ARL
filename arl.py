import os
import pandas
import math

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import lambertw
from scipy.optimize import differential_evolution, minimize, fmin_cobyla, fmin_slsqp

import pygmo as pg

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


class Availability:

    def __init__(self, dim, budget):
        self.dim = dim
        self.budget = budget
    def fitness(self,x):
        product = 1.
        for idx in componentIndices:
            A = avail(idx, x[componentIndices.index(idx)])
            product *= A
        ci1 = sum(x) - self.budget
        return [-product, ci1]
    
    def get_nic(self):
        return 1
    
    def get_bounds(self):
        return ([0]*self.dim,[self.budget]*self.dim)

    def get_name(self):
        return "Availability Function"

    def get_extra_info(self):
        return "\tDimension: " + str(self.dim)
    
    def gradient(self, x):
        return pg.estimate_gradient_h(lambda x: self.fitness(x), x)


prob = pg.problem(Availability(len(componentIndices), 10**7))
print(prob)

nl = pg.nlopt(solver="cobyla")
nl.xtol_rel = 1e-53
algo = pg.algorithm(pg.cstrs_self_adaptive(iters=20, algo=nl))

algo.set_verbosity(3)

pop  = pg.population(prob,100)

pop  = algo.evolve(pop)
print(pop.champion_x)
print(pop.champion_f)
