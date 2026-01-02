import subprocess, time
from fact_engine import generate_fact, load_used, save_used

SHORTS_PER_DAY = 20
FACTS_PER_VIDEO = 4

used = load_used()

for i in range(SHORTS_PER_DAY):
    facts = []

    for _ in range(FACTS_PER_VIDEO):
        fact = generate_fact(used)
        facts.append(fact)
        used.add(fact)

    save_used(used)

    with open("current_fact.txt", "w") as f:
        f.write(" ".join(facts))

    subprocess.run(["python", "generate_video.py"], check=True)
    subprocess.run(["python", "upload.py"], check=True)

    print(f"Uploaded {i+1}/{SHORTS_PER_DAY}")
    time.sleep(15)

print("AUTO RUNNER FINISHED SUCCESSFULLY")
import os
os._exit(0)
