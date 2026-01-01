import random

FACTS = [
    "Honey never spoils.",
    "Wombat poop is cube-shaped.",
    "Octopuses have three hearts.",
    "Your brain uses 20 percent of your body's energy.",
    "Bananas are berries."
]

fact = random.choice(FACTS)

with open("facts.txt", "w") as f:
    f.write(fact)

print(fact)
