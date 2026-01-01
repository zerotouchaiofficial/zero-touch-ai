import os
from moviepy.editor import ImageClip, AudioFileClip

AUDIO = "audio/voice.mp3"
BG = "background.png"
OUT_DIR = "videos"
OUT = "videos/short.mp4"

os.makedirs(OUT_DIR, exist_ok=True)

if not os.path.exists(AUDIO):
    raise Exception("Audio missing — voice.py failed")

audio = AudioFileClip(AUDIO)
clip = ImageClip(BG).set_duration(audio.duration).set_audio(audio)

clip.write_videofile(
    OUT,
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

print("Video created:", OUT)
