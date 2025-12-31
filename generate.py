import requests, random, os

API_KEY = os.getenv("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")

PROMPTS = [
    "Give one shocking but true science fact in max 18 words.",
    "Give one psychology fact that sounds unbelievable but is true. Max 18 words.",
    "Give one space fact most people don't know. Max 18 words."
]

def get_fact():
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": random.choice(PROMPTS)}]
        }
    )
    return r.json()["choices"][0]["message"]["content"]

fact = get_fact()

with open("fact.txt", "w") as f:
    f.write(fact)
