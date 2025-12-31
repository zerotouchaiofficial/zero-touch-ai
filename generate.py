import random

FACTS = [
    "Octopuses have three hearts.",
    "A day on Venus is longer than a year on Earth.",
    "Honey never spoils, even after thousands of years.",
    "Bananas are berries, but strawberries are not.",
    "Your brain uses about 20 percent of your body's energy.",
    "Sharks existed before trees.",
    "There are more stars in the universe than grains of sand on Earth.",
    "Wombat poop is cube-shaped.",
    "Humans share about 60 percent DNA with bananas.",
    "An octopus has blue blood."
]

def generate_fact():
    return random.choice(FACTS)

if __name__ == "__main__":
    print(generate_fact())
