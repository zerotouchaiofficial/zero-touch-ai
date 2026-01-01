import os
from gtts import gTTS

os.makedirs("audio", exist_ok=True)

with open("facts.txt") as f:
    text = f.read().strip()

if not text:
    raise Exception("facts.txt empty")

tts = gTTS(text)
tts.save("audio/voice.mp3")

print("Audio created")
