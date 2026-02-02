__all__ = ["compute_ratios", "optimal_price_from_wtp", "total_profit_from_wtp"]

def compute_ratios(real_wtp, source_wtp, cost_range_index):
    ratios = []

    if cost_range_index==1:
        cost_max_v=-12
    elif cost_range_index==2:
        cost_max_v=22
    elif cost_range_index==3:
        cost_max_v=56

    for cost in range(-44,cost_max_v):

        # oracle price on real
        p_real = optimal_price_from_wtp(real_wtp, cost)
        denom = total_profit_from_wtp(real_wtp, p_real, cost)

        if denom <= 0:
            continue 

        p_src = optimal_price_from_wtp(source_wtp, cost)
        num = total_profit_from_wtp(real_wtp, p_src, cost)

        ratios.append(num / denom)

    return sum(ratios) / len(ratios)

def optimal_price_from_wtp(wtp_list, cost):
    uniq = sorted(set(wtp_list))
    candidates = [p for p in uniq if p >= cost]
    if not candidates:
        return cost  

    n = len(wtp_list)
    best_p, best_profit = candidates[0], -1.0
    for p in candidates:
        dem = sum(1 for x in wtp_list if x >= p) / n
        prof = (p - cost) * dem
        if prof > best_profit:
            best_profit = prof
            best_p = p
    return max(best_p, cost)

def total_profit_from_wtp(wtp_list, price, cost):
    n = len(wtp_list)
    if n == 0:
        return 0.0
    demand_frac = sum(1 for x in wtp_list if x >= price) / n
    return (price - cost) * demand_frac 
