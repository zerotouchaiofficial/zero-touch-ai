from gtts import gTTS

with open("fact.txt") as f:
    text = f.read()

tts = gTTS(text=text, lang="en")
tts.save("voice.mp3")

print("🎙 Voice created")
