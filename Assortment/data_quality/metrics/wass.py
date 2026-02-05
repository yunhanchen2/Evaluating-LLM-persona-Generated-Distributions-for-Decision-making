import numpy as np
from scipy.optimize import linprog
from itertools import combinations
from scipy.sparse import coo_matrix

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
    
    
    mass_per_fake = m // d
    if mass_per_fake * d != m:
        raise ValueError(f"Infeasible with current constraints: m={m} not divisible by d={d}.")

    nvars = m * d

    nrows = d + m

    rows = []
    cols = []
    data = []

    def idx(i, j):
        return i * d + j

    for j in range(d):
        for i in range(m):
            rows.append(j)
            cols.append(idx(i, j))
            data.append(1.0)

    for i in range(m):
        r = d + i
        for j in range(d):
            rows.append(r)
            cols.append(idx(i, j))
            data.append(1.0)

    A_eq = coo_matrix((data, (rows, cols)), shape=(nrows, nvars))
    b_eq = np.concatenate([np.full(d, float(mass_per_fake)), np.ones(m)])

    c = C.reshape(-1)
    bounds = [(0.0, None)] * nvars

    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if res.status == 0:
        return float(res.fun) / m
    raise RuntimeError(f"HiGHS linprog failed: status={res.status}, message={res.message}")
