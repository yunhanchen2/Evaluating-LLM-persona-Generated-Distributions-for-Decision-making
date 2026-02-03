import math
import random

__all__ = [
    "load_preferences",
    "load_rankings",
    "load_scores",
    "sample_pl_ranking",
    "sample_rankings_from_scores",
]


def load_preferences(filename):
    preferences = []
    with open(filename, 'r') as f:
        for line in f:
            ranking = list(map(int, line.strip().split()))
            preferences.append(ranking)
    return preferences

def sample_pl_ranking(scores, rng):
    n = len(scores)
    remaining = list(range(n))    
    ranking = []

    while remaining:
        max_u = max(scores[i] for i in remaining)
        weights = [math.exp(scores[i] - max_u) for i in remaining]
        total_w = sum(weights)

        r = rng.random() * total_w
        cum = 0.0
        chosen_pos = 0
        for idx, w in enumerate(weights):
            cum += w
            if r <= cum:
                chosen_pos = idx
                break

        ranking.append(remaining.pop(chosen_pos))

    return ranking

def sample_rankings_from_scores(scores, m=200, seed=0):
    if isinstance(scores, dict):
        s = []
        for i in range(10):
            s.append(float(scores[i] if i in scores else scores[str(i)]))
        scores = s
    else:
        scores = [float(x) for x in scores]
        if len(scores) != 10:
            raise ValueError(f"scores must have length 10, got {len(scores)}")

    rng = random.Random(seed)
    return [sample_pl_ranking(scores, rng) for _ in range(m)]

def load_rankings(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.strip().split())) for line in f]

def load_scores(filename):
    with open(filename, 'r') as f:
        return [list(map(float, line.strip().split())) for line in f]