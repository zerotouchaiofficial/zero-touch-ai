import random

FACTS_FILE = "facts.txt"
USED_FILE = "used_facts.txt"

with open(FACTS_FILE, "r") as f:
    facts = [x.strip() for x in f if x.strip()]

used = set()
try:
    with open(USED_FILE, "r") as f:
        used = set(x.strip() for x in f)
except:
    pass

available = list(set(facts) - used)

if not available:
    raise Exception("No unused facts left")

fact = random.choice(available)

with open("current_fact.txt", "w") as f:
    f.write(fact)

with open(USED_FILE, "a") as f:
    f.write(fact + "\n")

print(fact)
