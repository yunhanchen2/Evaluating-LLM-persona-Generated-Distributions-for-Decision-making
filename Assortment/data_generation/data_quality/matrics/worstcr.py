import numpy as np
import gurobipy as gp
from gurobipy import GRB
from itertools import combinations
from .avgcr import (
    to_vec, mask_to_subset, tuple_to_mask,
    compute_reward, compute_score_for_single_best_ranking,
    compute_reward_for_single_best_ranking,
)


__all__ = ["compute_worstcr"]

CHECKER_W_LIST = []

def check_lp(real_set, gen_set, K_list, n, eps=1e-1):
    model = gp.Model()
    model.Params.OutputFlag = 0  

    w = model.addMVar(n, lb=eps, name="w")

    # change the sushi combination to the vector
    x_real = to_vec(real_set, n)
    x_gen  = to_vec(gen_set, n)

    # real & gen: w^T x <= 1
    model.addConstr(w @ x_real <= 1)
    model.addConstr(w @ x_gen  <= 1)

    # bad K：w^T x_K >= 1 + eps 
    for K in K_list:
        xK = to_vec(K, n)
        model.addConstr(w @ xK >= 1 + eps)

    model.setObjective(0, GRB.MINIMIZE)
    model.optimize()

    if model.Status != GRB.OPTIMAL:
        return False, None
    return True, w.X

def checker(denom_mask, num_mask, denom_reward, num_reward, n, real_prefs, comp_prefs, real_rewards, comp_rewards, function_num, single_rank = False):
    real = set(mask_to_subset(denom_mask, n))
    gen  = set(mask_to_subset(num_mask, n))

    if single_rank:
        score = compute_score_for_single_best_ranking(real_prefs, function_num, n=10)
        real_comp = compute_reward_for_single_best_ranking(real, score)
        gen_comp = compute_reward_for_single_best_ranking(gen, score)
    else:
        real_comp = comp_rewards[denom_mask]
        gen_comp  = comp_rewards[num_mask]

    # Reward_comp(real) > Reward_comp(gen) 
    if real_comp > gen_comp:
        return False

    A_set = real & gen
    B_set = real - gen
    C_set = gen - real

    A = sorted(A_set)
    B = sorted(B_set)
    C = sorted(C_set)

    # min(|A|, |C|) <= 1 
    if len(A) <= 1 or len(C) <= 1:
        return True
    
    # Check S_bad (Reward_comp​(S_bad)>Reward_comp​(gen) or Rewardreal​(S_bad)>Reward_real​(real))
    S_bad = []  

    blocks = []
    if len(A_set) > 0:
        blocks.append(A_set)
    if len(B_set) > 0:
        blocks.append(B_set)
    if len(C_set) > 0:
        blocks.append(C_set)

    m = len(blocks)

    for r in range(1, m + 1):
        for idxs in combinations(range(m), r):
            K_set = set()
            for i in idxs:
                K_set |= blocks[i]  

            K_mask = tuple_to_mask(sorted(K_set))

            if single_rank:
                score = compute_score_for_single_best_ranking(real_prefs, function_num, n=10)
                K_comp = compute_reward_for_single_best_ranking(K_set, score)
            else:
                K_comp = comp_rewards[K_mask]

            K_real = real_rewards[K_mask]

            # S_bad condition
            if (K_comp > gen_comp) or (K_real > denom_reward):
                S_bad.append(sorted(list(K_set)))

    feasible, w = check_lp(real, gen, S_bad, n)

    if feasible:
        CHECKER_W_LIST.append(w)   
        return True

    return False

def compute_ratio_from_two_prefs(comp_prefs, gt_prefs, function_num, single_rank = False):
    n = len(gt_prefs[0])
    max_mask = 1 << n
    masks = list(range(1, max_mask))

    gt_rewards = np.zeros(max_mask)
    comp_rewards = np.zeros(max_mask)

    for mask in masks:
        S = mask_to_subset(mask, n)
        gt_rewards[mask] = compute_reward(S, gt_prefs, function_num)
        comp_rewards[mask] = compute_reward(S, comp_prefs, function_num)

    gt_masks_sorted_asc = sorted(masks, key=lambda m: gt_rewards[m])
    gt_reward_vec = np.array([gt_rewards[m] for m in gt_masks_sorted_asc])

    num_sets = len(gt_masks_sorted_asc)
    lower_bound = 1
    best_ratio = None

    regret_sum = 0.0

    for denom_idx in range(num_sets - 1, -1, -1):
        denom_mask = gt_masks_sorted_asc[denom_idx]
        denom_reward = gt_reward_vec[denom_idx]

        for num_idx in range(num_sets):
            num_mask = gt_masks_sorted_asc[num_idx]
            num_reward = gt_reward_vec[num_idx]

            ratio = num_reward / denom_reward

            if ratio >= lower_bound:
                continue

            if not checker(
                denom_mask, num_mask,
                denom_reward, num_reward,
                n,
                gt_prefs, comp_prefs,
                gt_rewards, comp_rewards, function_num, single_rank
            ):
                continue

            lower_bound = ratio
            best_ratio = ratio
            best_pair_indices = (denom_idx, num_idx)
            break
    return best_ratio