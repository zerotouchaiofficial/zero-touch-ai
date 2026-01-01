import os
from gtts import gTTS

TEXT_FILE = "data/text.txt"
AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)

if not os.path.exists(TEXT_FILE):
    raise Exception("text.txt missing — generate.py failed")

with open(TEXT_FILE, "r", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    raise Exception("text.txt is empty")

tts = gTTS(text)
output = os.path.join(AUDIO_DIR, "voice.mp3")
tts.save(output)

print("Audio created:", output)
