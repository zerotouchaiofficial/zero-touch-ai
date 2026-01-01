import os
from gtts import gTTS

AUDIO_DIR = "audio"
FACTS_DIR = "facts"

os.makedirs(AUDIO_DIR, exist_ok=True)

fact_text = None

# 1️⃣ Try root facts.txt
if os.path.exists("facts.txt"):
    with open("facts.txt", "r") as f:
        fact_text = f.read().strip()

# 2️⃣ Try facts folder (first .txt file)
elif os.path.isdir(FACTS_DIR):
    files = [f for f in os.listdir(FACTS_DIR) if f.endswith(".txt")]
    if files:
        with open(os.path.join(FACTS_DIR, files[0]), "r") as f:
            fact_text = f.read().strip()

if not fact_text:
    raise Exception("No fact text found (facts.txt or facts/*.txt missing)")

out = os.path.join(AUDIO_DIR, "voice.mp3")
gTTS(fact_text).save(out)

print("Audio created:", out)
