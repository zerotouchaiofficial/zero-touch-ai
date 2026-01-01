import os
import random
from pathlib import Path
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    ColorClip
)

WIDTH = 1080
HEIGHT = 1920
FPS = 30
OUTPUT = "videos/short.mp4"
AUDIO_DIR = "audio"
BG_DIR = "backgrounds"

# Ensure output dirs exist
Path("videos").mkdir(exist_ok=True)
Path(AUDIO_DIR).mkdir(exist_ok=True)

# ---- Load audio ----
audio_files = [
    f for f in os.listdir(AUDIO_DIR)
    if f.endswith(".mp3")
]

if not audio_files:
    raise Exception("No audio found in audio/")

audio_path = os.path.join(AUDIO_DIR, audio_files[-1])
audio = AudioFileClip(audio_path)
duration = max(audio.duration, 5)  # force minimum length

# ---- Background selection ----
bg_images = []
if os.path.exists(BG_DIR):
    bg_images = [
        os.path.join(BG_DIR, f)
        for f in os.listdir(BG_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

if bg_images:
    bg_path = random.choice(bg_images)
    background = (
        ImageClip(bg_path)
        .set_duration(duration)
        .resize(height=HEIGHT)
        .crop(x_center=WIDTH // 2, y_center=HEIGHT // 2, width=WIDTH, height=HEIGHT)
    )
else:
    # Fallback solid background
    background = (
        ColorClip(size=(WIDTH, HEIGHT), color=(15, 15, 15))
        .set_duration(duration)
    )

# ---- Combine ----
final = (
    CompositeVideoClip([background])
    .set_audio(audio)
)

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    bitrate="8000k",
    threads=4,
    preset="medium"
)

print(f"Video created: {OUTPUT}")
