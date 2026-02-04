import os
from .avgcr import total_profit_from_wtp

__all__ = ["worst_ratios", "candidate_costs_from_wtp", "optimal_price_from_wtp_with_tie", "compute_ratios_single",]


def worst_ratios(A, B, cost_max):
    cost1 = candidate_costs_from_wtp(A, cost_max)
    cost2 = candidate_costs_from_wtp(B, cost_max)
    # merge possible costs
    candidate_costs = sorted(set(cost1) | set(cost2))

    # init
    worst_ratio = float('inf')
    worst_c = None

    # go over all possible cost
    for c in candidate_costs: 
        r = compute_ratios_single(A, B, c)
        if r < worst_ratio:
            worst_ratio = r
            worst_c = c

    if worst_ratio == float('inf'):
        return float('nan')   
    return worst_ratio

def candidate_costs_from_wtp(A, cost_max):
    A = sorted(A)
    n = len(A)
    prices = sorted(set(A))

    # D(p): used to calculate the ccdf of a wtp
    def D(p):
        return sum(1 for x in A if x >= p)

    #finding possible costs
    costs = []

    if cost_max==1:
        cost_max_value = -12
    elif cost_max==2:
        cost_max_value = 22

    # double for loop to solve the function of (p-c)D(p)=(q-c)D(q)
    for i, p in enumerate(prices):
        for q in prices[i+1:]:
            Dp, Dq = D(p), D(q)
            # delete the extreme case, otherwise, denom will be 0
            if Dp == Dq:
                continue
            c = (p*Dp - q*Dq) / (Dp - Dq)

            # cost can't smaller than 0
            if c < -44:
                continue
            # cost can't bigger than 66 (<=)
            if c > cost_max_value:
                continue
            # I will explain it here: 
            if c <= min(p, q):
                costs.append(c)

    return costs

def optimal_price_from_wtp_with_tie(real_list, wtp_list, cost):
    uniq = sorted(set(wtp_list))
    candidates = [p for p in uniq if p >= cost]

    # all the wtp is smaller than cost
    if not candidates:
        return cost  

    #init
    n = len(wtp_list)
    best_p, best_profit = candidates[0], -1.0
    for p in candidates:
        dem = sum(1 for x in wtp_list if x >= p) / n
        prof = (p - cost) * dem
        if prof > best_profit:
            best_profit = prof
            best_p = p
        #break the tie
        elif prof == best_profit:
            if total_profit_from_wtp(real_list, p, cost) < total_profit_from_wtp(real_list, best_p, cost):
                best_profit = prof
                best_p = p

    return max(best_p, cost)

def compute_ratios_single(real_wtp, source_wtp, cost):
    p_real = optimal_price_from_wtp_with_tie(real_wtp, real_wtp, cost)
    denom = total_profit_from_wtp(real_wtp, p_real, cost)
    if denom==0:
        return float('inf')

    p_src = optimal_price_from_wtp_with_tie(real_wtp, source_wtp, cost)
    num = total_profit_from_wtp(real_wtp, p_src, cost)
    if num == 0:
        return float('inf')

    ratio = num / denom
    return ratio