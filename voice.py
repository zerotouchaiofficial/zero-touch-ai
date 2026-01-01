from gtts import gTTS
import os

with open("current_fact.txt", "r") as f:
    text = f.read().strip()

os.makedirs("audio", exist_ok=True)

tts = gTTS(text=text, lang="en")
tts.save("audio/voice.mp3")

print("Audio created")
