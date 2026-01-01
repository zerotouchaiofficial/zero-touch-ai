import os
import random
from pathlib import Path
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    ColorClip
)

# ---------------- CONFIG ----------------
WIDTH = 1080
HEIGHT = 1920
FPS = 30

AUDIO_DIR = "audio"
BG_DIR = "backgrounds"
OUT_DIR = "videos"
OUT_FILE = f"{OUT_DIR}/short.mp4"

# ---------------- PREP ----------------
Path(AUDIO_DIR).mkdir(exist_ok=True)
Path(BG_DIR).mkdir(exist_ok=True)
Path(OUT_DIR).mkdir(exist_ok=True)

# ---------------- AUDIO ----------------
audio_files = [
    f for f in os.listdir(AUDIO_DIR)
    if f.endswith(".mp3")
]

if not audio_files:
    raise Exception("❌ No audio files found in audio/")

audio_path = os.path.join(AUDIO_DIR, audio_files[-1])
audio = AudioFileClip(audio_path)

duration = max(5, int(audio.duration) + 1)

# ---------------- BACKGROUND ----------------
bg_images = [
    os.path.join(BG_DIR, f)
    for f in os.listdir(BG_DIR)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

if bg_images:
    bg_path = random.choice(bg_images)

    bg = ImageClip(bg_path).set_duration(duration)

    # 🔥 SAFE scaling (NO PIL, NO ANTIALIAS)
    scale = max(WIDTH / bg.w, HEIGHT / bg.h)
    bg = bg.resized(scale)

    # Center crop
    bg = bg.crop(
        x_center=bg.w / 2,
        y_center=bg.h / 2,
        width=WIDTH,
        height=HEIGHT
    )
else:
    bg = ColorClip(
        size=(WIDTH, HEIGHT),
        color=(18, 18, 18)
    ).set_duration(duration)

# ---------------- FINAL VIDEO ----------------
final = CompositeVideoClip([bg]).set_audio(audio)

final.write_videofile(
    OUT_FILE,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    bitrate="9000k",
    threads=4,
    preset="medium",
    logger=None
)

print(f"✅ Video created: {OUT_FILE}")
