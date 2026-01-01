import os
import random

FACTS = [
    "Wombat poop is cube-shaped.",
    "Honey never spoils.",
    "Your brain uses about 20 percent of your body's energy.",
    "Octopus have three hearts.",
    "Bananas are berries but strawberries are not."
]

os.makedirs("data", exist_ok=True)

fact = random.choice(FACTS)

with open("data/text.txt", "w", encoding="utf-8") as f:
    f.write(fact)

print(fact)
