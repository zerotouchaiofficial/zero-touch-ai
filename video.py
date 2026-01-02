import os
import random
from moviepy.editor import (
    ColorClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip
)

# ---------------- CONFIG ----------------
WIDTH = 1080
HEIGHT = 1920
DURATION = 60
AUDIO_PATH = "audio/voice.mp3"
OUTPUT = "videos/short.mp4"

os.makedirs("videos", exist_ok=True)

# --------------- LOAD FACT ----------------
with open("current_fact.txt", "r") as f:
    fact = f.read().strip()

if not fact:
    raise Exception("❌ No fact found")

# --------------- BACKGROUND ----------------
# Random pleasant background colors
COLORS = [
    (20, 20, 20),
    (15, 30, 60),
    (40, 20, 60),
    (10, 60, 40),
    (60, 30, 20)
]

bg_color = random.choice(COLORS)

background = ColorClip(
    size=(WIDTH, HEIGHT),
    color=bg_color,
    duration=DURATION
)

# --------------- TEXT ----------------
text = TextClip(
    fact,
    fontsize=70,
    color="white",
    size=(900, None),
    method="caption",
    align="center"
).set_position("center").set_duration(DURATION)

# --------------- AUDIO ----------------
audio = AudioFileClip(AUDIO_PATH).set_duration(DURATION)

# --------------- COMPOSE ----------------
video = CompositeVideoClip([background, text])
video = video.set_audio(audio)

video.write_videofile(
    OUTPUT,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    threads=2,
    preset="medium"
)

print("✅ Video created successfully")
