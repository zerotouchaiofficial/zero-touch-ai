from gtts import gTTS

with open("current_fact.txt") as f:
    text = f.read()

tts = gTTS(text)
tts.save("audio/voice.mp3")

print("Audio created")
