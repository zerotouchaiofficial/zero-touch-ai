import os
from moviepy.editor import ColorClip

os.makedirs("videos", exist_ok=True)

clip = ColorClip(
    size=(720, 1280),
    color=(0, 0, 0),
    duration=5
)

clip.write_videofile(
    "videos/short.mp4",
    fps=30,
    codec="libx264",
    audio=False
)

print("✅ Video generated successfully")
