def get_gpt_ranking(prompt, model=1):
    if model == 1:
        from .gpt_4o import get_gpt_ranking as f
        return f(prompt)

    elif model == 2:
        from .gpt_5_mini import get_gpt_ranking as f
        return f(prompt)

    elif model == 3:
        from .gemini_3_flash_preview import get_gpt_ranking as f
        return f(prompt)

    elif model == 4:
        from .mistral_large_latest import get_gpt_ranking as f
        return f(prompt)

    else:
        raise ValueError(f"Unknown model: {model}")

