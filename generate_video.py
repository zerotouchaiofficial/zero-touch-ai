from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageSequenceClip
import textwrap, os

W, H = 720, 1280
FPS = 30
DURATION = 60  # seconds
FRAMES = FPS * DURATION

os.makedirs("videos", exist_ok=True)

with open("current_fact.txt", "r") as f:
    facts = f.read().split(".")[:-1]

frames = []
font = ImageFont.load_default()

for i in range(FRAMES):
    img = Image.new("RGB", (W, H), (20, 20, 20))
    draw = ImageDraw.Draw(img)

    fact_index = min(i // (FRAMES // len(facts)), len(facts) - 1)
    text = facts[fact_index].strip()

    wrapped = textwrap.fill(text, width=30)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
    x = (W - bbox[2]) // 2
    y = (H - bbox[3]) // 2

    draw.multiline_text((x, y), wrapped, font=font, fill=(255, 255, 255), align="center")
    frames.append(np.array(img))

clip = ImageSequenceClip(frames, fps=FPS)
clip.write_videofile(
    "videos/short.mp4",
    codec="libx264",
    audio=False,
    fps=FPS,
    verbose=False,
    logger=None
)
