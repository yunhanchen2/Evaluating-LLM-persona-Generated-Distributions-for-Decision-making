from io_utils import *
from stats_utils import *
from metrics import *  
import os
import csv, random, numpy as np, matplotlib.pyplot as plt
from metrics.avgcr import compute_costs


os.environ["GRB_LICENSE_FILE"] = "gurobi.lic"


COST_POOL_SIZE = 2000
rng_cost = np.random.default_rng(12345)
COST_POOL = [compute_costs(n_items=10, rng=rng_cost) for _ in range(COST_POOL_SIZE)]
cost_ptr = 0

def function_caller (A,B,method,k,n,function_num, avgcr_type,single_rank=False):
    global cost_ptr
    if method==1:
        return compute_avg_distances(B, A)

    if method==2:
        return compute_matching_cost(A,B)

    elif method==3:
        if avgcr_type==1:
            return compute_ratio_1(A,B,k,n,function_num, single_rank)
        elif avgcr_type==2:
            if single_rank:
                tmp = []
                for _ in range(2000):
                    costs = COST_POOL[cost_ptr] 
                    cost_ptr += 1
                    tmp.append(compute_ratio_2( A, B, costs, k, function_num, single_rank))
                return np.mean(tmp)
            else:
                tmp = []
                for scen in range(100):
                    costs = COST_POOL[cost_ptr] 
                    cost_ptr += 1
                    tmp.append(compute_ratio_2( A, B, costs, k, function_num, single_rank))
                return np.mean(tmp)
        elif avgcr_type==3:
            return compute_ratio_3(A,B,k,function_num,single_rank)

    elif method==4:
        return compute_ratio_from_two_prefs(A, B, function_num, single_rank)

def get_folder_path(model):
    model_folder = {1: "gpt-4o", 2: "gpt-5-mini", 3: "gemini", 4: "mistral"}[model]
    return os.path.join("src", model_folder)


def main():
    global cost_ptr
    base_file = os.path.join("src", "baseline", "Ground Truth.txt")      
    n = 10     

    print("Select model: 1-GPT-4o, 2-GPT-5-mini, 3-Gemini, 4-Mistral")
    model = int(input("Enter 1–4: "))   

    print("Select reward function: 1-10/i, 2-10-(i-1), 3-10-0.1*(i-1)*(i-1), where i is from 1-10")
    function_num = int(input("Enter 1-3: ")) 

    print("Select metric: 1-Kendall-tau, 2-Wasserstein, 3-AverageCR, 4-WorstCR")
    method = int(input("Enter a number (1–4): "))
    
    avgcr_type = 0
    if method == 3:
        print("Select AvgCR cost type: 1-Unit cost, 2-Random cost, 3-Hard cost")
        avgcr_type = int(input("Enter 1–3: "))

    if method==3:
        k_values = list(range(2, 7))
    else:
        k_values = [0] # means only one loop below

    mean_ratio = {}
    ci_low_ratio = {}
    ci_high_ratio = {}

    folder= get_folder_path(model)

    base_all = load_preferences(base_file)[:600]

    rng = random.Random(0)

    model_log_files = { "Background Steering for Sampling Method": os.path.join(folder, "no_steering_1.txt"),
    "Persona Steering for Sampling Method": os.path.join(folder, "persona_steering_1.txt"),}

    for label, filepath in model_log_files.items():
        comp_all = load_preferences(filepath)[:600]

        mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []

        for k in k_values:
            cost_ptr = 0
            vals = []
            for _ in range(20):
                base_sample = rng.sample(base_all, 600)
                comp_sample = rng.sample(comp_all, 200)
                vals.append(function_caller(comp_sample, base_sample, method,k,n,function_num, avgcr_type))

            m, lo, hi = mean_ci_95(vals)
            mean_ratio[label].append(m)
            ci_low_ratio[label].append(lo)
            ci_high_ratio[label].append(hi)

            if k==0:
                print(label, f"mean=", m, "CI=(", lo, ",", hi, ")")
            else:
                print(label, f"B={k}", "mean=", m, "CI=(", lo, ",", hi, ")")

    model_log_files2 = {"Few-shot Steering for Sampling Method": os.path.join(folder, "few_shot_steering_1.txt"),
    "Persona + Few-shot Steering for Sampling Method": os.path.join(folder, "persona_few_shot_steering_1.txt"),}

    for label, filepath in model_log_files2.items():
        comp_all = load_rankings(filepath)

        mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []

        for k in k_values:
            cost_ptr = 0
            vals = []
            for seg in range(5):
                block = comp_all[seg*300:(seg+1)*300]
                for _ in range(4):
                    base_sample = rng.sample(base_all, 600)
                    comp_sample = rng.sample(block, 200)
                    vals.append(function_caller(comp_sample, base_sample,  method,k,n,function_num, avgcr_type))


            m, lo, hi = mean_ci_95(vals)
            mean_ratio[label].append(m)
            ci_low_ratio[label].append(lo)
            ci_high_ratio[label].append(hi)

            if k==0:
                print(label, f"mean=", m, "CI=(", lo, ",", hi, ")")
            else:
                print(label, f"B={k}", "mean=", m, "CI=(", lo, ",", hi, ")")

    sequence_files = {"Background Steering for Batch Method": os.path.join(folder, "no_steering_2.txt"),
    "Few-shot Steering for Batch Method": os.path.join(folder, "few_shot_steering_2.txt"),}

    for label, filepath in sequence_files.items():
        comp_all = load_rankings(filepath)

        mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []

        for k in k_values:
            cost_ptr = 0
            vals = []
            for j in range(20):
                block = comp_all[j*30:(j+1)*30]
                base_sample = rng.sample(base_all, 600)
                vals.append(function_caller(block, base_sample,  method,k,n,function_num, avgcr_type))

            m, lo, hi = mean_ci_95(vals)
            mean_ratio[label].append(m)
            ci_low_ratio[label].append(lo)
            ci_high_ratio[label].append(hi)

            if k==0:
                print(label, f"mean=", m, "CI=(", lo, ",", hi, ")")
            else:
                print(label, f"B={k}", "mean=", m, "CI=(", lo, ",", hi, ")")

    knowledge_files = {"Background Steering for Description Method": os.path.join(folder, "no_steering_3.txt"),
    "Few-shot Steering for Description Method": os.path.join(folder, "few_shot_steering_3.txt"),}

    for label, filepath in knowledge_files.items():
        score_list = load_scores(filepath)

        mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []

        for k in k_values:
            cost_ptr = 0
            vals = []
            for j, scores in enumerate(score_list[:20]):
                comp_sample = sample_rankings_from_scores(scores, m=200, seed=100 + j)
                base_sample = rng.sample(base_all, 600)
                vals.append(function_caller(comp_sample, base_sample,  method,k,n,function_num, avgcr_type))

            m, lo, hi = mean_ci_95(vals)
            mean_ratio[label].append(m)
            ci_low_ratio[label].append(lo)
            ci_high_ratio[label].append(hi)

            if k==0:
                print(label, f"mean=", m, "CI=(", lo, ",", hi, ")")
            else:
                print(label, f"B={k}", "mean=", m, "CI=(", lo, ",", hi, ")")

    baseline_files = {"Uniform baseline": os.path.join("src", "baseline", "random.txt")}

    for label, filepath in baseline_files.items():
        comp_all = load_rankings(filepath)[:600]

        mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []

        for k in k_values:
            cost_ptr = 0
            vals = []
            for _ in range(20):
                base_sample = rng.sample(base_all, 600)
                comp_sample = rng.sample(comp_all, 200)
                vals.append(function_caller(comp_sample, base_sample, method,k,n,function_num, avgcr_type))

            m, lo, hi = mean_ci_95(vals)
            mean_ratio[label].append(m)
            ci_low_ratio[label].append(lo)
            ci_high_ratio[label].append(hi)

            if k==0:
                print(label, f"mean=", m, "CI=(", lo, ",", hi, ")")
            else:
                print(label, f"B={k}", "mean=", m, "CI=(", lo, ",", hi, ")")

    baseline_files2 = {"Ground Truth": os.path.join("src", "baseline", "5000_a.txt")}

    sizes = [5, 10, 15, 20, 30, 50]

    for base_label, filepath in baseline_files2.items():
        gt_all = load_rankings(filepath)[600:]

        for s in sizes:
            label = f"Few-shot empirical baseline (k={s})"

            mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []

            for k in k_values:
                cost_ptr = 0
                vals = []
                for _ in range(20):
                    base_sample = rng.sample(base_all, 600)
                    comp_sample = rng.sample(gt_all, s)
                    vals.append(function_caller(comp_sample, base_sample,  method,k,n,function_num, avgcr_type))

                m, lo, hi = mean_ci_95(vals)
                mean_ratio[label].append(m)
                ci_low_ratio[label].append(lo)
                ci_high_ratio[label].append(hi)

                if k==0:
                    print(label, f"mean=", m, "CI=(", lo, ",", hi, ")")
                else:
                    print(label, f"B={k}", "mean=", m, "CI=(", lo, ",", hi, ")")


    if method == 3 or method == 4:
        label = "Single Ranking Baseline"
        single_rank = True

        mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []

        for k in k_values:
            cost_ptr = 0
            base_sample = rng.sample(base_all, 600)
            comp_sample = [single_rank]

            ratio = function_caller(base_sample, base_sample, method,k,n,function_num, avgcr_type, single_rank)

            mean_ratio[label].append(ratio)
            ci_low_ratio[label].append(ratio)
            ci_high_ratio[label].append(ratio)
            if k==0:
                print(label, f"mean=", ratio, "CI=(", ratio, ",", ratio, ")")
            else:
                print(label, f"B={k}", "mean=", ratio, "CI=(", ratio, ",", ratio, ")")

    if method ==1:
        shuffled_files = {"Unshuffled Persona Steering for Sampling Method": os.path.join(folder, "persona_steering_1.txt"),}

        for label, filepath in shuffled_files.items():
            mean_ratio[label], ci_low_ratio[label], ci_high_ratio[label] = [], [], []
            comp_pool = load_rankings(filepath)

            base_fixed = base_all
            comp_fixed = rng.sample(comp_pool, 600)

            v = compute_avg_distance_pairwise(base_fixed, comp_fixed, 10)

            mean_ratio[label] = v
            ci_low_ratio[label] = v
            ci_high_ratio[label] = v

            print(label, "value =", v)

    


if __name__ == "__main__":
    main()
    

