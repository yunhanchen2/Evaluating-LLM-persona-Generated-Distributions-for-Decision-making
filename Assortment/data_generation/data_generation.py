from tqdm import tqdm
from steering_methods import *
from models import *
from io_utils import *

# check whether there are 10 sushi in a line
def parse_one_line_ranking(ranking_full: str, sushi_count=10):
    valid_ids = []
    for x in ranking_full.split():
        if x.isdigit():
            val = int(x)
            if 0 <= val <= sushi_count - 1 and val not in valid_ids:
                valid_ids.append(val)
            if len(valid_ids) == sushi_count:
                break
    if len(valid_ids) != sushi_count:
        return "ERROR"
    return " ".join(map(str, valid_ids))


def main():
    print("Select model: 1-GPT-4o, 2-GPT-5-mini, 3-Gemini, 4-Mistral")
    MODEL = int(input("Enter 1–4: ")) 
    print("Select genertation method: 1-Sampling, 2-Batch, 3-Description")
    DIS = int(input("Enter 1–3: ")) 
    print("Select steering method: 1-background steering, 2-few-shot steering, 3-persona steering, 4-persona and few-shot steering")
    STR =int(input("Enter 1–4: ")) 

    if DIS in (2, 3) and STR not in (1, 2):
        raise ValueError("For DIS=2 or 3, STR must be 1 or 2")
    if DIS == 1 and STR not in (1, 2, 3, 4):
        raise ValueError("For DIS=1, STR must be 1..4")


    user_file = "src/sushi_u.txt"
    sushi_file = "src/sushi_i_a.txt"
    sample_file = "src/prompt_persona.txt"
    sushi_count = 10
    os.makedirs("results", exist_ok=True)

    # get the name of output files
    if DIS == 1:
        n_users = 600
        if STR == 1:
            output_txt = "results/no_steering_1.txt"
        elif STR == 2:
            output_txt = "results/few_shot_steering_1.txt"
        elif STR == 3:
            output_txt = "results/persona_steering_1.txt"
        elif STR == 4:
            output_txt = "results/persona_few_shot_steering_1.txt"
    elif DIS == 2:
        n_users = 20
        n_samples = 30
        if STR == 1:
            output_txt = "results/no_steering_2.txt"
        elif STR == 2:
            output_txt = "results/few_shot_steering_2.txt"
    elif DIS == 3:
        n_users = 20
        runs = []
        if STR == 1:
            output_txt = "results/no_steering_3.txt"
        elif STR == 2:
            output_txt = "results/few_shot_steering_3.txt"
    else:
        raise ValueError("MODE must be 1, 2, or 3")

    if DIS == 1 and STR in (2, 4):
        repeat_times = 5
        n_users = 300
    else:
        repeat_times = 1

    # load data
    all_users = load_user_features(user_file)

    if STR in (3, 4):
        users = all_users[2* n_users:3 * n_users]
    else:
        users = all_users[:n_users]
    sushis = load_sushi_features(sushi_file)

    total_steps = repeat_times * len(users)

    #generate data (including error checking)
    with open(output_txt, "w", encoding="utf-8") as out:
        for r in range(repeat_times):
            for user in tqdm(users, desc=f"Users (round {r+1}/{repeat_times})"):
                example = sample_fewshot_lines(sample_file, 6)
                prompt = build_prompt(user, sushis,DIS, STR, example)

                raw = get_gpt_ranking(prompt, MODEL)
                print("\n===== LLM's thinking =====")
                print(raw)

                if DIS == 1:
                    clean_ranking = parse_one_line_ranking(raw, sushi_count=sushi_count)
                    if clean_ranking == "ERROR":
                        print(f"Invalid output for user {user[0]}")
                    out.write(clean_ranking + "\n")

                elif DIS == 2:
                    rationale = extract_rationale(raw)
                    lines = extract_rankings(raw, n_lines=n_samples)
                    if len(lines) != n_samples:
                        print(f"Invalid output: expected {n_samples} lines, got {len(lines)} for user {user[0]}")
                        for i in range(n_samples):
                            if i < len(lines):
                                out.write(lines[i] + "\n")
                            else:
                                out.write("ERROR\n")
                    else:
                        for ln in lines:
                            out.write(ln + "\n")   

                elif DIS == 3:
                    utilities, _ = extract_distribution(raw)
                    if len(utilities) != sushi_count:
                        continue

                    runs.append([utilities[i] for i in range(sushi_count)])
                    out.write(" ".join(f"{utilities[i]:.6f}" for i in range(sushi_count)) + "\n")

            if DIS == 3 and runs:
                m = len(runs)
                mean_vec = [sum(run[i] for run in runs) / m for i in range(sushi_count)]
                out.write("MEAN " + " ".join(f"{u:.6f}" for u in mean_vec) + "\n")



if __name__ == "__main__":
    main()
