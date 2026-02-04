import numpy as np
from scipy.optimize import linprog

__all__ = ["compute_matching_cost"]

def compute_matching_cost(real_vals, fake_vals, k=10):
    m = len(real_vals)
    d = len(fake_vals)

    C = np.zeros((m, d))
    for i in range(m):
        for j in range(d):
            C[i, j] = abs(float(real_vals[i]) - float(fake_vals[j]))

    mass_per_fake = m // d
    if mass_per_fake * d != m:
        raise ValueError(f"Infeasible with current constraints: m={m} not divisible by d={d}.") 

    def idx(i, j):
        return i * d + j

    nvars = m * d

    A_eq = []
    b_eq = []

    for j in range(d):
        row = np.zeros(nvars, dtype=float)
        for i in range(m):
            row[idx(i, j)] = 1.0
        A_eq.append(row)
        b_eq.append(float(mass_per_fake))

    for i in range(m):
        row = np.zeros(nvars, dtype=float)
        for j in range(d):
            row[idx(i, j)] = 1.0
        A_eq.append(row)
        b_eq.append(1.0)

    A_eq = np.vstack(A_eq)
    b_eq = np.array(b_eq, dtype=float)

    c = C.reshape(-1) 

    bounds = [(0.0, None)] * nvars

    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if res.status == 0:  
        return float(res.fun) / m
    else:
        raise RuntimeError(f"HiGHS linprog failed: status={res.status}, message={res.message}")