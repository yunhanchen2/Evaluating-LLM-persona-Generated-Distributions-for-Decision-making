import numpy as np
import gurobipy as gp
from gurobipy import GRB
from itertools import combinations

from .kendall_tau import topk_kendall_distance

__all__ = ["compute_matching_cost"]


def compute_matching_cost(fake_rankings,real_rankings, k=10):
    m = len(real_rankings)
    d = len(fake_rankings)

    n = len(real_rankings[0])

    C = np.zeros((m, d))
    for i in range(m):
        for j in range(d):
            C[i, j] = topk_kendall_distance(real_rankings[i], fake_rankings[j], k)
    
    model = gp.Model("Matching_Kendall")
    model.Params.OutputFlag = 0  
    
    X = {(i, j): model.addVar(lb=0, ub=GRB.INFINITY,
                              name=f"X_{i}_{j}") for i in range(m) for j in range(d)}

    mass_per_fake = m // d  

    for j in range(d):
        model.addConstr(gp.quicksum(X[i, j] for i in range(m)) == mass_per_fake)

    for i in range(m):
        model.addConstr(gp.quicksum(X[i, j] for j in range(d)) == 1)

    model.setObjective(
        gp.quicksum(C[i, j] * X[i, j] for i in range(m) for j in range(d)),
        GRB.MINIMIZE
    )
    model.optimize()

    if model.status == GRB.OPTIMAL:
        obj_val = model.objVal
        obj_per_real = obj_val / m
        return obj_per_real
    else:
        raise RuntimeError(f"Gurobi did not find optimal solution, status = {model.status}")


