import numpy as np
import itertools

__all__ = [
    "compute_ratio_1",
    "compute_ratio_2",
    "compute_ratio_3",
    "find_best_assortment",
    "find_best_assortment_under_budget",
    "compute_reward",
]

def compute_reward(S, preferences, function_num):
    total_reward = 0
    for pref in preferences:
        for i, sushi in enumerate(pref):  
            if sushi in S:
                if function_num == 1:
                    total_reward += 10 / (i+1)
                if function_num == 2:
                    total_reward += 10 - i
                if function_num == 3:
                    total_reward += 10 -0.1*i*i

                break
    return total_reward

def compute_score_for_single_best_ranking(preferences, function_num, n=10):
    m = len(preferences)
    #create list for 10 sushi 
    scores = [0.0] * n
    
    #calculate score for each sushi 
    for ranking in preferences:
        for pos, sushi in enumerate(ranking):
            i = pos
            if function_num == 1:
                reward = 10 / (i + 1)
            if function_num == 2:
                reward = 10 - i
            if function_num == 3:
                reward = 10 - 0.1 * i * i

            scores[sushi] += reward

    scores = [s / m for s in scores]
    return scores

def compute_reward_for_single_best_ranking(S, score):
    total_reward = 0.0
    for j in S:
        total_reward += score[j]
    return total_reward

def tuple_to_mask(t):
    m = 0
    for x in t:
        m |= (1 << x)
    return m

def mask_to_subset(mask, n):
    return [i for i in range(n) if (mask >> i) & 1]

def to_vec(S, n):
    v = [0]*n
    for i in S:
        v[i] = 1
    return np.array(v, dtype=float)

def compute_costs(n_items=10, rng=None):
    if rng is None:
        rng = np.random.default_rng(0)
    return 2 + rng.random(n_items)

def find_best_assortment(preferences, k, n, score, function_num, single_rank = False):
    best_S = None
    best_reward = -1
    for S in itertools.combinations(range(n), k):
        if single_rank:
            reward = compute_reward_for_single_best_ranking(set(S),score)
        else:
            reward = compute_reward(set(S), preferences, function_num)
        if reward >= best_reward:
            best_reward = reward
            best_S = set(S)
    return best_S

def compute_ratio_1(pred_prefs,true_prefs, k, n, function_num, single_rank = False,eps=1e-15):
    score = compute_score_for_single_best_ranking(true_prefs, function_num)
    S_hat = find_best_assortment(pred_prefs, k, n, score,function_num, single_rank)
    S_star = find_best_assortment(true_prefs, k, n, score,function_num, False)
    reward_hat_true = compute_reward(S_hat, true_prefs, function_num)
    reward_star_true = compute_reward(S_star, true_prefs, function_num)

    return reward_hat_true / (reward_star_true + eps)


#files for avg2

def compute_ratio_2( method_prefs, gt_prefs, costs, k, function_num, single_rank = False, eps=1e-15):
    score = compute_score_for_single_best_ranking(gt_prefs, function_num)
    budget = float(k * np.mean(costs))

    S_method = find_best_assortment_under_budget(method_prefs, costs, budget, score, function_num, single_rank)
    S_gt = find_best_assortment_under_budget(gt_prefs, costs, budget, score, function_num, False)

    R_method = compute_reward(S_method, gt_prefs, function_num)
    R_gt = compute_reward(S_gt, gt_prefs, function_num)

    return R_method / (R_gt + eps)


#files for avg3
def compute_borda_costs(preferences, function_num, n_items=10):
    costs = compute_score_for_single_best_ranking(preferences, function_num, 10)
    return costs

def find_best_assortment_under_budget(preferences, costs, budget, score, function_num, single_rank = False):
    n = len(costs)
    best_S = set()
    best_reward = -1
    best_cost = 0

    for r in range(1, n + 1):
        for S in itertools.combinations(range(n), r):
            total_cost = sum(costs[i] for i in S)
            if total_cost <= budget:
                if single_rank:
                    reward = compute_reward_for_single_best_ranking(set(S),score)
                else:
                    reward = compute_reward(set(S), preferences, function_num)
                if (reward >= best_reward) or (reward == best_reward and total_cost > best_cost):
                    best_reward = reward
                    best_cost = total_cost
                    best_S = set(S)
    return best_S

def compute_ratio_3( method_prefs, gt_prefs, budget_mult, function_num, single_rank = False, eps=1e-12):
    score = compute_score_for_single_best_ranking(gt_prefs, function_num)
    costs = compute_borda_costs(gt_prefs, function_num)
    budget = float(budget_mult * np.mean(costs))

    S_method = find_best_assortment_under_budget(method_prefs, costs, budget, score,function_num, single_rank)
    S_gt = find_best_assortment_under_budget(gt_prefs, costs, budget, score,function_num, False)

    R_method = compute_reward(S_method, gt_prefs, function_num)
    R_gt = compute_reward(S_gt, gt_prefs, function_num)

    return R_method / (R_gt + eps)
