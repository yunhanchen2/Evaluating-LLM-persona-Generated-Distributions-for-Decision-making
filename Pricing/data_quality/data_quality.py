from io_utils import *
from stats_utils import *
from matrics import *
import os
import csv, random, numpy as np, matplotlib.pyplot as plt

os.environ["GRB_LICENSE_FILE"] = "gurobi.lic"


def function_caller(A, B, k, cost_range_index=0, cost_max=0):
    if k==1:
        return mae (A, B)
    elif k == 2:
        return ks_between_samples(A, B)
    elif k == 3:
        return compute_matching_cost(A, B)
    elif k == 4:
        return compute_ratios(A, B, cost_range_index)
    elif k == 5:
        return worst_ratios(A, B, cost_max)
    else:
        raise ValueError(f"Unknown k={k}")

def get_folder_path(f, model):
    model_folder = {1: "gpt-4o", 2: "gpt-5-mini", 3: "gemini", 4: "mistral"}[model]
    data_folder  = {1: "awards", 2: "origin"}[f]
    return os.path.join("src", model_folder, data_folder)


def main():
    print("Select model: 1-GPT-4o, 2-GPT-5-mini, 3-Gemini, 4-Mistral")
    model = int(input("Enter 1–4: "))

    print("Select dataset: 1-Awards, 2-Origin")
    f = int(input("Enter 1 or 2: "))

    print("Select metric: 1-MAE, 2-KS, 3-Wasserstein, 4-AverageCR, 5-WorstCR")
    k = int(input("Enter a number (1–5): "))

    cost_range_index=0
    cost_max=0

    if k==4:
        print("Select cost range: 1-(0–32), 2-(0–66), 3-(0–100)")
        cost_range_index = int(input("Enter 1–3: "))
    elif k==5:
        print("Select cost max value: 1-32, 2-66")
        cost_max = int(input("Enter 1–2: "))


    products = ["Bohol", "Davao", "ImprovedBicol"]
    rng = random.Random(0)

    mean_curves = {}
    ci_low_curves = {}
    ci_high_curves = {}

    real_file = os.path.join("src", "baseline", "award.txt" if f == 1 else "origin.txt")

    real_products = load_products(real_file, n_products=3)

    base_all = {
        "Bohol": real_products[0][:100],
        "Davao": real_products[1][:100],
        "ImprovedBicol": real_products[2][:100],
    }

    folder=get_folder_path(f,model)
    
    model_log_files = { "Background Steering for Sampling Method": os.path.join(folder, "no_steering_1.txt"),
    "Persona Steering for Sampling Method": os.path.join(folder, "persona_steering_1.txt"),}

    for label, filepath in model_log_files.items():
        mean_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_low_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_high_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}

        comp_all_list = load_products(filepath, n_products=3)
        comp_all_list = [lst[:100] for lst in comp_all_list]

        comp_all = {
            "Bohol": comp_all_list[0],
            "Davao": comp_all_list[1],
            "ImprovedBicol": comp_all_list[2],
        }

        vals = {p: [] for p in products}

        for _ in range(20):
            for p in products:
                base_sample = base_all[p] 
                comp_sample = rng.sample(comp_all[p], 50)
                vals[p].append(function_caller(base_sample, comp_sample, k, cost_range_index, cost_max))  

        for p in products:
            m, lo, hi = mean_ci_95(vals[p])
            mean_curves[label][p] = m
            ci_low_curves[label][p] = lo
            ci_high_curves[label][p] = hi

        print(label, "mean=", mean_curves[label], "CI=(", ci_low_curves[label], ",", ci_high_curves[label], ")")

    model_log_files2 = {"Few-shot Steering for Sampling Method": os.path.join(folder, "few_shot_steering_1.txt"),
    "Persona + Few-shot Steering for Sampling Method": os.path.join(folder, "persona_few_shot_steering_1.txt"),}

    for label, filepath in model_log_files2.items():
        mean_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_low_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_high_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}

        comp_all_list = load_products(filepath, n_products=3)
        comp_all_list = [lst[:500] for lst in comp_all_list]   

        comp_all = {
            "Bohol": comp_all_list[0],
            "Davao": comp_all_list[1],
            "ImprovedBicol": comp_all_list[2],
        }

        vals = {p: [] for p in products}

        for seg in range(5):                        
             for p in products:
                block = comp_all[p][seg*100:(seg+1)*100] 

                for _ in range(4):
                    base_sample = base_all[p] 
                    comp_sample = rng.sample(block, 50) 
                    vals[p].append(function_caller(base_sample, comp_sample, k, cost_range_index, cost_max))

        for p in products:
            m, lo, hi = mean_ci_95(vals[p])
            mean_curves[label][p] = m
            ci_low_curves[label][p] = lo
            ci_high_curves[label][p] = hi

        print(label, "mean=", mean_curves[label], "CI=(", ci_low_curves[label], ",", ci_high_curves[label], ")")

    sequence_files = {"Background Steering for Batch Method": os.path.join(folder, "no_steering_2.txt"),
    "Few-shot Steering for Batch Method": os.path.join(folder, "few_shot_steering_2.txt"),}

    for label, filepath in sequence_files.items():
        print("[Batch]", label, {p: len(comp_all[p]) for p in products})
        mean_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_low_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_high_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}

        comp_all_list = load_products(filepath, n_products=3)
        comp_all = {
            "Bohol": comp_all_list[0],
            "Davao": comp_all_list[1],
            "ImprovedBicol": comp_all_list[2],
        }

        vals = {p: [] for p in products}

        for j in range(20):
            for p in products:
                block = comp_all[p][j*25:j*25 + 25]

                base_sample = rng.sample(base_all[p], len(block))
                vals[p].append(function_caller(base_sample, block, k, cost_range_index, cost_max)) 

        for p in products:
            m, lo, hi = mean_ci_95(vals[p])
            mean_curves[label][p] = m
            ci_low_curves[label][p] = lo
            ci_high_curves[label][p] = hi

        print(label, "mean=", mean_curves[label], "CI=(", ci_low_curves[label], ",", ci_high_curves[label], ")")

    knowledge_files = {"Background Steering for Description Method": os.path.join(folder, "no_steering_3.txt"),
    "Few-shot Steering for Description Method": os.path.join(folder, "few_shot_steering_3.txt"),}
 
    for label, filepath in knowledge_files.items():
        mean_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_low_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_high_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}

        dist_lines = read_lines(filepath)

        vals = {p: [] for p in products}

        for j, line in enumerate(dist_lines[:20]):  
            expanded = line_to_expanded_structure(line, n=50)  

            for p in products:
                comp_sample = expanded[p]                             
                base_sample = rng.sample(base_all[p], len(comp_sample))
                vals[p].append(function_caller(base_sample, comp_sample, k, cost_range_index, cost_max))

        for p in products:
            m, lo, hi = mean_ci_95(vals[p])
            mean_curves[label][p] = m
            ci_low_curves[label][p] = lo
            ci_high_curves[label][p] = hi

        print(label, "mean=", mean_curves[label], "CI=(", ci_low_curves[label], ",", ci_high_curves[label], ")")

    baseline_files = {"Uniform baseline": os.path.join("src", "baseline", "random.txt")}

    for label, filepath in baseline_files.items():
        mean_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_low_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
        ci_high_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}

        comp_all_list = load_products(filepath, n_products=3)
        comp_all = {
            "Bohol": comp_all_list[0],
            "Davao": comp_all_list[1],
            "ImprovedBicol": comp_all_list[2],
        }

        vals = {p: [] for p in products}

        for _ in range(20):
            for p in products:
                base_sample = base_all[p]
                comp_sample = rng.sample(comp_all[p], 50)  
                vals[p].append(function_caller(base_sample, comp_sample, k, cost_range_index, cost_max))

        for p in products:
            m, lo, hi = mean_ci_95(vals[p])
            mean_curves[label][p] = m
            ci_low_curves[label][p] = lo
            ci_high_curves[label][p] = hi

        print(label, "mean=", mean_curves[label], "CI=(", ci_low_curves[label], ",", ci_high_curves[label], ")")

    baseline_files2 = {"Ground Truth": os.path.join("src", "baseline", "award.txt" if f == 1 else "origin.txt")}

    sizes = [5, 10, 20]

    for base_label, filepath in baseline_files2.items():
        gt_list = load_products(filepath, n_products=3)
        gt_list = [lst[101:] for lst in gt_list]

        gt_all = {
            "Bohol": gt_list[0],
            "Davao": gt_list[1],
            "ImprovedBicol": gt_list[2],
        }

        for s in sizes:
            label = f"Few-shot empirical baseline (k={s})"

            mean_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
            ci_low_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
            ci_high_curves[label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}

            vals = {p: [] for p in products}

            for _ in range(20):
                for p in products:
                    base_sample = base_all[p]                   
                    comp_sample = rng.sample(gt_all[p], s)      
                    vals[p].append(function_caller(base_sample, comp_sample, k, cost_range_index, cost_max))

            for p in products:
                m, lo, hi = mean_ci_95(vals[p])
                mean_curves[label][p] = m
                ci_low_curves[label][p] = lo
                ci_high_curves[label][p] = hi

            print(label, "mean=", mean_curves[label],
                "CI=(", ci_low_curves[label], ",", ci_high_curves[label], ")")


    if k==1:
        unshuffled_files = {"Unshuffled Persona Steering for Sampling Method": os.path.join(folder, "persona_steering_1.txt")}
        for label, filepath in unshuffled_files.items():
            new_label = label 
            mean_curves[new_label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
            ci_low_curves[new_label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}
            ci_high_curves[new_label] = {"Bohol": None, "Davao": None, "ImprovedBicol": None}

            comp_all_list = load_products(filepath, n_products=3)
            comp_all_list = [lst[:100] for lst in comp_all_list] 

            comp_all = {
                "Bohol": comp_all_list[0],
                "Davao": comp_all_list[1],
                "ImprovedBicol": comp_all_list[2],
            }

            for p in products:
                m_un = mae_unshuffled(base_all[p], comp_all[p])
                mean_curves[new_label][p] = m_un
                ci_low_curves[new_label][p] = m_un   
                ci_high_curves[new_label][p] = m_un

            print(new_label, "mean=", mean_curves[new_label], "CI=(",
              ci_low_curves[new_label], ",", ci_high_curves[new_label], ")")


if __name__ == "__main__":
    main()
