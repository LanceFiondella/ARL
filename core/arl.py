import pandas as pd
import math
import numpy as np
from scipy.special import lambertw
from scipy.optimize import minimize, brute, differential_evolution
import matplotlib.pyplot as plt


from mystic.termination import NormalizedChangeOverGeneration as NCOG
from mystic.symbolic import generate_penalty, generate_conditions
from mystic.symbolic import generate_constraint, generate_solvers, simplify
from mystic.solvers import diffev

class ARL:
    def __init__(self, data, componentIndices, intermediate = 20):
        self.df = data
        self.L = data['L'][0].astype('float_')       #Lifecycle
        self.b = data['B'][0].astype('float_')       #Budget
        self.ba = data['BA'][0].astype('float_')     #Budget for availability improvement
        self.Ma = data['Ma'].astype('float_')        #A-mode failures
        self.Mb = data['Mb'].astype('float_')        #B-mode failures
        self.c0 = data['c0'].astype('float_')
        self.c1 = data['c1'].astype('float_')
        self.cv = data['cv'][0].astype('float_')
        self.mub = data['mub'].astype('float_')      #Average value of cost increment
        self.mud = data['mud'].astype('float_')      #Average B-mode failure fix effectiveness factor
        self.MTTRi = data['MTTRi'].astype('float_')  #Mean time to repair for subsystem i
        self.componentIndices = componentIndices
        self.epsilon = 0.001
        self.intermediate = intermediate
        
        self.results = []
        self.avail_ = []
        self.budget_ = []
        self.eta_ = []
        self.lc_cost = []
        self.marg_util = []
        self.comp_avail = []
    
    #MTTF : M1, M2
    def mttf(self, idx, gamma_i):
        la = 1 / float(self.Ma[idx])
        lb = 1 / float(self.Mb[idx])
        exp_part_a = ( self.c0[idx] + self.cv**2 * gamma_i)/self.mub[idx]
        pl = (( self.c0[idx] * np.exp(exp_part_a))/self.mub[idx])
        w = lambertw(pl).real
        #print('Lambert : {}'.format(w))
        b = (self.c0[idx] * self.mud[idx])/(self.mub[idx] * w)
        c = la + lb * (1 - self.mud[idx] + b)
        M = 1 / c
        return np.real(M)
    
    #Subsystem availablility: A1, A2
    def avail(self, idx, gamma_i):
        mttf = self.mttf(idx, gamma_i)
        deno = mttf + self.MTTRi[idx]
        Ai = mttf/deno
        return Ai
    
    #System availability: A = A1 * A2 *... * An
    def sys_avail(self, gammaVec):
        product = 1.0
        for i, idx in enumerate(self.componentIndices):
            #A = avail(idx,gammaVec[componentIndices.index(idx)])
            A = self.avail(idx,gammaVec[i])
            product *=A
            
        return -product
    
    #Number of replacement parts over system lifecycle. P1, P2 ...
    def rep_parts(self, idx, gamma_i):
        P = ((self.L/self.mttf(idx, gamma_i))) - self.epsilon
        return np.floor(P)
    
    #Part replacement cost of a single component over its lifecycle C1, C2...
    def lifecycle_cost(self, idx, gamma_i):
        Ci = self.c1[idx]*(1 + self.rep_parts(idx, gamma_i))
        return Ci
    
    #Total cost of maintaining a single unit over its lifecycle
    def unit_cost(self, gammaVec):
        C = 0
        for i, idx in enumerate(self.componentIndices):
            C += self.lifecycle_cost(idx, gammaVec[i])
        return C
    
    #Eta Number of systems that can be bought based on some reliability investement
    def n_gamma(self, gammaVec, *args):
        try:
            sign = args[0]
        except:
            sign = 1.0
        #print( '({} - {}) / {}'.format(self.b, sum(gammaVec), self.unit_cost(gammaVec)))
        return sign*math.floor((self.b - sum(gammaVec))/self.unit_cost(gammaVec))
    
    def constraint(self, vec):
        result = self.ba
        for x in vec:
            result -= x
        return result
    
    def maximize_n_gamma(self):
        cons = ({'type': 'ineq', 'fun': self.constraint})
        bnds = [(0, self.ba) for i in range(len(self.componentIndices))]
        print(bnds)
        #result = minimize(self.n_gamma, (self.ba/8,self.ba/8), method='SLSQP', constraints = cons, args=(-1.0,), options={'disp':True}, bounds=bnds)
        #result = brute(self.n_gamma, ((0, self.ba), (0, self.ba)), args=(-1.0,), disp=True)
        while True:
            result = differential_evolution(self.n_gamma, bnds, maxiter=10000, args=(-1.0,), tol = 0.001)
            
            if sum(result.x) < self.ba:
                break
        return result
    
    
    def mysticCompute(self):
        #for b in range(10**5, budget,  ba):
        for b in range(0, int(self.ba), int(self.ba/self.intermediate)):
            equations = "{} <= {}".format("+".join((["x{}".format(i) for i in range(len(self.componentIndices))])), b)
            #print(equations)
            cf = generate_constraint(generate_solvers(simplify(equations)))
            pf = generate_penalty(generate_conditions(equations))
            x0 = [b/len(self.componentIndices) for i in self.componentIndices]
            bounds = [(0,b) for i in self.componentIndices]
            result = diffev(self.sys_avail, x0=x0, bounds=bounds, constraints=cf, penalty=pf, npop=10, disp=True)
            #print(result)
            self.results.append(result)
            self.avail_.append(-self.sys_avail(result))
            self.budget_.append(b)
                    
            #print(self.n_gamma(result))
            self.eta_.append(self.n_gamma(result))
        return self.results
    
    
    #Functions for plotting in ARL tool
    def get_lc_costs(self, gammas):
        plotline = []
        for i, idx in enumerate(self.componentIndices):
            line = []
            for gamma in gammas:
                line.append(self.lifecycle_cost(idx, gamma))
            plotline.append(line)
        self.lc_cost = plotline
        #return self.lc_cost
    
    def get_marg_util(self, gammas):
        plotline = []
        for i, idx in enumerate(self.componentIndices):
            line = []
            gammaVec = [0 for x in range(len(self.componentIndices))]
            for gamma in gammas:
                gammaVec[i] = gamma
                line.append(self.n_gamma(gammaVec))
            plotline.append(line)
        self.marg_util = plotline
            
    def get_comp_avail(self, gammas):
        plotline = []
        for i, idx in enumerate(self.componentIndices):
            line = []
            for gamma in gammas:
                line.append(self.avail(idx, gamma))
            plotline.append(line)
        self.comp_avail = plotline
            
    def get_sys_avail(self):
        plotline = []
        for gammaVec in self.results:
            plotline.append(-self.sys_avail(gammaVec))
        self.sys_avail_list = plotline
        
    def get_fleet_size(self):
        plotline = []
        for gammaVec in self.results:
            plotline.append(self.n_gamma(gammaVec))
        self.opt_fleet_size = plotline
                

if __name__ == '__main__':
    df = pd.read_excel('../sample.xlsx')
    comp = [0, 1]
    a = ARL(df, comp)
    res = a.maximize_n_gamma()
    print(res)
    print(a.n_gamma(res.x))
    uc = a.unit_cost(res.x)
    print('Unit cost : {}'.format(uc))
    fc = uc * res.fun * -1.0
    print('Fleet cost: {}'.format(fc))
    print('Component data :')
    C = []
    P = []
    M = []
    for i, idx in enumerate(a.componentIndices):
            C.append(a.lifecycle_cost(idx, res.x[i]))
            P.append(a.rep_parts(idx, res.x[i]))
            M.append(a.mttf(idx, res.x[i]))
    print(C)
    print(P)
    print(M)
    
    
    
                        