import random
import re
import json
import numpy as np


def extract_wtp_block(text, n_lines=30):
    # Extract <WTP> ... </WTP>
    block = re.search(r"<WTP>(.*?)</WTP>", text, flags=re.DOTALL | re.IGNORECASE)
    if not block:
        return []

    lines = block.group(1).strip().splitlines()
    out = []
    for ln in lines:
        ln = ln.strip()
        # try parse JSON
        try:
            obj = json.loads(ln)
            prem = obj["premium_php"]
            b = float(prem["Bohol"])
            d = float(prem["Davao"])
            i = float(prem["ImprovedBicol"])
            out.append(f"{b}\t{d}\t{i}")
        except:
            out.append("ERROR")

        if len(out) == n_lines:
            break

    return out

def extract_rationale(text):
    m = re.search(r"<RATIONALE>(.*?)</RATIONALE>", text,
                  flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    rationale = m.group(1).strip()
   
    rationale = re.sub(r"\s+", " ", rationale)
    return rationale


def extract_output_json(text):
    m = re.search(r"<OUTPUT>(.*?)</OUTPUT>", text, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    blob = m.group(1).strip()
    try:
        return json.loads(blob)
    except:
        return None

def line_to_expanded_structure(line, n=100):
    """
    Input: one JSON line from no_steering_3_awards_distribution.txt
    Output: dict with expanded lists of length n for each product (proportion-based, deterministic)
    """
    dist = json.loads(line)
    supp = dist["premium_support"]
    probs = dist["probabilities"]

    def expand(values, ps):
        ps = np.array(ps, dtype=float)
        raw = ps * n
        cnt = np.floor(raw).astype(int)
        rem = n - cnt.sum()

        # allocate remaining slots to largest fractional parts
        frac = raw - np.floor(raw)
        order = np.argsort(-frac)
        for k in range(rem):
            cnt[order[k]] += 1

        out = []
        for v, c in zip(values, cnt):
            out += [v] * int(c)
        return out  # length n

    expanded = {
        "Bohol": expand(supp["Bohol"], probs["Bohol"]),
        "Davao": expand(supp["Davao"], probs["Davao"]),
        "ImprovedBicol": expand(supp["ImprovedBicol"], probs["ImprovedBicol"]),
    }
    return expanded

#Background Steering

def build_prompt_background_steering(user_row, product_rows, example):
    products = list(product_rows)
    random.shuffle(products)
    products_block = "\n".join(products)

    prompt = f"""
Please simulate 25 willingness-to-pay (WTP) decisions for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines.

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it. 

Products:
{products_block}

Requirements:
- For EACH product, output EXACTLY 5 most likely premium values (integers).
- The 5 values MUST include 0 (meaning you would not exchange).
- Each premium value must be between 0 and 100 (inclusive).
- Output the probability (as a decimal) for each of the 5 values.
- Probabilities must be non-negative and sum to 1 for each product.
- Avoid identical distributions across the three products unless strongly justified.

Output format (STRICT):
First, briefly explain your reasoning in EXACTLY 10 sentences.
<RATIONALE>
...
</RATIONALE>

<OUTPUT>
{{
  "premium_support": {{
    "Bohol": [v1, v2, v3, v4, v5],
    "Davao": [v1, v2, v3, v4, v5],
    "ImprovedBicol": [v1, v2, v3, v4, v5]
  }},
  "probabilities": {{
    "Bohol": [p1, p2, p3, p4, p5],
    "Davao": [p1, p2, p3, p4, p5],
    "ImprovedBicol": [p1, p2, p3, p4, p5]
  }}
}}
</OUTPUT>

Do not output anything outside <OUTPUT>...</OUTPUT>.
"""
    return prompt


#Few-shot Steering
def build_prompt_few_shot_steering(user_row, product_rows, example):
    products = list(product_rows)
    random.shuffle(products)
    products_block = "\n".join(products)

    prompt = f"""
Please simulate 25 willingness-to-pay (WTP) decisions for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines.

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it. 

Products:
{products_block}

Here are some examples of users' choices:
{example}

Requirements:
- For EACH product, output EXACTLY 5 most likely premium values (integers).
- The 5 values MUST include 0 (meaning you would not exchange).
- Each premium value must be between 0 and 100 (inclusive).
- Output the probability (as a decimal) for each of the 5 values.
- Probabilities must be non-negative and sum to 1 for each product.
- Avoid identical distributions across the three products unless strongly justified.

Output format (STRICT):
First, briefly explain your reasoning in EXACTLY 10 sentences.
<RATIONALE>
...
</RATIONALE>

<OUTPUT>
{{
  "premium_support": {{
    "Bohol": [v1, v2, v3, v4, v5],
    "Davao": [v1, v2, v3, v4, v5],
    "ImprovedBicol": [v1, v2, v3, v4, v5]
  }},
  "probabilities": {{
    "Bohol": [p1, p2, p3, p4, p5],
    "Davao": [p1, p2, p3, p4, p5],
    "ImprovedBicol": [p1, p2, p3, p4, p5]
  }}
}}
</OUTPUT>

Do not output anything outside <OUTPUT>...</OUTPUT>.
"""
    return prompt

