import random, json, os

USED_FILE = "used_facts.json"

SUBJECTS = [
    "Octopuses", "Honey", "Bananas", "The Moon", "Sharks",
    "Butterflies", "Venus", "The human brain", "Wombats",
    "Dolphins", "Goldfish", "Lightning", "Ants", "Saturn"
]

FACTS = [
    "have three hearts",
    "never spoils naturally",
    "are technically berries",
    "has moonquakes",
    "existed before trees",
    "can taste using their feet",
    "has a day longer than its year",
    "uses about 20 percent of body oxygen",
    "produce cube-shaped poop",
    "can recognize themselves in mirrors",
    "can remember things for months",
    "is hotter than the surface of the sun",
    "can lift objects many times their weight",
    "could float in water"
]

def load_used():
    if not os.path.exists(USED_FILE):
        return set()
    with open(USED_FILE, "r") as f:
        return set(json.load(f))

def save_used(used):
    with open(USED_FILE, "w") as f:
        json.dump(list(used), f, indent=2)

def generate_fact(used):
    while True:
        fact = f"{random.choice(SUBJECTS)} {random.choice(FACTS)}."
        if fact not in used:
            return fact
