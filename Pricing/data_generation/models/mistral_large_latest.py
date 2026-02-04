from mistralai import Mistral

client = Mistral()

def get_gpt_premiums(prompt):
    resp = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant simulating willingness to pay."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return resp.choices[0].message.content.strip()
