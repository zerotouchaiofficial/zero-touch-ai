import random, json, os

USED_FILE = "used_facts.json"

FACT_TEMPLATES = [
    "{animal} can {ability}.",
    "Did you know? {object} is {property}.",
    "{planet} has {space_fact}.",
    "Scientists discovered that {science_fact}.",
    "{food} has {food_fact}."
]

ANIMALS = [
    ("Octopus", "three hearts"),
    ("Dolphin", "recognize itself in mirrors"),
    ("Shark", "existed before trees"),
    ("Wombat", "cube-shaped poop")
]

OBJECTS = [
    ("Honey", "never spoils"),
    ("Glass", "is technically a slow-moving liquid"),
    ("Banana", "classified as a berry"),
    ("Eiffel Tower", "grows taller in summer")
]

PLANETS = [
    ("Venus", "a day longer than its year"),
    ("Jupiter", "the biggest storm in the solar system"),
    ("Mars", "the tallest volcano ever"),
]

FOODS = [
    ("Chocolate", "was once used as money"),
    ("Cheese", "is the most stolen food"),
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
        template = random.choice(FACT_TEMPLATES)

        if "{animal}" in template:
            a, f = random.choice(ANIMALS)
            fact = template.format(animal=a, ability=f)

        elif "{object}" in template:
            o, p = random.choice(OBJECTS)
            fact = template.format(object=o, property=p)

        elif "{planet}" in template:
            p, s = random.choice(PLANETS)
            fact = template.format(planet=p, space_fact=s)

        elif "{food}" in template:
            f, x = random.choice(FOODS)
            fact = template.format(food=f, food_fact=x)

        else:
            fact = "The human brain uses 20 percent of body oxygen."

        if fact not in used:
            return fact
