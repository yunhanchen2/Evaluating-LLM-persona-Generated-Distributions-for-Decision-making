from mistralai import Mistral

client = Mistral()

def get_gpt_ranking(prompt):
    resp = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant simulating sushi preferences."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return resp.choices[0].message.content.strip()
