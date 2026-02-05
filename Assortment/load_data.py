import os
import random
import sys
import importlib.util
from data_generation.io_utils import *

def process_sushi_files(input_dir):
    path_gen = os.path.join("data_generation", "src")
    path_qual = os.path.join("data_quality", "src", "baseline")
    
    for p in [path_gen, path_qual]:
        os.makedirs(p, exist_ok=True)

    src_a = os.path.join(input_dir, "sushi3a.5000.10.order")
    if os.path.exists(src_a):
        with open(src_a, "r", encoding="utf-8") as f:
            lines = f.readlines()[1:] 

        processed_a = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 2:
                processed_a.append(" ".join(parts[2:]) + "\n")

        for target_dir in [path_gen, path_qual]:
            with open(os.path.join(target_dir, "5000_a.txt"), "w", encoding="utf-8") as f:
                f.writelines(processed_a)
        
        with open(os.path.join(path_qual, "Ground Truth.txt"), "w", encoding="utf-8") as f:
            f.writelines(processed_a[:600])
            
        print(f"Successfully processed sushi3a -> 5000_a.txt and Ground Truth.txt")

    src_u = os.path.join(input_dir, "sushi3.udata")
    if os.path.exists(src_u):
        dst_u = os.path.join(path_gen, "sushi_u.txt")
        with open(src_u, "r", encoding="utf-8") as f_in, \
             open(dst_u, "w", encoding="utf-8") as f_out:
            f_out.write(f_in.read())
        print("Copied sushi3.udata -> sushi_u.txt")

    src_i = os.path.join(input_dir, "sushi3.idata")
    if os.path.exists(src_i):
        dst_i = os.path.join(path_gen, "sushi_i_a.txt")
        with open(src_i, "r", encoding="utf-8") as f:
            i_lines = f.readlines()

        with open(dst_i, "w", encoding="utf-8") as f:
            f.writelines(i_lines[:10])
        print("Processed sushi3.idata -> sushi_i_a.txt (first 10 lines)")

    items = list(range(10))
    random_rankings = []
    for _ in range(600):
        shuffled = items[:]
        random.shuffle(shuffled) 
        random_rankings.append(" ".join(map(str, shuffled)) + "\n")
    
    with open(os.path.join(path_qual, "random.txt"), "w", encoding="utf-8") as f:
        f.writelines(random_rankings)
    print(f"Successfully generated random.txt")

    u_txt_path = os.path.join(path_gen, "sushi_u.txt")
    if os.path.exists(u_txt_path) and len(processed_a) >= 1200:
        u_data = load_user_features(u_txt_path)
        
        prompt_persona_list = []
        for i in range(600, 1200):
            user_desc = user_to_text(u_data[i])
            ranking = processed_a[i].strip()

            line = f"{user_desc} Ranks the sushi as: {ranking}\n"
            prompt_persona_list.append(line)
        
        with open(os.path.join(path_gen, "prompt_persona.txt"), "w", encoding="utf-8") as f:
            f.writelines(prompt_persona_list)
        print("Successfully generated prompt_persona.txt")

    
if __name__ == "__main__":
    process_sushi_files(input_dir="sushi3-2016")