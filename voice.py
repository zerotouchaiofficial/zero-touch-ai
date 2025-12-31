from gtts import gTTS

text = open("fact.txt").read()

tts = gTTS(text=text, lang="en")
tts.save("voice.mp3")
