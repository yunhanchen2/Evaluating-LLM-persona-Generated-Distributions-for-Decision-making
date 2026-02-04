import re
import json
import random

def extract_premiums_from_text(full_text: str):
    cleaned = full_text.replace("```json", "").replace("```", "").strip()

    json_blocks = re.findall(r"\{[^{}]*premium_php[^{}]*\{.*?\}.*?\}", cleaned, flags=re.DOTALL)

    if not json_blocks:
        json_blocks = re.findall(r"\{.*?\}", cleaned, flags=re.DOTALL)

    for cand in json_blocks:
        try:
            obj = json.loads(cand)
            prem = obj.get("premium_php", obj)
            b = float(prem["Bohol"])
            d = float(prem["Davao"])
            i = float(prem["ImprovedBicol"])
            return [b, d, i]
        except Exception:
            continue

    def find_key_num(key: str):
        m = re.search(rf'"{key}"\s*:\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', cleaned)
        return float(m.group(1)) if m else None

    b = find_key_num("Bohol")
    d = find_key_num("Davao")
    i = find_key_num("ImprovedBicol")
    if b is not None and d is not None and i is not None:
        return [b, d, i]

    found = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', cleaned)
    if len(found) >= 3:
        return [float(found[0]), float(found[1]), float(found[2])]

    return None

#Background Steering
def build_prompt_background_steering(user_row, product_rows, example):
    products = list(product_rows) 
    products_shown = products[:]
    random.shuffle(products_shown)
    products_block = "\n".join(products_shown)

    prompt = f"""
Please simulate a willingness-to-pay (WTP) decision for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines and avoid always giving the same product the highest premium.

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it.

The willingness to pay could be in the range of [0,100]; if you would not exchange for that product, use 0.

Products:
{products_block}

Return your reasoning first (no more than 10 short sentences).

Then, on a NEW LINE, return EXACTLY ONE JSON object with this exact shape and keys (numbers only, no currency symbols):
{{"premium_php": {{"Bohol": 0, "Davao": 0, "ImprovedBicol": 0}}}} (this is a fake wtp)
""".strip()
    return prompt



#Persona Steering
def build_prompt_persona_steering(user_row, product_rows, example):
    user_text = user_row

    products = list(product_rows) 
    products_shown = products[:]
    random.shuffle(products_shown)
    products_block = "\n".join(products_shown)

    prompt = f"""
Please simulate a willingness-to-pay (WTP) decision for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines and avoid always giving the same product the highest premium.

Pretend you are the persona:
{user_text}

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it.

The willingness to pay could be in the range of [0,100]; if you would not exchange for that product, use 0.

Products:
{products_block}

Return your reasoning first (no more than 10 short sentences).

Then, on a NEW LINE, return EXACTLY ONE JSON object with this exact shape and keys (numbers only, no currency symbols):
{{"premium_php": {{"Bohol": 0, "Davao": 0, "ImprovedBicol": 0}}}} (this is a fake wtp)
""".strip()
    return prompt


#Few-shot Steering
def build_prompt_few_shot_steering(user_row, product_rows, example):
    products = list(product_rows) 
    products_shown = products[:]
    random.shuffle(products_shown)
    products_block = "\n".join(products_shown)

    prompt = f"""
Please simulate a willingness-to-pay (WTP) decision for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines and avoid always giving the same product the highest premium.

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it.

The willingness to pay could be in the range of [0,100]; if you would not exchange for that product, use 0.

Products:
{products_block}

Here are some examples of users' choices:
{example}

Return your reasoning first (no more than 10 short sentences).

Then, on a NEW LINE, return EXACTLY ONE JSON object with this exact shape and keys (numbers only, no currency symbols):
{{"premium_php": {{"Bohol": 0, "Davao": 0, "ImprovedBicol": 0}}}} (this is a fake wtp)
""".strip()
    return prompt



#Few-shot + Persona Steering
def build_prompt_persona_and_few_shot_steering(user_row, product_rows, example):
    user_text = user_row

    products = list(product_rows) 
    products_shown = products[:]
    random.shuffle(products_shown)
    products_block = "\n".join(products_shown)

    prompt = f"""
Please simulate a willingness-to-pay (WTP) decision for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines and avoid always giving the same product the highest premium.

Pretend you are the persona:
{user_text}

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it.

The willingness to pay could be in the range of [0,100]; if you would not exchange for that product, use 0.

Products:
{products_block}

Here are some examples of users' choices:
{example}

Return your reasoning first (no more than 10 short sentences).

Then, on a NEW LINE, return EXACTLY ONE JSON object with this exact shape and keys (numbers only, no currency symbols):
{{"premium_php": {{"Bohol": 0, "Davao": 0, "ImprovedBicol": 0}}}} (this is a fake wtp)
""".strip()
    return prompt