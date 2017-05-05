import os
import pandas
import math

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import lambertw
from scipy.optimize import differential_evolution, minimize, fmin_cobyla, fmin_slsqp


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


def callBack(x):
    print(x)


def compute():
    for b in range(10**5, budget, 10**6):
        cons = lambda x: -(x.sum() -b)
        constraints = [{'type':'ineq', 'fun':cons}]
        bounds = np.array([(0,b) for i in componentIndices])
        x0 = np.array([b/len(componentIndices) for i in componentIndices])
        resultAva = minimize(sys, x0=x0, bounds=bounds, constraints=constraints, method="SLSQP")
        print(resultAva)


# compute()



# def sys2(g):
#     product = 1
#     print(g.value)
#     for idx in componentIndices:
#         A = avail(idx,g.value[componentIndices.index(idx)])
#         product *= A
#     return -product

# def compute2():
#     x = variable(len(componentIndices), 'x')
#     # x.value = 1
#     constraints1 = (x >= 0)
#     constraints2 = (sum(x) <= 10**9)
#     problem = op(dot(x, x), [constraints1, constraints2])
#     result = problem.solve()
#     print(result)


# def compute3():
#     x = Variable(len(componentIndices))
#     objective = Minimize(geo_mean(avail(x))



# compute2()


# b1 = np.linspace(70000000,100000000,10)
# b2 = b1

# grid = np.meshgrid(b1, b2)
# def z(x,y):
#     return x*(1-y)
# # data = z(grid[0], grid[1])
# data = sys(grid)

# fig3d = plt.figure()
# ax3d = Axes3D(fig3d)
# ax3d.plot_wireframe(grid[0], grid[1], data)
# budg = 1000
# iterbudget = budg
# f = (0, budg)
# bounds = [f]*len(componentIndices)
# x0 = [10,]*len(componentIndices)
# result = minimize(sys, x0, method="TNC", bounds=bounds, constraints=constraints)
# print(result)
# print(eta(result.x))
# fig3d.show()
# import time
# time.sleep(10)

# from mystic.solvers import DifferentialEvolutionSolver2
from mystic.termination import NormalizedChangeOverGeneration as NCOG
from mystic.symbolic import generate_penalty, generate_conditions
from mystic.symbolic import generate_constraint, generate_solvers, simplify
from mystic.solvers import diffev

def mysticCompute():
    for b in range(10**5, budget, 10**7):
        equations = "{} <= {}".format("+".join((["x{}".format(i) for i in range(len(componentIndices))])), b)
        # print(equations)
        # def cons(x):
        #     x[0]+x[1] - b <= 0
        #     return x

        cf = generate_constraint(generate_solvers(simplify(equations)))
        pf = generate_penalty(generate_conditions(equations))

        x0 = [b/len(componentIndices) for i in componentIndices]
        bounds = [(0,b) for i in componentIndices]
        result = diffev(sys, x0=x0, bounds=bounds, constraints=cf, penalty=pf, npop=40, disp=True)
        # solver.SetInitialPoints(x0)
        # solver.SetStrictRanges(min=[0,]*len(componentIndices), max=[b]*len(componentIndices))
        # solver.SetConstraints(cons)
        # solver.Solve(sys, NCOG(tolerance=1e-14), disp=1)
        # solver.enable_signal_handler()

        print(result)
        print(eta(result))
mysticCompute()
