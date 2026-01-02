import json
import random

FACTS_PER_VIDEO = 10

def get_facts(topic):
    with open("data/facts_pool.json", "r") as f:
        pool = json.load(f)

    selected = random.sample(pool, FACTS_PER_VIDEO)
    return [f"{topic}: {fact}" for fact in selected]
