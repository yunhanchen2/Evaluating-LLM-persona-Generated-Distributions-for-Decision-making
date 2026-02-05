import os
import json
from tqdm import tqdm
from steering_methods import *
from models import *
from io_utils import *

def main():
    print("Select model: 1-GPT-4o, 2-GPT-5-mini, 3-Gemini, 4-Mistral")
    MODEL = int(input("Enter 1–4: ")) 
    print("Select genertation method: 1-Sampling, 2-Batch, 3-Description")
    DIS = int(input("Enter 1–3: ")) 
    print("Select steering method: 1-background steering, 2-few-shot steering, 3-persona steering, 4-persona and few-shot steering")
    STR =int(input("Enter 1–4: ")) 
    print("Select information type: 1-provide awards, 2-provide origin")
    INFO = int(input("Enter 1–2: ")) 
    os.makedirs("results", exist_ok=True)

    if INFO == 1:
        os.makedirs("results/awards", exist_ok=True)
        base_dir = "results/awards"
        product = [
        "- Bohol (won Academy of Chocolate)",
        "- Davao (won Great Taste)",
        "- Improved Bicol (no award)",
        ]
    elif INFO == 2:
        os.makedirs("results/origin", exist_ok=True)
        base_dir = "results/origin"
        product = [
        "- Bohol (origin: Bohol island cacao)",
        "- Davao (origin: Davao region cacao)",
        "- Improved Bicol (origin: Bicol region cacao)",
        ]
    else:
        raise ValueError("INFO must be 1 (awards) or 2 (origin)")


    # get the name of output files
    if DIS == 1:
        n_groups= 100
        if STR == 1:
            output_txt = f"{base_dir}/no_steering_1.txt"
        elif STR == 2:
            output_txt = f"{base_dir}/few_shot_steering_1.txt"
        elif STR == 3:
            output_txt = f"{base_dir}/persona_steering_1.txt"
        elif STR == 4:
            output_txt = f"{base_dir}/persona_few_shot_steering_1.txt"
    elif DIS == 2:
        n_groups = 20
        n_per_call = 30
        if STR == 1:
            output_txt = f"{base_dir}/no_steering_2.txt"
        elif STR == 2:
            output_txt = f"{base_dir}/few_shot_steering_2.txt"
    elif DIS == 3:
        n_groups = 20
        runs = []
        if STR == 1:
            output_txt = f"{base_dir}/no_steering_3.txt"
        elif STR == 2:
            output_txt = f"{base_dir}/few_shot_steering_3.txt"
    else:
        raise ValueError("MODE must be 1, 2, or 3")

    if DIS == 1 and STR in (2, 4):
        repeat_times = 5
    else:
        repeat_times = 1


    example = sample_fewshot_lines(6, INFO)

    user_file = "src/persona.txt"
    all_users = load_user_features(user_file)

    if STR in (3, 4):
        users = all_users[n_groups:2 * n_groups]
    else:
        users = all_users[:n_groups]

    if DIS == 1:
        with open(output_txt, "w", encoding="utf-8") as out:
            for r in range(repeat_times):
                for idx, user in enumerate(tqdm(users, desc=f"Personas (round {r+1}/{repeat_times})")):
                    prompt = build_prompt(user, product, DIS, STR, example)
                    full = get_gpt_premiums(prompt, MODEL)
                    print(f"\n--- LLM OUTPUT ---")
                    print(full)

                    nums = extract_premiums_from_text(full)

                    if nums is not None and len(nums) == 3:
                        clean_line = f"{nums[0]}\t{nums[1]}\t{nums[2]}"
                    else:
                        print(f"Invalid output (need exactly 3 numbers) for line")
                        clean_line = "ERROR"

                    out.write(clean_line + "\n")

    elif DIS == 2:
        print(f"[INFO] n_groups={n_groups}, n_per_call={n_per_call}")

        with open(output_txt, "w", encoding="utf-8") as out:
            for g in tqdm(range(n_groups), desc="GPT batches"):
                prompt = build_prompt(None, product, DIS, STR, example)
                raw = get_gpt_premiums(prompt, MODEL)
                lines = extract_wtp_block_batch(raw, n_lines=n_per_call)

                if len(lines) != n_per_call:
                    print(f"Expected {n_per_call} lines but got {len(lines)} in batch {g}")
                    for i in range(n_per_call):
                        if i < len(lines):
                            out.write(lines[i] + "\n")
                        else:
                            out.write("ERROR\n")
                else:
                    for ln in lines:
                        out.write(ln + "\n")

    elif DIS == 3:
        print(f"[INFO] n_groups={n_groups}")

        with open(output_txt, "w", encoding="utf-8") as out:
            for g in tqdm(range(n_groups), desc="GPT batches"):
                prompt = build_prompt(None, product, DIS, STR, example)
                raw = get_gpt_premiums(prompt, MODEL)
                rationale = extract_rationale(raw)
                if rationale:
                    print(f"\n[Batch {g}] RATIONALE:")
                    print(rationale)
                else:
                    print(f"\n[Batch {g}] No rationale found")

                obj = extract_output_json(raw)
                if obj is None:
                    out.write("ERROR\n")
                else:
                    out.write(json.dumps(obj, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
