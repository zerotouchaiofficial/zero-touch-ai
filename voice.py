from TTS.api import TTS
import os

tts = TTS(model_name="tts_models/en/vctk/vits")

def generate_voice(text):
    os.makedirs("output", exist_ok=True)
    out = "output/audio.wav"
    tts.tts_to_file(text=text, file_path=out)
    return out
