import numpy as np
import gurobipy as gp
from gurobipy import GRB

__all__ = ["compute_matching_cost"]

def compute_matching_cost(real_vals, fake_vals, k=10):
    m = len(real_vals)
    d = len(fake_vals)

    C = np.zeros((m, d))
    for i in range(m):
        for j in range(d):
            C[i, j] = abs(float(real_vals[i]) - float(fake_vals[j]))
    
    model = gp.Model("Matching_val")
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
        return model.objVal / m
    else:
        raise RuntimeError(f"Gurobi status = {model.status}")