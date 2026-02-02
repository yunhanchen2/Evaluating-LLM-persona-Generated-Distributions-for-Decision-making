__all__ = ["mae_unshuffled", "mae"]

def mae_unshuffled(list_a, list_b):
    n = len(list_a)
    return sum(abs(x - y) for x, y in zip(list_a, list_b)) / n if n > 0 else float('nan')

def mae(A, B):
    if len(A) == 0 or len(B) == 0:
        return float('nan')
    return sum(abs(a - b) for a in A for b in B) / (len(A) * len(B))