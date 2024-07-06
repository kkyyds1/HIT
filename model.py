from itertools import product
from ortools.linear_solver import pywraplp
import pandas as pd
# import craft as data
import ipdb
import time

def define_constants(data):
    P, PL, H, T, D, F, I, N, LB, UB, hoist_interval, hoist_position, product_position, TS, SI1 = data.P, data.PL, data.H, data.T, data.D, data.F, data.I, data.N, data.LB, data.UB, data.hoist_interval, data.hoist_position, data.product_position, data.TS, data.SI1
    return P, PL, H, T, D, F, I, N, LB, UB, hoist_interval, hoist_position, product_position, TS, SI1

def define_variables(solver, constants, data):
    P, PL, H, T, D, F, I, N, LB, UB, hoist_interval, hoist_position, product_position, TS, SI1 = data.P, data.PL, data.H, data.T, data.D, data.F, data.I, data.N, data.LB, data.UB, data.hoist_interval, data.hoist_position, data.product_position, data.TS, data.SI1
    infinity = solver.infinity()
    s = {(r, i) : solver.IntVar(0.0, infinity, name=f's_{r}_{i}') for r in PL for i in range(I[r], N[r])}
    y = {(r, i, u, j) : solver.BoolVar(name=f'y_{r}_{i}_{u}_{j}') for r in PL for i in range(I[r], N[r]) for u in P for j in range(I[u], N[u])}
    Z = solver.IntVar(0.0, infinity, name='T')
    return s, y, Z

def define_constraints(solver, constants, variables, data, S):
    P, PL, H, T, D, F, I, N, LB, UB, hoist_interval, hoist_position, product_position, TS, SI1 = data.P, data.PL, data.H, data.T, data.D, data.F, data.I, data.N, data.LB, data.UB, data.hoist_interval, data.hoist_position, data.product_position, data.TS, data.SI1

    s, y, Z = variables
    M = 100000
    
    # RIUJPW = [(r, i, u, j) for r in PW for i in range(I[r], N[r]) for u in PW for j in range(I[u], N[u]) if (r, i) != (u, j)]
    RIUJP  = [(r, i, u, j) for r in P  for i in range(I[r], N[r]) for u in P  for j in range(I[u], N[u]) if (r, i) != (u, j)]
    zeta = define_zeta(H, T, D, F, LB, UB, hoist_interval, RIUJP)
    if S:
        for r in data.P:
            if data.I[r] > 0:
                for i in range(data.I[r], data.N[r]):
                    solver.Add(s[r, i] == S[r, i] - data.TS)
    for r, i, u, j in RIUJP:
        if (r, i) != (u, j) and ( (r, i) not in S or (u, j) not in S):    
            if T[r, i] == T[u, j] and j > I[u] and i > I[r]:
                solver.Add(y[r, i, u, j - 1] + y[ u, j,r, i - 1] == 1)
            solver.Add(s[u, j] - s[r, i] >= zeta[r, i, u, j, H[u, j] - H[r, i]]  - M * (1 - y[r, i, u, j]) )
            
            if (r, i) != (u, j):
                if T[r, i] == T[u, j]:
                    solver.Add(s[u, j] - s[r, i] >= D[r, i] + F[T[r, i + 1], T[u, j]] - M * (1 - y[r, i, u, j]))
                solver.Add(y[r, i, u, j] + y[u, j, r, i] == 1)
                if j > i:
                    solver.Add(y[r, i, r, j] == 1)
            
            if i > I[r]:
                solver.Add(s[r, i] - s[r, i - 1] - D[r, i - 1] >= LB[r, i])
                solver.Add(s[r, i] - s[r, i - 1] - D[r, i - 1] <= UB[r, i])
            
            solver.Add(y[r, i, u, j] + y[u, j, r, i] == 1)
    
    for r in P:
        try:
            solver.Add(Z >= s[r, N[r] - 1] + D[r, N[r] - 1])
        except:
            ipdb.set_trace()
        solver.Add(s[r, I[r]] >= F[hoist_position[H[r, I[r]]], T[r, I[r]]])
    
    solver = reschedule(solver, data, variables)

    return solver

def reschedule(solver, data, variables):
    s, y, Z = variables
    P, PL, H, T, D, F, I, N, LB, UB, hoist_interval, hoist_position, product_position, TS, SI1 = data.P, data.PL, data.H, data.T, data.D, data.F, data.I, data.N, data.LB, data.UB, data.hoist_interval, data.hoist_position, data.product_position, data.TS, data.SI1
    RIUJPL = [(r, i, u, j) for r in PL for i in range(I[r], N[r]) for u in PL for j in range(I[u], N[u]) if (r, i) != (u, j)]
    for r in PL:
        if I[r] > 0:
            solver.Add(TS + s[r, I[r]] - SI1[r] - D[r, I[r] - 1] >= LB[r, I[r]])
            solver.Add(TS + s[r, I[r]] - SI1[r] - D[r, I[r] - 1] <= UB[r, I[r]])
    
    for r, i, u, j in RIUJPL:
        if (r, i) != (u, j):
            if T[r, I[r]] == T[u, j] and j > I[u]:
                solver.Add(y[r, I[r], u, j - 1] == 1)
    return solver

def define_zeta(H, T, D, F, LB, UB, hoist_interval, RIUJ):
    zeta = {}
    for r, i, u, j in RIUJ:
        h, g = H[r, i], H[u, j]
        theta = g - h
        try:
            zeta[r, i, u, j, theta] = D[r, i] + F[T[r, i + 1], T[u, j]]
        except:
            continue

   
    return zeta

def solver(data, S):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    P, PL, H, T, D, F, I, N, LB, UB, hoist_interval, hoist_position, product_position, TS, SI1 = data.P, data.PL, data.H, data.T, data.D, data.F, data.I, data.N, data.LB, data.UB, data.hoist_interval, data.hoist_position, data.product_position, data.TS, data.SI1

    constants =  define_constants(data)
    s, y, Z = define_variables(solver, constants, data)
    define_constraints(solver, constants, (s, y, Z), data, S)
    solver.Minimize(Z)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('Z =', Z.solution_value())
    else:
        statusname = {pywraplp.Solver.FEASIBLE: 'feasible, or stopped by limit.', 
                    pywraplp.Solver.INFEASIBLE: 'proven infeasible.',
                    pywraplp.Solver.UNBOUNDED: 'proven unbounded.',
                    pywraplp.Solver.ABNORMAL: 'abnormal, i.e., error of some kind.',
                    pywraplp.Solver.MODEL_INVALID:'the model is trivially invalid (NaN coefficients, etc).',
                    pywraplp.Solver.NOT_SOLVED: 'not been solved yet.',}
        print('The problem does not have an optimal solution.')
        print(statusname.get(status))
        S = {(r, i): S[r,i] - data.TS for r, i in S if i >= data.I[r]}
        return S
    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    for r, i in s:
        data.S[r, i] = s[r, i].solution_value()
    return S
