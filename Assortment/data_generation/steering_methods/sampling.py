import random, re, json
from io_utils import sushi_to_text, user_to_text


def build_prompt_background_steering(user_row, sushi_rows, example):
    sushi_rows = sushi_rows.copy()
    random.shuffle(sushi_rows) #for not always make sushi 0 to be the first items show to LLM

    sushi_info = "\n".join([sushi_to_text(s) for s in sushi_rows])
    
    prompt = f"""
Please simulate a sushi ranking for Japanese consumers and avoid always ranking the same item first.

Sushi items:
{sushi_info}

Return **exactly 10 unique integers from 0 to 9**, in order of preference from most preferred to least preferred, like:
0 1 2 3 4 5 6 7 8 9 (this is a fake ranking)
Return your reasoning first, then output the final sushi ranking in a new line.
"""
    return prompt

def build_prompt_persona_steering(user_row, sushi_rows, example):
    user_text = user_to_text(user_row)

    sushi_rows = sushi_rows.copy()
    random.shuffle(sushi_rows)

    sushi_info = "\n".join([sushi_to_text(s) for s in sushi_rows])
    
    prompt = f"""
Please simulate a sushi ranking for Japanese consumers and avoid always ranking the same item first. 

Sushi items:
{sushi_info}

Here is a persona description of the one you should pretend to be.
{user_text}

Return **exactly 10 unique integers from 0 to 9**, in order of preference from most preferred to least preferred, like:
0 1 2 3 4 5 6 7 8 9 (this is a fake ranking)
Return your reasoning first, then output the final sushi ranking in a new line.
"""
    return prompt


def build_prompt_few_shot_steering(user_row, sushi_rows, example):
    sushi_rows = sushi_rows.copy()
    random.shuffle(sushi_rows) #for not always make sushi 0 to be the first items show to LLM

    sushi_info = "\n".join([sushi_to_text(s) for s in sushi_rows])
    
    prompt = f"""
Please simulate a sushi ranking for Japanese consumers and avoid always ranking the same item first.

Sushi items:
{sushi_info}

We already know some choices made by customers:
{example}

Return **exactly 10 unique integers from 0 to 9**, in order of preference from most preferred to least preferred, like:
0 1 2 3 4 5 6 7 8 9 (this is a fake ranking)
Return your reasoning first, then output the final sushi ranking in a new line.
"""
    return prompt


def build_prompt_persona_few_shot_steering(user_row, sushi_rows, example):
    user_text = user_to_text(user_row)

    sushi_rows = sushi_rows.copy()
    random.shuffle(sushi_rows)

    sushi_info = "\n".join([sushi_to_text(s) for s in sushi_rows])
    
    prompt = f"""
Please simulate a sushi ranking for Japanese consumers and avoid always ranking the same item first. 

Sushi items:
{sushi_info}

Here is a persona description of the one you should pretend to be.
{user_text}

We already know some choices made by customers:
{example}

Return **exactly 10 unique integers from 0 to 9**, in order of preference from most preferred to least preferred, like:
0 1 2 3 4 5 6 7 8 9 (this is a fake ranking)
Return your reasoning first, then output the final sushi ranking in a new line.
"""
    return prompt
