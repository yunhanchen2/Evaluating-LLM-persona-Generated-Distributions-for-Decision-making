import csv
import os
import pandas as pd
from data_generation.io_utils import user_to_text
from secrets import randbelow

INFILE = "Experimental Auction on Tablea Dataset (Panel).xlsx.csv"
OUT_DIR = "data_quality/src/baseline"

AWARD_COL_NAME = "bid_award"
ORIGIN_COL_NAME = "Bids_Origin"

AWARD_FALLBACK_IDX = 40   
ORIGIN_FALLBACK_IDX = 41 

def extract_and_write(col_name, fallback_idx, outfile):
    with open(INFILE, newline="", encoding="utf-8") as f, \
         open(outfile, "w", encoding="utf-8") as out:

        reader = csv.reader(f)
        header = next(reader)

        try:
            idx = header.index(col_name)
            print(f"[INFO] Using column '{col_name}' (index {idx})")
        except ValueError:
            idx = fallback_idx
            print(f"[WARN] Column '{col_name}' not found, fallback to index {idx}")

        col = [row[idx] for row in reader if len(row) > idx]

        for i in range(0, (len(col) // 3) * 3, 3):
            a, b, c = col[i], col[i+1], col[i+2]
            out.write(f"{a}\t{c}\t{b}\n")

def generate_persona(outfile):
    keep = [
        "AGE","SEX","HHINCO","MAINSH","TABLEACH",
        "IORIGIN","DARKCH","GTSEEN","GTTRUST","ACSEEN","ACTRUST"
    ]

    df = pd.read_csv(INFILE, dtype=str)

    df_sel = df[keep]
    df_every3 = df_sel.iloc[::3].reset_index(drop=True)  # 每 3 行取 1 行

    # 不要表头，直接写内容
    df_every3.to_csv(outfile, sep="\t", index=False, header=False)

def build_examples(persona_file, wtp_file, outfile, start=100, end=200):
    with open(persona_file, "r", encoding="utf-8") as f:
        persona_lines = f.readlines()

    with open(wtp_file, "r", encoding="utf-8") as f:
        wtp_lines = f.readlines()

    persona_slice = persona_lines[start:end]
    wtp_slice = wtp_lines[start:end]

    if len(persona_slice) != len(wtp_slice):
        raise ValueError(
            f"Mismatch: personas={len(persona_slice)} vs wtps={len(wtp_slice)}"
        )

    with open(outfile, "w", encoding="utf-8") as out:
        for p_line, w_line in zip(persona_slice, wtp_slice):
            fields = p_line.rstrip("\n").split("\t")[:11]
            wtp_vals = w_line.strip().split()[:3]
            wtp_text = ", ".join(wtp_vals)

            out.write(
                user_to_text(fields)
                + f" The person's WTPs are: {wtp_text}.\n"
            )

def generate_random_baseline(reference_file, outfile):
    with open(reference_file, "r", encoding="utf-8") as f:
        n_lines = sum(1 for _ in f)

    with open(outfile, "w", encoding="utf-8") as out:
        for _ in range(n_lines):
            a, b, c = randbelow(101), randbelow(101), randbelow(101)
            out.write(f"{a}\t{b}\t{c}\n")

def main():
    if not os.path.isfile(INFILE):
        raise FileNotFoundError(f"Input file not found: {INFILE}")

    os.makedirs(OUT_DIR, exist_ok=True)

    award_out = os.path.join(OUT_DIR, "award.txt")
    origin_out = os.path.join(OUT_DIR, "origin.txt")

    print("[INFO] Generating award baseline...")
    extract_and_write(AWARD_COL_NAME, AWARD_FALLBACK_IDX, award_out)

    print("[INFO] Generating origin baseline...")
    extract_and_write(ORIGIN_COL_NAME, ORIGIN_FALLBACK_IDX, origin_out)

    print("[DONE] Baseline files generated:")
    print("  ", award_out)
    print("  ", origin_out)

    persona_dir = "data_generation/src"
    os.makedirs(persona_dir, exist_ok=True)

    persona_out = os.path.join(persona_dir, "persona.txt")

    print("[INFO] Generating persona file...")
    generate_persona(persona_out)

    print("[DONE] Persona file generated:")
    print("  ", persona_out)

    examples_dir = "data_generation/src"
    os.makedirs(examples_dir, exist_ok=True)

    persona_file = os.path.join(examples_dir, "persona.txt")
    award_file = os.path.join(OUT_DIR, "award.txt")
    origin_file = os.path.join(OUT_DIR, "origin.txt")

    examples_award_out = os.path.join(examples_dir, "examples_awards.txt")
    examples_origin_out = os.path.join(examples_dir, "examples_origin.txt")

    print("[INFO] Generating award examples (100–200)...")
    build_examples(persona_file, award_file, examples_award_out, start=100, end=200)

    print("[INFO] Generating origin examples (100–200)...")
    build_examples(persona_file, origin_file, examples_origin_out, start=100, end=200)

    print("[DONE] Example files generated:")
    print("  ", examples_award_out)
    print("  ", examples_origin_out)
    
    random_out = os.path.join(OUT_DIR, "random.txt")

    print("[INFO] Generating random baseline...")
    generate_random_baseline(award_out, random_out)

    print("[DONE] Random baseline generated:")
    print("  ", random_out)


if __name__ == "__main__":
    main()
