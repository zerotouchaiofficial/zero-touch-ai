from moviepy.editor import (
    ColorClip,
    AudioFileClip,
    CompositeVideoClip,
)
import random

WIDTH, HEIGHT = 1080, 1920
DURATION = 8

audio = AudioFileClip("voice.mp3")
duration = min(audio.duration, DURATION)

bg = ColorClip(
    size=(WIDTH, HEIGHT),
    color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)),
    duration=duration
)

video = CompositeVideoClip([bg]).set_audio(audio)

video.write_videofile(
    "short.mp4",
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("🎬 Video created")
