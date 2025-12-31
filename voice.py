from TTS.api import TTS

tts = TTS(model_name="tts_models/en/vctk/vits")
tts.tts_to_file(
    text=open("fact.txt").read(),
    file_path="voice.wav"
)
