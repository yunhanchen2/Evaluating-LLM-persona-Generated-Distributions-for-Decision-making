from .batch import (
    build_prompt_background_steering as _batch_background,
    build_prompt_few_shot_steering as _batch_fewshot,
    extract_wtp_block as extract_wtp_block_batch,
)

from .sampling import (
    build_prompt_background_steering as _samp_background,
    build_prompt_few_shot_steering as _samp_fewshot,
    build_prompt_persona_steering as _samp_persona,
    build_prompt_persona_and_few_shot_steering as _samp_persona_fewshot,
    extract_premiums_from_text,
)

from .description import (
    build_prompt_background_steering as _dist_background,
    build_prompt_few_shot_steering as _dist_fewshot,
    extract_wtp_block as extract_wtp_block_distribution,
    extract_rationale,
    extract_output_json,
    line_to_expanded_structure,
)

def build_prompt(user_row, product_rows, dis: int, steer: int, example=None):
    if dis == 1:
        if steer == 1:
            return _samp_background(user_row, product_rows,example)
        elif steer == 2:
            return _samp_fewshot(user_row, product_rows,example)
        elif steer == 3:
            return _samp_persona(user_row, product_rows,example)
        elif steer == 4:
            return _samp_persona_fewshot(user_row, product_rows,example)
        else:
            raise ValueError("sampling (dis=1): steer must be 1..4")

    elif dis == 2:
        if steer == 1:
            return _batch_background(user_row, product_rows,example)
        elif steer == 2:
            return _batch_fewshot(user_row, product_rows,example)
        else:
            raise ValueError("batch (dis=2): steer must be 1 (background) or 2 (few-shot)")

    elif dis == 3:
        if steer == 1:
            return _dist_background(user_row, product_rows,example)
        elif steer == 2:
            return _dist_fewshot(user_row, product_rows,example)
        else:
            raise ValueError("distribution (dis=3): steer must be 1 (background) or 2 (few-shot)")

    else:
        raise ValueError("dis must be 1 (sampling), 2 (batch), or 3 (distribution)")

__all__ = [
    "build_prompt",

    "extract_premiums_from_text",

    "extract_wtp_block_batch",

    "extract_wtp_block_distribution",
    "extract_rationale",
    "extract_output_json",
    "line_to_expanded_structure",
]
