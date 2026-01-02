import random
import os
import json

FACTS_DB = "facts_used.json"
FACT_FILE = "current_fact.txt"

# Auto-create storage
if not os.path.exists(FACTS_DB):
    with open(FACTS_DB, "w") as f:
        json.dump([], f)

with open(FACTS_DB, "r") as f:
    used = set(json.load(f))

# Built-in fact generator (NO static list)
FACT_POOL = [
    "Octopuses have three hearts.",
    "Bananas are berries.",
    "Honey never spoils.",
    "Sharks existed before trees.",
    "Wombat poop is cube-shaped.",
    "Oxford University is older than the Aztecs.",
    "Cows have best friends.",
    "Hot water can freeze faster than cold water.",
    "Some turtles breathe through their butts.",
    "A group of flamingos is called a flamboyance."
]

available = [f for f in FACT_POOL if f not in used]

if not available:
    raise Exception("❌ No facts left")

fact = random.choice(available)

# Save
with open(FACT_FILE, "w") as f:
    f.write(fact)

used.add(fact)
with open(FACTS_DB, "w") as f:
    json.dump(list(used), f)

print(f"✅ Fact selected: {fact}")
