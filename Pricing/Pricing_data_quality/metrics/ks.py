from bisect import bisect_left

__all__ = ["ks_between_samples", "wtp_ccdf"]

def ks_between_samples(A, B):
    xs1, ys1 = wtp_ccdf(A, normalize=True)
    xs2, ys2 = wtp_ccdf(B, normalize=True)
    D, _, _, _ = ks_from_ccdfs(xs1, ys1, xs2, ys2)
    return D

def wtp_ccdf(values, normalize=True):
    vals = sorted(values)
    n = len(vals)
    if n == 0:
        return [], []
    uniq, freq, last = [], [], None
    for v in vals:
        if v != last:
            uniq.append(v)
            freq.append(1)
            last = v
        else:
            freq[-1] += 1

    ge_counts = [0] * len(freq)
    running = 0
    for i in range(len(freq) - 1, -1, -1):
        running += freq[i]
        ge_counts[i] = running

    if normalize:
        ys = [c / n for c in ge_counts]
    else:
        ys = ge_counts
    return uniq, ys

def ks_from_ccdfs(xs1, ys1, xs2, ys2):
    grid = sorted(set(xs1) | set(xs2))
    D = 0.0
    x_star = None
    s1_star = s2_star = None
    for x in grid:
        s1 = _ccdf_step_at(xs1, ys1, x)
        s2 = _ccdf_step_at(xs2, ys2, x)
        diff = abs(s1 - s2)
        if diff > D:
            D = diff
            x_star = x
            s1_star, s2_star = s1, s2
    return D, x_star, s1_star, s2_star

def _ccdf_step_at(xs, ys, x):
    if not xs:
        return 0.0
    i = bisect_left(xs, x)
    if i >= len(xs):
        return 0.0
    return ys[i]
