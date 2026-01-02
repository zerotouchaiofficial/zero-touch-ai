from gtts import gTTS
from pathlib import Path

FACT_FILE = "current_fact.txt"
OUT_AUDIO = "audio/voice.mp3"

Path("audio").mkdir(exist_ok=True)

with open(FACT_FILE, "r") as f:
    fact = f.read().strip()

if not fact:
    raise Exception("❌ No fact found for voice")

tts = gTTS(text=fact, lang="en")
tts.save(OUT_AUDIO)

print("🎙 Audio created")
