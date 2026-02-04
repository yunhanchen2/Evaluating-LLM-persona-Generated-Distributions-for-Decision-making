from google import genai
from google.genai import types

client = genai.Client()

def get_gpt_ranking(prompt):
    config = types.GenerateContentConfig(
        temperature=0.0,
        system_instruction="You are a helpful assistant simulating sushi preferences.",
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.MEDIUM  # LOW / MEDIUM / HIGH
        ),
    )
    MODEL_NAME = "gemini-3-flash-preview"
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )

    return (response.text or "").strip()