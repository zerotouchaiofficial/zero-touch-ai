import os
import random
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip

WIDTH = 1080
HEIGHT = 1920
DURATION_MIN = 7  # seconds (safe for YouTube Shorts)

AUDIO_DIR = "audio"
BG_DIR = "backgrounds"
OUTPUT_DIR = "videos"

os.makedirs(OUTPUT_DIR, exist_ok=True)

audio_files = sorted(os.listdir(AUDIO_DIR))
bg_files = sorted(os.listdir(BG_DIR))

if not audio_files:
    raise Exception("No audio files found in audio/")

if not bg_files:
    raise Exception("No background images found in backgrounds/")

audio_path = os.path.join(AUDIO_DIR, audio_files[0])
bg_path = os.path.join(BG_DIR, random.choice(bg_files))

audio = AudioFileClip(audio_path)
duration = max(audio.duration, DURATION_MIN)

bg = (
    ImageClip(bg_path)
    .set_duration(duration)
    .resize((WIDTH, HEIGHT))
)

video = CompositeVideoClip([bg]).set_audio(audio)

output_path = os.path.join(OUTPUT_DIR, "short.mp4")

video.write_videofile(
    output_path,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    bitrate="6000k",
    threads=2,
    preset="medium"
)

print(f"Video created: {output_path}")
