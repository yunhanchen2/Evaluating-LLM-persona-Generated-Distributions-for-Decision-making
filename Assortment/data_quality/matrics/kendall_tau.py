from itertools import combinations

__all__ = [
    "topk_kendall_distance",
    "compute_avg_distances",
    "compute_avg_distance_pairwise",
]

def compute_truncated_ranks(ranking, k):
    return {item: min(i + 1, k + 1) for i, item in enumerate(ranking)}

def topk_kendall_distance(r1, r2, k):
    n = len(r1)
    rank1 = compute_truncated_ranks(r1, k)
    rank2 = compute_truncated_ranks(r2, k)

    total_penalty = 0
    for x, y in combinations(range(n), 2):
        r1x, r1y = rank1[x], rank1[y]
        r2x, r2y = rank2[x], rank2[y]

        if r1x == r1y == k+1 and r2x == r2y == k+1:
            continue
        elif (r1x < r1y and r2x > r2y) or (r1x > r1y and r2x < r2y):
            total_penalty += 1
        elif (r1x == r1y == k+1 and r2x != r2y) or (r2x == r2y == k+1 and r1x != r1y):
            total_penalty += 0.5

    max_penalty = compute_max_penalty(n, k)
    return total_penalty / max_penalty if max_penalty > 0 else 0.0

def compute_max_penalty(n, k):
    if k == n:
        return n * (n - 1) / 2
    elif k <= n // 2:
        return (k / 2) * (2 * n - k - 1)
    else:
        s = n - k
        a = 2 * k - n
        return s**2 + s*(s - 1) + 2 * a * s + (a * (a - 1)) / 2


def compute_avg_distances(base_rankings, compare_rankings, k_list=10):
    total = 0.0
    count = 0
    for r1 in base_rankings:
        for r2 in compare_rankings:
            total += topk_kendall_distance(r1, r2, 10)
            count += 1
    avg_distances = total / count
    return avg_distances

def compute_avg_distance_pairwise(base_rankings, compare_rankings, k=10):
    total = 0.0
    for r1, r2 in zip(base_rankings, compare_rankings):
        total += topk_kendall_distance(r1, r2, k)
    return total / len(base_rankings)