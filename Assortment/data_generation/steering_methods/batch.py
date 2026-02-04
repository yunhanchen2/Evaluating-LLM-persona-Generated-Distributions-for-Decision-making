import random, re, json
from io_utils import sushi_to_text, user_to_text


def extract_rankings(text, n_lines=30):
    lines_out = []
    block = re.search(r"<RANKINGS>(.*?)</RANKINGS>", text, flags=re.DOTALL | re.IGNORECASE)
    candidates = block.group(1).strip().splitlines() if block else text.strip().splitlines()

    for ln in candidates:
        if re.fullmatch(r"\s*(?:[0-9]\s+){9}[0-9]\s*\Z", ln):
            parts = list(map(int, ln.strip().split()))
            if len(parts) == 10 and len(set(parts)) == 10 and all(0 <= v <= 9 for v in parts):
                lines_out.append(" ".join(map(str, parts)))
                if len(lines_out) == n_lines:
                    break
    return lines_out

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

First, provide a brief justification (around 10 sentences) inside, consider from the perspective of both sushi items:
<RATIONALE>
...
</RATIONALE>

Then, emit exactly 30 independent preference rankings from most preferred to least preferred for a user from Japan, and output ONLY the block:
<RANKINGS>
i0 i1 i2 i3 i4 i5 i6 i7 i8 i9
...
(repeat until there are exactly 30 lines; each line has exactly 10 unique integers 0..9, space-separated)
</RANKINGS>

Do not output anything else outside these blocks.
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

First, provide a brief justification (around 6 sentences) inside, consider from the perspective of both sushi items and people:
<RATIONALE>
...
</RATIONALE>

Then, emit exactly 30 independent preference rankings from most preferred to least preferred for a user from Japan, and output ONLY the block:
<RANKINGS>
i0 i1 i2 i3 i4 i5 i6 i7 i8 i9
...
(repeat until there are exactly 30 lines; each line has exactly 10 unique integers 0..9, space-separated)
</RANKINGS>

Do not output anything else outside these blocks.
"""
    return prompt

