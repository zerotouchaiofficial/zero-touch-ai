import json
from gtts import gTTS

with open("facts.json") as f:
    facts = json.load(f)

script = ". ".join(facts) + ". Follow for more amazing facts."

tts = gTTS(script)
tts.save("voice.mp3")

print("🎙 Voice created")
