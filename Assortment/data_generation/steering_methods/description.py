import random, re, json
from io_utils import sushi_to_text, user_to_text


def extract_distribution(text):
    m = re.search(r"<DISTRIBUTION>(.*?)</DISTRIBUTION>", text, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return {}, {}
    block = m.group(1).strip()
    try:
        data = json.loads(block)
    except Exception:
        j = re.search(r"\{.*\}", block, flags=re.DOTALL)
        if not j:
            return {}, {}
        try:
            data = json.loads(j.group(0))
        except Exception:
            return {}, {}

    utils = data.get("utilities", {})
    reasons = data.get("reasons", {})

    u_out = {}
    for k, v in utils.items():
        try:
            ki = int(k)
            u_out[ki] = float(v)
        except Exception:
            continue

    r_out = {}
    if isinstance(reasons, dict):
        for k, v in reasons.items():
            try:
                ki = int(k)
                r_out[ki] = str(v)
            except Exception:
                continue

    return u_out, r_out


def extract_rationale(text, max_chars=800):
    m = re.search(r"<RATIONALE>(.*?)</RATIONALE>", text, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    rationale = m.group(1).strip()

    rationale = re.sub(r"\s+", " ", rationale)
    if len(rationale) > max_chars:
        rationale = rationale[:max_chars].rstrip() + "..."
    return rationale


def build_prompt_background_steering(user_row, sushi_rows, example):
    sushi_rows = sushi_rows.copy()
    random.shuffle(sushi_rows)
    sushi_info = "\n".join([sushi_to_text(s) for s in sushi_rows])

    prompt = f"""
Please simulate sushi rankings for Japanese consumers and avoid always ranking the same item first. 

Sushi items:
{sushi_info}

First, provide a concise justification (≤ 10 sentences) considering both item attributes and people:
<RATIONALE>
...
</RATIONALE>

Then, DO NOT produce rankings. Instead, VERBALIZE the utilities for the 10 sushi IDs.
Only output the following JSON block (no extra text outside the block). Keys must be the IDs 0..9 exactly once; utilities can be any real numbers (scale/shift invariant) and must be floats in [0, 5], the higher the more prefered. 

<DISTRIBUTION>
{{
  "utilities": {{
    "0": <float>, "1": <float>, "2": <float>, "3": <float>, "4": <float>,
    "5": <float>, "6": <float>, "7": <float>, "8": <float>, "9": <float>
  }},
}}
</DISTRIBUTION>
"""
    return prompt

def build_prompt_few_shot_steering(user_row, sushi_rows, example):
    sushi_rows = sushi_rows.copy()
    random.shuffle(sushi_rows)
    sushi_info = "\n".join([sushi_to_text(s) for s in sushi_rows])

    prompt = f"""
Please simulate sushi rankings for Japanese consumers and avoid always ranking the same item first. 

Sushi items:
{sushi_info}

We already know some choices made by customers:
{example}

First, provide a concise justification (≤ 10 sentences) considering both item attributes and people:
<RATIONALE>
...
</RATIONALE>

Then, DO NOT produce rankings. Instead, VERBALIZE the utilities for the 10 sushi IDs.
Only output the following JSON block (no extra text outside the block). Keys must be the IDs 0..9 exactly once; utilities can be any real numbers (scale/shift invariant) and must be floats in [0, 5], the higher the more prefered. 

<DISTRIBUTION>
{{
  "utilities": {{
    "0": <float>, "1": <float>, "2": <float>, "3": <float>, "4": <float>,
    "5": <float>, "6": <float>, "7": <float>, "8": <float>, "9": <float>
  }},
}}
</DISTRIBUTION>
"""
    return prompt