import random
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

WIDTH, HEIGHT = 1080, 1920

with open("current_fact.txt") as f:
    text = f.read()

bg = random.choice([
    "backgrounds/bg1.jpg",
    "backgrounds/bg2.jpg",
    "backgrounds/bg3.jpg",
    "backgrounds/bg4.jpg",
])

audio = AudioFileClip("audio/voice.mp3")
duration = audio.duration + 1

background = (
    ImageClip(bg)
    .set_duration(duration)
    .resize((WIDTH, HEIGHT))
)

final = background.set_audio(audio)

final.write_videofile(
    "videos/short.mp4",
    fps=30,
    codec="libx264",
    audio_codec="aac",
    bitrate="8000k"
)
