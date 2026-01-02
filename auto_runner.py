import subprocess, time, json
from fact_engine import generate_fact, load_used, save_used

SHORTS_PER_DAY = 20
FACTS_PER_VIDEO = 4   # 60 seconds total

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

    print(f"✅ Uploaded short {i+1}/20")
    time.sleep(15)
