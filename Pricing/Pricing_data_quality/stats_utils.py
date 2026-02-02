import math

__all__ = ["mean_ci_95"]

def mean_ci_95(vals):
    m = sum(vals) / len(vals)
    var = sum((x - m)**2 for x in vals) / (len(vals) - 1)
    se = math.sqrt(var) / math.sqrt(len(vals))
    return m, m - 1.96 * se, m + 1.96 * se