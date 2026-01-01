import os
from moviepy.editor import (
    ColorClip,
    AudioFileClip,
    CompositeVideoClip,
    TextClip
)

AUDIO_DIR = "audio"
VIDEO_DIR = "videos"

os.makedirs(VIDEO_DIR, exist_ok=True)

audio_files = sorted(os.listdir(AUDIO_DIR))
if not audio_files:
    raise Exception("No audio files found in audio/ — voice.py failed")

audio_path = os.path.join(AUDIO_DIR, audio_files[0])
audio = AudioFileClip(audio_path)

# FORCE MIN 7 SECONDS
duration = max(audio.duration, 7)

# 1080x1920 vertical
background = ColorClip(
    size=(1080, 1920),
    color=(0, 0, 0),
    duration=duration
)

text = TextClip(
    "Did you know?",
    fontsize=90,
    color="white",
    font="DejaVu-Sans-Bold"
).set_position("center").set_duration(duration)

video = CompositeVideoClip([background, text]).set_audio(audio)

output_path = os.path.join(VIDEO_DIR, "short.mp4")

video.write_videofile(
    output_path,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    bitrate="8000k",        # 🔥 VERY IMPORTANT
    threads=4,
    preset="medium"
)

print(f"Video created: {output_path}")
