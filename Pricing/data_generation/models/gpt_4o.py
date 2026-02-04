from openai import OpenAI

client = OpenAI()

def get_gpt_premiums(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant simulating willingness to pay."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()