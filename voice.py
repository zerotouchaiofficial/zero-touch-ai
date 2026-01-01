import os
from gtts import gTTS

FACT_FILE = "facts.txt"
AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(FACT_FILE, "r") as f:
    text = f.read().strip()

if not text:
    raise Exception("facts.txt empty")

out = os.path.join(AUDIO_DIR, "voice.mp3")
gTTS(text).save(out)

print("Audio created:", out)
