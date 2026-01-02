from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
import numpy as np
import os

os.makedirs("videos", exist_ok=True)

WIDTH, HEIGHT = 720, 1280
TEXT = "Did you know?\nOctopus have 3 hearts 🐙"
DURATION = 6
FPS = 30

frames = []

for _ in range(DURATION * FPS):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    bbox = draw.multiline_textbbox((0, 0), TEXT, font=font, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (WIDTH - text_w) // 2
    y = (HEIGHT - text_h) // 2

    draw.multiline_text((x, y), TEXT, fill="white", font=font, align="center")

    # 🔑 FIX: convert PIL → NumPy
    frames.append(np.array(img))

clip = ImageSequenceClip(frames, fps=FPS)
clip.write_videofile(
    "videos/short.mp4",
    codec="libx264",
    audio=False
)

print("✅ Video generated successfully")
