from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
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

    text_bbox = draw.multiline_textbbox((0, 0), TEXT, font=font, align="center")
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (WIDTH - text_width) // 2
    y = (HEIGHT - text_height) // 2

    draw.multiline_text((x, y), TEXT, fill="white", font=font, align="center")

    frames.append(img)

clip = ImageSequenceClip(frames, fps=FPS)
clip.write_videofile(
    "videos/short.mp4",
    codec="libx264",
    audio=False
)

print("✅ Video generated without ImageMagick")
