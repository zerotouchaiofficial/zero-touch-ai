import os
import random
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip

WIDTH = 1080
HEIGHT = 1920
DURATION = 60

FACT_FILE = "current_fact.txt"
AUDIO = "audio/voice.mp3"
OUTPUT = "videos/short.mp4"

os.makedirs("videos", exist_ok=True)

# ---------- SAFE FACT LOAD ----------
if not os.path.exists(FACT_FILE):
    raise Exception("❌ Fact file missing — generate.py did not run")

with open(FACT_FILE) as f:
    fact = f.read().strip()

if not fact:
    raise Exception("❌ Fact is empty")

# ---------- BACKGROUND ----------
COLORS = [(20,20,20), (40,20,60), (15,30,60), (10,60,40)]
bg = ColorClip((WIDTH, HEIGHT), color=random.choice(COLORS), duration=DURATION)

# ---------- TEXT ----------
txt = TextClip(
    fact,
    fontsize=70,
    color="white",
    size=(900, None),
    method="caption",
    align="center"
).set_duration(DURATION).set_position("center")

# ---------- AUDIO ----------
audio = AudioFileClip(AUDIO).set_duration(DURATION)

video = CompositeVideoClip([bg, txt]).set_audio(audio)

video.write_videofile(
    OUTPUT,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Video created")
