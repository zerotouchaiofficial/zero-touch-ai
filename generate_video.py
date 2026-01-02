from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os, textwrap
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

# Video settings
W, H = 720, 1280
FPS = 30
DURATION = 60
FRAMES = FPS * DURATION

os.makedirs("videos", exist_ok=True)

# Read generated facts
with open("current_fact.txt", "r") as f:
    facts = [x.strip() for x in f.read().split(".") if x.strip()]

frames = []
font = ImageFont.load_default()

for i in range(FRAMES):
    img = Image.new("RGB", (W, H), (18, 18, 18))
    draw = ImageDraw.Draw(img)

    idx = min(i // (FRAMES // len(facts)), len(facts) - 1)
    text = facts[idx]

    wrapped = textwrap.fill(text, width=28)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)

    x = (W - bbox[2]) // 2
    y = (H - bbox[3]) // 2

    draw.multiline_text(
        (x, y),
        wrapped,
        fill=(255, 255, 255),
        font=font,
        align="center"
    )

    frames.append(np.array(img))

clip = ImageSequenceClip(frames, fps=FPS)
clip.write_videofile(
    "videos/short.mp4",
    codec="libx264",
    audio=False,
    fps=FPS
)

# --- FORCE CLEAN EXIT FOR GITHUB ACTIONS ---
import os
import sys
import time

time.sleep(1)
sys.stdout.flush()
sys.stderr.flush()
os._exit(0)
