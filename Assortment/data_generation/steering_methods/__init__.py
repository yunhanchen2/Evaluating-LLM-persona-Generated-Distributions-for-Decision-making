from .batch import (
    build_prompt_background_steering as _batch_background,
    build_prompt_few_shot_steering as _batch_fewshot,
    extract_rationale, extract_rankings, 
)

from .sampling import (
    build_prompt_background_steering as _samp_background,
    build_prompt_few_shot_steering as _samp_fewshot,
    build_prompt_persona_steering as _samp_persona,
    build_prompt_persona_few_shot_steering as _samp_persona_fewshot,
)

from .description import (
    build_prompt_background_steering as _desc_background,
    build_prompt_few_shot_steering as _desc_fewshot,
    extract_distribution,
)


def build_prompt(user_row, sushi_rows, dis: int, str: int, example):
    if dis == 1:
        if str == 1:
            return _samp_background(user_row, sushi_rows, example)
        elif str == 2:
            return _samp_fewshot(user_row, sushi_rows, example)
        elif str == 3:
            return _samp_persona(user_row, sushi_rows, example)
        elif str == 4:
            return _samp_persona_fewshot(user_row, sushi_rows, example)
        else:
            raise ValueError("sampling (dis=1): str must be 1..4")

    elif dis == 2:
        if str == 1:
            return _batch_background(user_row, sushi_rows, example)
        elif str == 2:
            return _batch_fewshot(user_row, sushi_rows, example)
        else:
            raise ValueError("batch (dis=2): str must be 1 (background) or 2 (few-shot)")

    elif dis == 3:
        if str == 1:
            return _desc_background(user_row, sushi_rows, example)
        elif str == 2:
            return _desc_fewshot(user_row, sushi_rows, example)
        else:
            raise ValueError("description (dis=3): str must be 1 (background) or 2 (few-shot)")

    else:
        raise ValueError("dis must be 1 (sampling), 2 (batch), or 3 (description)")


__all__ = [
    "build_prompt",
    "extract_rationale",
    "extract_rankings",
    "extract_distribution",
]

