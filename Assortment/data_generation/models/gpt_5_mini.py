from openai import OpenAI

client = OpenAI()

def get_gpt_ranking(prompt):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant simulating sushi preferences."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()