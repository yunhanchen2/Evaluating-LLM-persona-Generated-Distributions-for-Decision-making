import random
import re
import json

def extract_wtp_block(text, n_lines=25):
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

#Background Steering
def build_prompt_background_steering(user_row, product_rows, example):

    products = list(product_rows) 
    random.shuffle(products)
    products_block = "\n".join(products)

    prompt = f"""
Please simulate 30 willingness-to-pay (WTP) decisions for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines and avoid always giving the same product the highest premium.

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it.

The willingness to pay could be in the range of [0,100]; if you would not exchange for that product, use 0.

Products:
{products_block}

First, give a brief justification (10 sentences).
<RATIONALE>
...
</RATIONALE>

Then output EXACTLY 30 JSON lines inside:
<WTP>
{{"premium_php": {{"Bohol": X, "Davao": Y, "ImprovedBicol": Z}}}}
(repeat until there are 30 lines; ONLY JSON dictionaries, one per line)
</WTP>

Do not output anything outside these tags.
"""
    return prompt



#Few-shot Steering
def build_prompt_few_shot_steering(user_row, product_rows, example):

    products = list(product_rows) 
    random.shuffle(products)
    products_block = "\n".join(products)

    prompt = f"""
Please simulate 30 willingness-to-pay (WTP) decisions for tablea chocolate products among consumers from Central Bicol State University of Agriculture in the Philippines and avoid always giving the same product the highest premium.

You hold an endowment chocolate (regular Bicol) worth 44 PHP.
For each target product below, report the premium (additional PHP over 44) you'd be willing to pay to exchange for it.

The willingness to pay could be in the range of [0,100]; if you would not exchange for that product, use 0.

Products:
{products_block}

Here are some examples of users' choices:
{example}

First, give a brief justification (10 sentences).
<RATIONALE>
...
</RATIONALE>

Then output EXACTLY 30 JSON lines inside:
<WTP>
{{"premium_php": {{"Bohol": X, "Davao": Y, "ImprovedBicol": Z}}}}
(repeat until there are 30 lines; ONLY JSON dictionaries, one per line)
</WTP>

Do not output anything outside these tags.
"""
    return prompt
