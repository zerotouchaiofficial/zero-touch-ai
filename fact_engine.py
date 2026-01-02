import json
import random

def get_facts(topic):
    with open("data/facts_pool.json") as f:
        pool = json.load(f)

    selected = random.sample(pool, 10)
    return [f"{topic}: {fact}" for fact in selected]
