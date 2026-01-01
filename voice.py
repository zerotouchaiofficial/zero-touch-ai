import os
from gtts import gTTS

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

TEXT_FILE = "facts/facts.txt"
AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)

# Read text
if not os.path.exists(TEXT_FILE):
    raise Exception("facts/facts.txt not found")

with open(TEXT_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

if not lines:
    raise Exception("facts.txt is empty — nothing to convert to voice")

# Create audio files
for i, text in enumerate(lines, start=1):
    tts = gTTS(text=text, lang="en")
    output_path = os.path.join(AUDIO_DIR, f"audio_{i}.mp3")
    tts.save(output_path)
    print("Created:", output_path)
