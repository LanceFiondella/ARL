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


import pygmo as pg

budget = 10**9

eps = 0.0001

data = pandas.read_excel(os.getcwd() + '/sample.xlsx')

# componentIndices = [int(i) for i in str.split(input('Enter component indices:'))]


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
        return ([0]*self.dim,[budget]*self.dim)

    def get_name(self):
        return "Availability Function"

    def get_extra_info(self):
        return "\tDimension: " + str(self.dim)
    
    def gradient(self, x):
        return pg.estimate_gradient_h(lambda x: self.fitness(x), x)


# import time
# times = []
# bud = []
# for b in range(10**5, 10**9, 3*10**8):
#     for i in range(2,12):
#         componentIndices = [j for j in range(i)]
#         prob = pg.problem(Availability(len(componentIndices), b))
#         print(prob)
#         # nl = pg.nlopt(solver='de')
#         # nl.xtol_abs = 1e-3
#         algo = pg.algorithm(pg.cstrs_self_adaptive(iters=10, algo=pg.de(10)))

#         algo.set_verbosity(3)

#         pop  = pg.population(prob,10)
#         start_time = time.time()
#         pop  = algo.evolve(pop)
#         end_time = time.time()
#         time_taken = start_time - end_time
#         times.append(-time_taken)
#         print(pop.champion_x)
#         print(pop.champion_f)
#     bud.append(times)
#     times=[]

# print(times)
# print(bud)

# for i,b in enumerate(range(10**5, 10**9, 3*10**8)):
#     plt.plot(range(2,12), bud[i], label='budget {}'.format(budget))

def compute():
    for b in range(10**5, 10**9, 10**7):
        prob = pg.problem(Availability(len(componentIndices), b))
        nl = pg.nlopt(solver='cobyla')
        nl.xtol_abs = 1e-12
        # algo = pg.algorithm(pg.cstrs_self_adaptive(iters=10, algo=nl))
        algo = pg.algorithm(nl)
        # algo = pg.algorithm(pg.cstrs_self_adaptive(iters=10, algo=pg.de(gen=3, variant=4)))

        algo.set_verbosity(3)
        pop  = pg.population(prob,5)
        pop  = algo.evolve(pop)
        avail_.append(-pop.champion_f[0])
        budget_.append(b)
        eta_.append(eta(pop.champion_x))

def mysticCompute():
    for b in range(10**5, budget, 10**7):
        equations = "{} <= {}".format("+".join((["x{}".format(i) for i in range(len(componentIndices))])), b)
        cf = generate_constraint(generate_solvers(simplify(equations)))
        pf = generate_penalty(generate_conditions(equations))
        x0 = [b/len(componentIndices) for i in componentIndices]
        bounds = [(0,b) for i in componentIndices]
        result = diffev(sys, x0=x0, bounds=bounds, constraints=cf, penalty=pf, npop=10, disp=True)
        print(result)
        avail_.append(-sys(result))
        budget_.append(b)

        print(eta(result))
        eta_.append(eta(result))
# plt.xlabel("# of components")
# plt.ylabel('time taken in seconds')
# plt.show()
