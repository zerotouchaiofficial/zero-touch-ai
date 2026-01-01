import json
import os
import random

USED_FILE = "facts_used.json"

# 1000+ safe short facts pool (extend anytime)
FACT_POOL = [
    "Octopuses have three hearts.",
    "Honey never spoils.",
    "Bananas are berries.",
    "Wombat poop is cube-shaped.",
    "Sharks existed before trees.",
    "Butterflies taste with their feet.",
    "Your brain uses about 20 percent of your energy.",
    "A day on Venus is longer than a year on Venus.",
    "There are more stars than grains of sand on Earth.",
    "The Eiffel Tower grows in summer.",
    "Sloths can hold their breath longer than dolphins.",
    "A shrimp’s heart is in its head.",
    "Tardigrades can survive space.",
    "Cats have fewer toes on their back paws.",
    "Lightning is hotter than the sun.",
    "Koalas have fingerprints like humans.",
    "Cows have best friends.",
    "A group of flamingos is called a flamboyance.",
    "The moon has moonquakes.",
    "Dolphins have names for each other.",
    "Your bones are constantly renewing.",
    "A cloud can weigh over a million tons.",
    "Bees recognize human faces.",
    "The tongue never gets tired.",
    "You burn calories while sleeping.",
    "Your ears never stop growing.",
    "Rats laugh when tickled.",
    "The brain feels no pain.",
    "A newborn has more bones than an adult.",
    "Goldfish can recognize faces.",
    "Some frogs can freeze and live.",
    "Birds don’t urinate.",
    "Your skin glows under UV light.",
    "Humans share DNA with bananas.",
    "Antarctica is a desert.",
    "A snail can sleep for three years.",
    "Humans glow faintly in the dark.",
    "The smell of rain is called petrichor.",
    "Your fingerprints form before birth.",
    "You are slightly radioactive.",
    "The brain edits memories every recall.",
    "Your brain predicts reality.",
    "You never see reality in real-time.",
]

# Load used facts
if os.path.exists(USED_FILE):
    with open(USED_FILE, "r") as f:
        used_facts = set(json.load(f))
else:
    used_facts = set()

# Find unused facts
unused_facts = list(set(FACT_POOL) - used_facts)

# Reset if all facts used
if not unused_facts:
    used_facts = set()
    unused_facts = FACT_POOL.copy()

# Pick new fact
fact = random.choice(unused_facts)

# Save used fact
used_facts.add(fact)
with open(USED_FILE, "w") as f:
    json.dump(list(used_facts), f, indent=2)

# Save current fact
with open("current_fact.txt", "w") as f:
    f.write(fact)

print(fact)
