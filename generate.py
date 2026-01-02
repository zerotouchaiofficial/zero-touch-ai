import random

FACTS = [
    "Bananas are berries",
    "Octopuses have three hearts",
    "Honey never spoils",
    "Wombat poop is cube shaped",
    "Oxford University is older than the Aztecs",
    "Sharks existed before trees",
    "Hot water can freeze faster than cold water",
]

fact = random.choice(FACTS)

with open("fact.txt", "w") as f:
    f.write(fact)

print("✅ Fact:", fact)
