import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

WIDTH, HEIGHT = 1080, 1920

with open("current_fact.txt", "r") as f:
    text = f.read().strip()

audio = AudioFileClip("audio/voice.mp3")
duration = max(audio.duration + 1, 6)

bg_folder = "backgrounds"
bg_files = [f for f in os.listdir(bg_folder) if f.endswith((".jpg", ".png"))]
bg_path = os.path.join(bg_folder, bg_files[0])

bg = (
    ImageClip(bg_path)
    .set_duration(duration)
    .resize(height=HEIGHT)
    .crop(x_center=WIDTH // 2, width=WIDTH, height=HEIGHT)
)

from moviepy.video.VideoClip import ColorClip

overlay = ColorClip(
    size=(WIDTH, HEIGHT),
    color=(0, 0, 0)
).set_opacity(0.35).set_duration(duration)

final = CompositeVideoClip([bg, overlay])
final = final.set_audio(audio)

os.makedirs("videos", exist_ok=True)

final.write_videofile(
    "videos/short.mp4",
    fps=30,
    codec="libx264",
    audio_codec="aac",
    bitrate="8000k"
)

print("Video created")
