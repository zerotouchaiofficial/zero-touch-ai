import random, json

FACT_POOL = [
    "Octopuses have three hearts",
    "Bananas are berries but strawberries are not",
    "Honey never spoils",
    "Wombat poop is cube shaped",
    "Oxford University is older than the Aztecs",
    "Sharks existed before trees",
    "Hot water can freeze faster than cold water",
    "Cows have best friends",
]

facts = random.sample(FACT_POOL, 5)

with open("facts.json", "w") as f:
    json.dump(facts, f)

print("✅ Facts generated")
