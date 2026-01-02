from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
import os

os.makedirs("videos", exist_ok=True)

TEXT = "Did you know?\nOctopus have 3 hearts 🐙"

video = ColorClip(size=(720, 1280), color=(0, 0, 0), duration=6)

text = TextClip(
    TEXT,
    fontsize=60,
    color="white",
    method="caption",
    size=(650, None),
    align="center"
).set_position("center").set_duration(6)

final = CompositeVideoClip([video, text])

final.write_videofile(
    "videos/short.mp4",
    fps=30,
    codec="libx264",
    audio=False
)

print("✅ Video generated: videos/short.mp4")
